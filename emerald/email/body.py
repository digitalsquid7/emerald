import os

from jinja2 import Template


class EmailBodyGenerator:

    def __init__(self, template: Template, html_path: str):
        self.__template = template
        self.__html_path = html_path
        self.__html_bodies = {}

    def generate(self, title: str, body_file_name: str) -> str:
        html_body = self.__html_bodies.get(body_file_name)

        if html_body is None:
            with open(os.path.join(self.__html_path, body_file_name)) as file:
                html_body = file.read()

            self.__html_bodies[body_file_name] = html_body

        return self.__template.render(title=title, message=html_body)
