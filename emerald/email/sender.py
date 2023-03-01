from logging import Logger
from smtplib import SMTP

from emerald.config import EmailConfig
from emerald.email import Email
from emerald.repository import EmeraldRepositoryUpdater


class EmailSender:

    def __init__(
            self,
            email_config: EmailConfig,
            emerald_repository_updater: EmeraldRepositoryUpdater,
            logger: Logger,
    ):
        self.__config = email_config
        self.__emerald_repository_updater = emerald_repository_updater
        self.__logger = logger

    def send_emails(self, emails: list[Email]):
        emails_sent = 0

        with SMTP(self.__config.host, self.__config.port) as server:
            try:
                for email in emails:
                    self.__try_to_send_email(server, email)
                    emails_sent += 1
            finally:
                self.__logger.info(f"Successfully sent {emails_sent} emails.")

    def __try_to_send_email(self, server: SMTP, email: Email):
        try:
            server.sendmail(
                self.__config.from_address,
                email.request_data.email_address,
                email.mime_message,
            )
            self.__emerald_repository_updater.update_email_request_sent_datetime(email.request_data)
        except Exception:
            self.__logger.error(f"Failed on email : {email.request_data}")
            raise
