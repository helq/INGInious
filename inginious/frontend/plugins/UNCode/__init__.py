import os
from inginious.frontend.plugins.utils import create_static_resource_page

_static_folder_path = os.path.join(os.path.dirname(__file__), "static")

_CONTEXT_TASK_TEMPLATE_FILE = "context_task_template.rst"
_TASK_CONTEXT_HELP_MODAL_HTML_FILE = "task_context_help_modal.html"
_TASK_FILES_UPLOAD_MULTIPLE_MODAL = "task_files_upload_multiple_modal.html"


def read_file(file_name):
    with open(_static_folder_path + "/" + file_name, "r") as file:
        content_file = file.read()
    return content_file


def init(plugin_manager, course_factory, client, config):
    plugin_manager.add_page(r'/UNCode/static/(.*)', create_static_resource_page(_static_folder_path))

    plugin_manager.add_hook("javascript_header", lambda: "/UNCode/static/js/uncode.js")
    plugin_manager.add_hook("javascript_header", lambda: "/UNCode/static/js/task_files_upload_multiple.js")
    plugin_manager.add_hook("css", lambda: "/UNCode/static/css/uncode.css")
    plugin_manager.add_hook("additional_body_html", lambda: "<p class='hidden' id='default_task_context'>" +
                                                            read_file(_CONTEXT_TASK_TEMPLATE_FILE) + "</p>")
    plugin_manager.add_hook("additional_body_html", lambda: read_file(_TASK_CONTEXT_HELP_MODAL_HTML_FILE))
    plugin_manager.add_hook("additional_body_html", lambda: read_file(_TASK_FILES_UPLOAD_MULTIPLE_MODAL))
