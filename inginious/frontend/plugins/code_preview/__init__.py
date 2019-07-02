import os
from inginious.frontend.plugins.utils import create_static_resource_page

from .pages.api.task_preview_file_api import TaskPreviewFileAPI


_static_folder_path = os.path.join(os.path.dirname(__file__), "static")

def init(plugin_manager, course_factory, client, config):
    plugin_manager.add_page('/api/code_preview/', TaskPreviewFileAPI)
    plugin_manager.add_page(r'/code_preview/static/(.*)', create_static_resource_page(_static_folder_path))


    
    plugin_manager.add_hook("javascript_footer", lambda: "/code_preview/static/js/code_preview_load.js")