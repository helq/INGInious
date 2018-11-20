import os
from inginious.frontend.plugins.utils import create_static_resource_page

_static_folder_path = os.path.join(os.path.dirname(__file__), "static")


def init(plugin_manager, course_factory, client, config):
    plugin_manager.add_page(r'/UNCode/static/(.*)', create_static_resource_page(_static_folder_path))

    plugin_manager.add_hook("javascript_header", lambda: "/UNCode/static/js/uncode.js")
    plugin_manager.add_hook("css", lambda: "/UNCode/static/css/uncode.css")
