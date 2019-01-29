import os
from inginious.frontend.plugins.utils import create_static_resource_page
from .pages.api.add_course_students_csv_file_api import AddCourseStudentsCsvFile

_static_folder_path = os.path.join(os.path.dirname(__file__), "static")
_REGISTER_STUDENTS_MODAL_HTML_FILE = "register_students_modal.html"


def read_file(file_name):
    with open(_static_folder_path + "/" + file_name, "r") as file:
        content_file = file.read()
    return content_file


def init(plugin_manager, course_factory, client, config):
    plugin_manager.add_page(r'/register_students/static/(.*)', create_static_resource_page(_static_folder_path))
    plugin_manager.add_page("/api/addStudents/", AddCourseStudentsCsvFile)

    plugin_manager.add_hook("javascript_header", lambda: "/register_students/static/js/register.js")
    plugin_manager.add_hook("additional_body_html", lambda: read_file(_REGISTER_STUDENTS_MODAL_HTML_FILE))
