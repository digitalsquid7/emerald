from jinja2 import Template


class EmailBodyGenerator:

    def __init__(self, template: Template):
        self.__template = template

    def generate(self, title, message) -> str:
        return self.__template.render(title=title, message=message)
