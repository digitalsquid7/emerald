from datetime import datetime
from logging import Logger

from emerald.email import EmailGenerator
from emerald.email.sender import EmailSender
from emerald.repository import EmeraldRepositoryReader


class Emerald:

    def __init__(
            self,
            emerald_repository_reader: EmeraldRepositoryReader,
            email_generator: EmailGenerator,
            email_sender: EmailSender,
            logger: Logger,
    ):
        self.__emerald_repository_reader = emerald_repository_reader
        self.__email_generator = email_generator
        self.__email_sender = email_sender
        self.__logger = logger

    def run(self):
        try:
            self.__logger.info(f"Emerald execution started at {datetime.now()}")
            self.__try_to_run()
        except Exception as exc:
            self.__logger.error("Exception occurred during execution...", exc_info=exc)
            raise
        finally:
            self.__logger.info(f"Emerald execution finished at {datetime.now()}")

    def __try_to_run(self):
        email_requests = self.__emerald_repository_reader.read_email_requests()
        emails = self.__email_generator.generate_emails(email_requests)
        self.__email_sender.send_emails(emails)
