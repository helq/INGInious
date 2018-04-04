import os
from inginious.frontend.plugins.utils import create_static_resource_page

_static_folder_path = os.path.join(os.path.dirname(__file__), "static")

def custom_input(inputId, language, template_helper):
    """ Displays some informations about the contest on the course page"""
    try:
        return str(template_helper.get_custom_renderer('frontend/plugins/custom_input', layout=False)
                   .custom_input(inputId, inputId)) + "<p>" + str(inputId) + " " + language +"</p>"
    except:
        print("custom_input error")
        return "<p>Error" + str(tool) + " " + language +"</p>"


def init(plugin_manager, course_factory, client, config):
    #plugin_manager.add_page(r'/custom_input/static/(.*)', create_static_resource_page(_static_folder_path))
    print("Init plugin")
    plugin_manager.add_hook('code_tool', custom_input)