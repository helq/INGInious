import web
import os
import inginious.frontend.pages.api._api_page as api

from inginious.frontend.pages.api._api_page import APIAuthenticatedPage
from inginious.common.course_factory import CourseNotFoundException, CourseUnreadableException, InvalidNameException

class TaskPreviewFileAPI(APIAuthenticatedPage):
    def API_GET(self):
        # Validate parameters
        username = self.user_manager.session_username()
        course_id = web.input(course_id=None).course_id
        task_id = web.input(task_id=None).task_id
        if course_id is None:
            raise api.APIError(400, {"error" : "course_id is mandatory"})
        if task_id is None:
            raise api.APIError(400, {"error": "task_id is mandatory"})

        try:
            course = self.course_factory.get_course(course_id)
        except (CourseNotFoundException, InvalidNameException, CourseUnreadableException):
            raise api.APIError(400, {"error", "The course does not exists or the user does not have permissions"})
        
        if not self.user_manager.course_is_user_registered(course, username):
            raise api.APIError(400, {"error", "The course does not exists or the user does not have permissions"})


        try:
            task = course.get_task(task_id)
        except:
            raise api.APIError(400, {"error", "The task does not exists in the course"})
        
        # Asks for file
        try:
            f = open(os.path.join(task.get_fs().prefix + 'preview'), 'r')
            return 200, f.read()
        except:
            return 200, "File not found"
        # Returns file text
        