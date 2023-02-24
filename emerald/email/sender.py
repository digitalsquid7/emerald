from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import Logger
from smtplib import SMTP

from emerald.config import EmailConfig
from emerald.repository import EmailRequest, EmeraldRepositoryUpdater


class EmailSender:

    def __init__(self, email_config: EmailConfig, emerald_repository_updater: EmeraldRepositoryUpdater, logger: Logger):
        self.__config = email_config
        self.__emerald_repository_updater = emerald_repository_updater
        self.__logger = logger

    def send_emails(self, email_requests: list[EmailRequest]):
        emails_sent = 0

        with SMTP(self.__config.host, self.__config.port) as server:
            try:
                for email_request in email_requests:
                    self.__try_to_send_email(server, email_request)
                    emails_sent += 1
            finally:
                self.__logger.info(f"Successfully sent {emails_sent} emails.")

    def __try_to_send_email(self, server, email_request):
        try:
            server.sendmail(
                self.__config.from_address,
                email_request.email_address,
                self.__create_message(email_request),
            )
            self.__emerald_repository_updater.update_email_request_sent_datetime(email_request)
        except Exception:
            self.__logger.error(f"Failed on email : {email_request}")
            raise

    def __create_message(self, email_request: EmailRequest) -> str:
        message = MIMEMultipart()
        message["From"] = self.__config.from_address
        message["To"] = email_request.email_address
        message["Subject"] = email_request.subject
        message.attach(MIMEText(email_request.body, "html"))
        return message.as_string()
