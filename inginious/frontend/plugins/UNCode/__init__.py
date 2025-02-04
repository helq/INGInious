import os
from inginious.frontend.plugins.utils import create_static_resource_page, read_file

_static_folder_path = os.path.join(os.path.dirname(__file__), "static")

_CONTEXT_TASK_TEMPLATE_FILE = "context_task_template.rst"
_TASK_CONTEXT_HELP_MODAL_HTML_FILE = "task_context_help_modal.html"
_TASK_FILES_UPLOAD_MULTIPLE_MODAL = "task_files_upload_multiple_modal.html"
_TASK_RESULT_LEGEND_MODAL_HTML_FILE = "task_result_legend_modal.html"


def init(plugin_manager, course_factory, client, config):
    plugin_manager.add_page(r'/UNCode/static/(.*)', create_static_resource_page(_static_folder_path))

    use_minified = config.get("use_minified", True)
    if use_minified:
        plugin_manager.add_hook("javascript_footer", lambda: "/UNCode/static/js/UNCode.min.js")
        plugin_manager.add_hook("css", lambda: "/UNCode/static/css/UNCode.min.css")
    else:
        plugin_manager.add_hook("javascript_footer", lambda: "/UNCode/static/js/uncode.js")
        plugin_manager.add_hook("javascript_footer", lambda: "/UNCode/static/js/task_files_upload_multiple.js")
        plugin_manager.add_hook("css", lambda: "/UNCode/static/css/uncode.css")

    plugin_manager.add_hook("additional_body_html", lambda: "<p class='hidden' id='default_task_context'>" +
                                                            read_file(_static_folder_path,
                                                                      _CONTEXT_TASK_TEMPLATE_FILE) + "</p>")
    plugin_manager.add_hook("additional_body_html",
                            lambda: read_file(_static_folder_path, _TASK_CONTEXT_HELP_MODAL_HTML_FILE))
    plugin_manager.add_hook("additional_body_html",
                            lambda: read_file(_static_folder_path, _TASK_FILES_UPLOAD_MULTIPLE_MODAL))
    plugin_manager.add_hook("additional_body_html",
                            lambda: read_file(_static_folder_path, _TASK_RESULT_LEGEND_MODAL_HTML_FILE))
