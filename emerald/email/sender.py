from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from ssl import create_default_context

from emerald.config import EmailConfig
from emerald.repository import EmailRequest


class EmailSender:

    def __init__(self, email_config: EmailConfig, smtp_server: SMTP):
        self.email_config = email_config
        self.smtp_server = smtp_server

    def send_emails(self, email_requests: list[EmailRequest]):
        if self.email_config.use_ssl:
            context = create_default_context()
            self.smtp_server.starttls(context=context)

        with self.smtp_server as server:
            for email_request in email_requests:
                server.sendmail(
                    self.email_config.from_address,
                    email_request.email_address,
                    self.__create_message(email_request),
                )

    def __create_message(self, email_request: EmailRequest) -> str:
        message = MIMEMultipart()
        message["From"] = self.email_config.from_address
        message["To"] = email_request.email_address
        message["Subject"] = email_request.subject
        message.attach(MIMEText(email_request.body, "html"))
        return message.as_string()