import os

from inginious.frontend.plugins.utils import create_static_resource_page
from inginious.frontend.plugins.multilang.problems.code_multiple_languages_problem import \
    DisplayableCodeMultipleLanguagesProblem
from inginious.frontend.plugins.multilang.problems.code_multiple_file_languages_problem import \
    DisplayableCodeFileMultipleLanguagesProblem
from inginious.frontend.plugins.multilang.problems.constants import set_linter_url, set_python_tutor_url, \
    set_show_tools, get_show_tools

_static_folder_path = os.path.join(os.path.dirname(__file__), "static")


def init(plugin_manager, course_factory, client, plugin_config):
    # This option is to hide/show tools like Python tutor.
    show_tools = plugin_config.get("show_tools", True)
    if show_tools != "":
        set_show_tools(show_tools)

    plugin_manager.add_page(r'/multilang/static/(.*)', create_static_resource_page(_static_folder_path))

    use_minified = plugin_config.get("use_minified", True)

    if use_minified:
        plugin_manager.add_hook("javascript_footer", lambda: "/multilang/static/multilang.min.js")
        plugin_manager.add_hook("css", lambda: "/multilang/static/multilang.min.css")
    else:
        plugin_manager.add_hook("javascript_footer", lambda: "/multilang/static/multilang.js")
        plugin_manager.add_hook("javascript_footer", lambda: "/multilang/static/grader.js")
        plugin_manager.add_hook("css", lambda: "/multilang/static/multilang.css")
    if get_show_tools():
        if use_minified:
            plugin_manager.add_hook("javascript_footer", lambda: "/multilang/static/tools.min.js")
            plugin_manager.add_hook("css", lambda: "/multilang/static/tools.min.css")
        else:
            plugin_manager.add_hook("javascript_footer", lambda: "/multilang/static/pythonTutor.js")
            plugin_manager.add_hook("javascript_footer", lambda: "/multilang/static/codemirror_linter.js")
            plugin_manager.add_hook("javascript_footer", lambda: "/multilang/static/lint.js")
            plugin_manager.add_hook("css", lambda: "/multilang/static/lint.css")
    course_factory.get_task_factory().add_problem_type(DisplayableCodeMultipleLanguagesProblem)
    course_factory.get_task_factory().add_problem_type(DisplayableCodeFileMultipleLanguagesProblem)

    python_tutor_url = plugin_config.get("python_tutor_url", "")
    if python_tutor_url != "":
        set_python_tutor_url(python_tutor_url)

    linter_url = plugin_config.get("linter_url", "")
    if linter_url != "":
        set_linter_url(linter_url)
