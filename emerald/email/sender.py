from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import Logger
from smtplib import SMTP
from ssl import create_default_context

from emerald.config import EmailConfig
from emerald.repository import EmailRequest


class EmailSender:

    def __init__(self, email_config: EmailConfig, smtp_server: SMTP, logger: Logger):
        self.email_config = email_config
        self.smtp_server = smtp_server
        self.__logger = logger

    def send_emails(self, email_requests: list[EmailRequest]):
        if self.email_config.use_ssl:
            context = create_default_context()
            self.smtp_server.starttls(context=context)

        with self.smtp_server as server:
            self.__send_emails(server, email_requests)

    def __send_emails(self, server, email_requests):
        emails_sent = 0
        try:
            for email_request in email_requests:
                self.__try_to_send_email(server, email_request)
                emails_sent += 1
        finally:
            self.__logger.info(f"Successfully sent {emails_sent} emails.")

    def __try_to_send_email(self, server, email_request):
        try:
            self.__send_email(server, email_request)
        except Exception:
            self.__logger.error(f"Failed to send email to : {email_request}")
            raise

    def __send_email(self, server, email_request):
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
