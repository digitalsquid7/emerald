import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Template, Environment

from emerald.config import AssetConfig, EmailConfig
from emerald.email.dataclass import Email
from emerald.repository import EmailRequestData


class EmailGenerator:

    def __init__(
            self,
            email_template: Template,
            base_env: Environment,
            asset_config: AssetConfig,
            email_config: EmailConfig
    ):
        self.__email_template = email_template
        self.__base_env = base_env
        self.__asset_config = asset_config
        self.__email_config = email_config
        self.__html_bodies = {}

    def generate_emails(self, email_requests: list[EmailRequestData]) -> list[Email]:
        emails = []

        for email_request in email_requests:
            email = self.__generate_email(email_request)
            emails.append(email)

        return emails

    def __generate_email(self, email_request: EmailRequestData) -> Email:
        html_body = self.__html_bodies.get(email_request.file_name)

        if html_body is None:
            with open(os.path.join(self.__asset_config.html_path, email_request.file_name), encoding="utf-8") as file:
                html_body = file.read()

            self.__html_bodies[email_request.file_name] = html_body

        body_template = self.__base_env.from_string(html_body)
        rendered_body = body_template.render(recipient_name=email_request.first_name)
        rendered_email = self.__email_template.render(title=email_request.subject, message=rendered_body)
        mime_message = self.__create_mime_message(email_request, rendered_email)

        return Email(email_request, mime_message)

    def __create_mime_message(self, email_request: EmailRequestData, email_body: str):
        message = MIMEMultipart()
        message["From"] = self.__email_config.from_address
        message["To"] = email_request.email_address
        message["Subject"] = email_request.subject
        message.attach(MIMEText(email_body, "html"))
        return message.as_string()
