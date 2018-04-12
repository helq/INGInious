import json
import web

import os
from inginious.frontend.pages.utils import INGIniousPage
from inginious.client.client_sync import ClientSync

# static_folder_path = os.path.join(os.path.dirname(__file__), "static")


class BaseCustomInput(object):
    def __init__(self, calling_page):
        self.cp = calling_page
        self.submission_manager = self.cp.submission_manager
        self.user_manager = self.cp.user_manager
        self.database = self.cp.database
        self.course_factory = self.cp.course_factory
        self.template_helper = self.cp.template_helper
        self.default_allowed_file_extensions = self.cp.default_allowed_file_extensions
        self.default_max_file_size = self.cp.default_max_file_size
        self.webterm_link = self.cp.webterm_link
        self.plugin_manager = self.cp.plugin_manager

    def POST(self, client):  # pylint: disable=arguments-differ
        """ POST a new submission """
        username = self.user_manager.session_username()
        try:
            userinput = web.input()
            print(userinput)

            courseid = userinput["courseid"]
            taskid = userinput["taskid"]
            course = self.course_factory.get_course(courseid)
            if not self.user_manager.course_is_open_to_user(course, username):
                return self.template_helper.get_renderer().course_unavailable()

            task = course.get_task(taskid)
            if not self.user_manager.task_is_visible_by_user(task, username):
                return self.template_helper.get_renderer().task_unavailable()
            print(task)
            self.user_manager.user_saw_task(username, courseid, taskid)

            # TODO: this is nearly the same as the code in the webapp.
            # We should refactor this.

            try:
                temp_client = ClientSync(client)
                result, grade, problems, tests, custom, archive, stdout, stderr = temp_client.new_job(
                    task, userinput)

                data = {
                    "status": ("done" if result[0] == "success" or result[0] == "failed" else "error"),
                    "result": result[0],
                    "grade": grade,
                    "text": result[1],
                    "tests": tests,
                    "problems": problems,
                    "stdout": stdout,
                    "stderr": stderr
                }

                web.header('Content-Type', 'application/json')
                print(data)
                return json.dumps(data)
            except Exception as ex:
                web.header('Content-Type', 'application/json')
                return json.dumps({"status": "error", "text": str(ex)})
        except Exception as ex:
            if web.config.debug:
                raise
            else:
                raise web.notfound()


class CustomInput(INGIniousPage):
    client = None

    def POST(self):
        return BaseCustomInput(self).POST(self.client)


def custom_input(inputId, courseid, taskid, template_helper):
    """ Displays some informations about the contest on the course page"""
    try:
        return str(template_helper.get_custom_renderer('frontend/plugins/custom_input', layout=False)
                   .custom_input(inputId, courseid, taskid))
    except Exception as ex:
        print(ex)
        return "<p>Error in custom input</p>"


def init(plugin_manager, course_factory, client, config):
    # plugin_manager.add_page(r'/custom_input/static/(.*)', create_static_resource_page(_static_folder_path))
    print("Init plugin")
    # plugin_manager.add_hook("javascript_footer", lambda: "/inginious/frontend/plugins/custom_input/static/js/main.js")
    CustomInput.client = client
    plugin_manager.add_hook('code_tool', custom_input)
    plugin_manager.add_page('/api/custom_input/', CustomInput)