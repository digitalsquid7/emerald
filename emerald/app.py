import logging
import logging.config
from configparser import ConfigParser
from datetime import datetime
from smtplib import SMTP

from jinja2 import Environment, select_autoescape, FileSystemLoader
from sqlalchemy import create_engine

from emerald.config import ConfigRetriever
from emerald.email.body import EmailBodyGenerator
from emerald.email.sender import EmailSender
from emerald.repository import EmeraldRepositoryReader
from emerald.sql import TableFactory
from emerald.util import EnvironmentVariableRetriever


class Emerald:

    @classmethod
    def run(cls):
        logger_config_path = EnvironmentVariableRetriever.retrieve("EMERALD_LOGGER_CONFIG_PATH")
        logging.config.fileConfig(fname=logger_config_path, disable_existing_loggers=False)
        logger = logging.getLogger(__name__)
        cls.__try_to_run_emerald(logger)

    @classmethod
    def __try_to_run_emerald(cls, logger: logging.Logger):
        logger.info(f"Emerald started at {datetime.now()}")

        try:
            cls.__run_emerald(logger)
        except Exception as exc:
            logger.error("Emerald exception occurred...", exc_info=exc)
            raise
        finally:
            logger.info(f"Emerald finished at {datetime.now()}")

    @classmethod
    def __run_emerald(cls, logger: logging.Logger):
        # Create dependencies
        config_path = EnvironmentVariableRetriever.retrieve("EMERALD_CONFIG_PATH")
        config_parser = ConfigParser()
        config_parser.read(config_path)
        config = ConfigRetriever.retrieve(config_parser)

        engine = create_engine(config.database.connection_string)
        table_factory = TableFactory()
        template_loader = FileSystemLoader(config.asset.html_path)
        env = Environment(loader=template_loader, autoescape=select_autoescape())
        template = env.get_template(config.asset.notification_file)
        email_body_generator = EmailBodyGenerator(template, config.asset.html_path)
        emerald_repository_reader = EmeraldRepositoryReader(engine, table_factory, email_body_generator, logger)

        smtp_server = SMTP(config.email.host, config.email.port)
        email_sender = EmailSender(config.email, smtp_server, logger)

        # Run Emerald logic
        email_requests = emerald_repository_reader.read_email_requests()
        email_sender.send_emails(email_requests)
