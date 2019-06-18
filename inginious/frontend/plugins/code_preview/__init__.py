import os
#from inginious.frontend.plugins.utils import create_static_resourse_page

from .pages.api.task_preview_file_api import TaskPreviewFileAPI


_static_folder_path = os.path.join(os.path.dirname(__file__), "static")

def init(plugin_manager, course_factory, client, config):
    plugin_manager.add_page('/api/code_preview', TaskPreviewFileAPI)