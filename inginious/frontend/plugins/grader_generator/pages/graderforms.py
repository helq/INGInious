import os
import tempfile
from collections import OrderedDict
from inginious.frontend.pages.course_admin.task_edit import CourseEditTask


_PLUGIN_PATH = os.path.dirname(__file__)
_BASE_RENDERER_PATH = _PLUGIN_PATH
_MULTILANG_FILE_TEMPLATE_PATH = os.path.join(_PLUGIN_PATH, 'run_file_template.txt')
_HDL_FILE_TEMPLATE_PATH = os.path.join(_PLUGIN_PATH, 'hdl_file_template.txt')

class InvalidGraderError(Exception):
    """
    This class represents any error present on
    the form for the generation of the grader (check edit_task->tab grader)
    """
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message

class GraderForm:
    """ This class parse and validates fields in the grader form, common
    in all the forms (i.e multilang, HDL) """

    def __init__(self, task_data, task_fs):
        self.task_data = dict(task_data)
        self.task_fs = task_fs
    
    def parse(self):
        # Convert diff_max_lines to integer if this fail the string isn't an integer
        try:
            self.task_data["grader_diff_max_lines"] = int(self.task_data.get("grader_diff_max_lines", None))
        except (ValueError, TypeError):
            raise InvalidGraderError("'Maximum diff lines' must be an integer")

        # Convert diff_context_lines to integer if this fails the string isn't an integer
        try:
            self.task_data["grader_diff_context_lines"] = int(self.task_data.get("grader_diff_context_lines", None))
        except (ValueError, TypeError):
            raise InvalidGraderError("'Diff context lines' must be an integer")

        # Parse checkboxes
        self.task_data["grader_compute_diffs"] = "grader_compute_diffs" in self.task_data
        self.task_data["treat_non_zero_as_runtime_error"] = "treat_non_zero_as_runtime_error" in self.task_data

    def validate(self):
        # Check if grader problem was set
        if 'grader_problem_id' not in self.task_data:
            raise InvalidGraderError("Grader: the problem was not specified")
        
        # The problem_id does not exists
        if self.task_data['grader_problem_id'] not in self.task_data['problems']:
            print(self.task_data)
            raise InvalidGraderError("Grader: problem does not exist")

        # check the type of problem. (written code or project folder only options)
        problem_type = self.task_data["problems"][self.task_data["grader_problem_id"]]["type"]

        if problem_type not in ['code_multiple_languages', 'code_file_multiple_languages']:
            raise InvalidGraderError("Grader: only 'Code Multiple Language' and 'Code File Multiple Language' problems are supported")

        # Check values that must be positive
        if self.task_data["grader_diff_max_lines"] <= 0:
            raise InvalidGraderError("'Maximum diff lines' must be positive")

        if self.task_data["grader_diff_context_lines"] <= 0:
            raise InvalidGraderError("'Diff context lines' must be positive")

class MultilangForm(GraderForm):
    """
    This class manage the fields only present on the multilang form.
    """
    def tests_to_dict(self):
        """ This method parses the tests cases information in a dictionary """

        # Transform grader_test_cases[] entries into an actual array (they are sent as separate keys).
        grader_test_cases = CourseEditTask.dict_from_prefix("grader_test_cases", self.task_data) or OrderedDict()

        # Remove the repeated information
        keys_to_remove = [key for key, _ in self.task_data.items() if key.startswith("grader_test_cases[")]
        for key in keys_to_remove:
            del self.task_data[key]

        return grader_test_cases

    def parse_and_validate_test_cases(self):
        """ This method parses all the test cases. """
        test_cases = []
        for _, test_case in self.tests_to_dict().items():
            # Parsing
            try:
                test_case["weight"] = float(test_case.get("weight", 1.0))
            except (ValueError, TypeError):
                raise InvalidGraderError("The weight for grader test cases must be a float")

            test_case["diff_shown"] = "diff_shown" in test_case

            # Validate
            if not test_case.get("input_file", None):
                raise InvalidGraderError("Invalid input file in grader test case")

            if not test_case.get("output_file", None):
                raise InvalidGraderError("Invalid output file in grader test case")

            if not self.task_fs.exists(test_case["input_file"]):
                raise InvalidGraderError("Grader input file does not exist: " + test_case["input_file"])

            if not self.task_fs.exists(test_case["output_file"]):
                raise InvalidGraderError("Grader output file does not exist: " + test_case["output_file"])

            test_cases.append(test_case)

        if not test_cases:
            raise InvalidGraderError("You must provide test cases to autogenerate the grader")

        input_files_are_unique = (len(set(test_case["input_file"] for test_case in test_cases)) ==
                              len(test_cases))

        if not input_files_are_unique:
            raise InvalidGraderError("Duplicated input files in grader")

        return test_cases

    def parse(self):
        super(MultilangForm, self).parse()
        # Parse test cases
        self.task_data['grader_test_cases'] = self.parse_and_validate_test_cases()

    def generate_grader(self):
        """ This method generates a grader through the form data """
    
        problem_id = self.task_data["grader_problem_id"]
        test_cases = [(test_case["input_file"], test_case["output_file"])
                    for test_case in self.task_data["grader_test_cases"]]
        weights = [test_case["weight"] for test_case in self.task_data["grader_test_cases"]]
        options = {
            "compute_diff": self.task_data["grader_compute_diffs"],
            "treat_non_zero_as_runtime_error": self.task_data["treat_non_zero_as_runtime_error"],
            "diff_max_lines": self.task_data["grader_diff_max_lines"],
            "diff_context_lines": self.task_data["grader_diff_context_lines"],
            "output_diff_for": [test_case["input_file"] for test_case in self.task_data["grader_test_cases"]
                                if test_case["diff_shown"]]
        }

        with open(_MULTILANG_FILE_TEMPLATE_PATH, "r") as template, tempfile.TemporaryDirectory() as temporary:
            run_file_template = template.read()

            run_file_name = 'run'
            target_run_file = os.path.join(temporary, run_file_name)

            with open(target_run_file, "w") as f:
                f.write(run_file_template.format(
                    problem_id=repr(problem_id), test_cases=repr(test_cases),
                    options=repr(options), weights=repr(weights)))
            
            self.task_fs.copy_to(temporary)

class HDLForm(GraderForm):
    """
    This class manages the fields only present on the HDL form
    """
    def parse(self):
        super(HDLForm, self).parse()

        if not self.task_data['testbench_file_name']:
            raise InvalidGraderError("No testbench was selected for testing")
        
        if not self.task_data['hdl_expected_output']:
            raise InvalidGraderError("No expected output was selected for testing")
        
    def generate_grader(self):
        problem_id = self.task_data["grader_problem_id"]
        testbench_file_name = self.task_data["testbench_file_name"]
        hdl_expected_output = self.task_data["hdl_expected_output"]
        options = {
            "compute_diff": self.task_data["grader_compute_diffs"],
            "treat_non_zero_as_runtime_error": self.task_data["treat_non_zero_as_runtime_error"],
            "diff_max_lines": self.task_data["grader_diff_max_lines"],
            "diff_context_lines": self.task_data["grader_diff_context_lines"],
            "output_diff_for": [testbench_file_name],
            "entity_name" : self.task_data.get('vhdl_entity', None)
        }

        with open(_HDL_FILE_TEMPLATE_PATH, "r") as template, tempfile.TemporaryDirectory() as temporary:
            run_file_template = template.read()

            run_file_name = 'run'
            target_run_file = os.path.join(temporary, run_file_name)

            with open(target_run_file, "w") as f:
                f.write(run_file_template.format(
                    problem_id=repr(problem_id), testbench=repr(testbench_file_name),
                    options=repr(options), output=repr(hdl_expected_output)))
            
            self.task_fs.copy_to(temporary)