from collections import OrderedDict
from abc import ABC, abstractmethod
from inginious.frontend.pages.course_admin.task_edit import CourseEditTask

class InvalidGraderError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)

        self.message = message


class GraderForm(ABC):
    """ This class represents an abstract class in order to model the different GraderForms. 
    A form refers to the data received from the grader form and the way that data should be parsed and validated. 
    """

    def __init__(self, task_data, task_fs):
        self.task_data = dict(task_data)
        self.task_fs = task_fs

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def validate(self):
        pass


class MultilangForm(GraderForm):
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

        if len(test_cases) == 0:
            raise InvalidGraderError("You must provide test cases to autogenerate the grader")

        input_files_are_unique = (len(set(test_case["input_file"] for test_case in test_cases)) ==
                              len(test_cases))

        if not input_files_are_unique:
            raise InvalidGraderError("Duplicated input files in grader")

        return test_cases

    def parse(self):
        """
        This function parse the data from task_data i.e (test_cases)
        """
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

        # Parse test cases
        self.task_data['grader_test_cases'] = self.parse_and_validate_test_cases()

    def validate(self):
        """
        This function validates the data from task_data
        """
        # Check if grader problem was set
        if 'grader_problem_id' not in self.task_data:
            raise InvalidGraderError("Grader: the problem was not specified")
        
        # The problem_id does not exists
        if self.task_data['grader_problem_id'] not in self.task_data['problems']:
            raise InvalidGraderError("Grader: problem does not exist")

        # check the type of problem. (written code or project folder only options)
        problem_type = self.task_data["problems"][self.task_data["grader_problem_id"]]["type"]

        if problem_type not in ['code_multiple_languages', 'code_file_multiple_languages']:
            raise InvalidGraderError("Grader: only Code Multiple Language and Code File Multiple Language problems are supported")

        # Check values that must be positive
        if self.task_data["grader_diff_max_lines"] <= 0:
            raise InvalidGraderError("'Maximum diff lines' must be positive")

        if self.task_data["grader_diff_context_lines"] <= 0:
            raise InvalidGraderError("'Diff context lines' must be positive")
    
