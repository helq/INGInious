import json
import tempfile
import os
from inginious.frontend.pages.course_admin.task_edit import CourseEditTask
from collections import OrderedDict
import re
from .graderforms import MultilangForm, InvalidGraderError

_PLUGIN_PATH = os.path.dirname(__file__)
_BASE_RENDERER_PATH = _PLUGIN_PATH
_RUN_FILE_TEMPLATE_PATH = os.path.join(_PLUGIN_PATH, 'run_file_template.txt')



def generate_grader(form):
    """ This method generates a grader through the form data """
    
    problem_id = form.task_data["grader_problem_id"]
    test_cases = [(test_case["input_file"], test_case["output_file"])
                  for test_case in form.task_data["grader_test_cases"]]
    weights = [test_case["weight"] for test_case in form.task_data["grader_test_cases"]]
    options = {
        "compute_diff": form.task_data["grader_compute_diffs"],
        "treat_non_zero_as_runtime_error": form.task_data["treat_non_zero_as_runtime_error"],
        "diff_max_lines": form.task_data["grader_diff_max_lines"],
        "diff_context_lines": form.task_data["grader_diff_context_lines"],
        "output_diff_for": [test_case["input_file"] for test_case in form.task_data["grader_test_cases"]
                            if test_case["diff_shown"]]
    }

    with open(_RUN_FILE_TEMPLATE_PATH, "r") as template, tempfile.TemporaryDirectory() as temporary:
        run_file_template = template.read()

        run_file_name = 'run'
        target_run_file = os.path.join(temporary, run_file_name)

        with open(target_run_file, "w") as f:
            f.write(run_file_template.format(
                problem_id=repr(problem_id), test_cases=repr(test_cases),
                options=repr(options), weights=repr(weights)))
        
        form.task_fs.copy_to(temporary)





def on_task_editor_submit(course, taskid, task_data, task_fs):
    """ This method use the form from the plugin to generate
    the grader (code to use the utilities from the containers i.e multilang) """

    print(task_data)

    # Create form object
    task_data["generate_grader"] = "generate_grader" in task_data

    if task_data['generate_grader']:
        form = MultilangForm(task_data, task_fs)
        
        # Try to parse and validate all the information
        try:
            form.parse()
            form.validate()
        except InvalidGraderError as e:
            return json.dumps({'status': 'error', 'message': e.message})
        
        # Update the task_data        

        # Generate the grader
        if form.task_data['generate_grader']:
            generate_grader(form)


def grader_generator_tab(course, taskid, task_data, template_helper):
    tab_id = 'tab_grader'
    link = '<i class="fa fa-check-circle fa-fw"></i>&nbsp; Grader'
    grader_test_cases_dump = json.dumps(task_data.get('grader_test_cases', []))
    content = template_helper.get_custom_renderer(_BASE_RENDERER_PATH, layout=False).grader(task_data,
                                                                                            grader_test_cases_dump,
                                                                                            course, taskid)
    template_helper.add_javascript('/grader_generator/static/js/grader_generator.js')

    return tab_id, link, content


def grader_footer(course, taskid, task_data, template_helper):
    return template_helper.get_custom_renderer(_BASE_RENDERER_PATH, layout=False).grader_templates()