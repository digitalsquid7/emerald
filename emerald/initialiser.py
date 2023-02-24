import logging.config
from logging import Logger
from configparser import ConfigParser
from datetime import datetime
from smtplib import SMTP

from jinja2 import Environment, select_autoescape, FileSystemLoader
from sqlalchemy import create_engine

from emerald.app import Emerald
from emerald.config import ConfigRetriever, Config
from emerald.email.body import EmailBodyGenerator
from emerald.email.sender import EmailSender
from emerald.repository import EmeraldRepositoryReader
from emerald.sql import TableFactory
from emerald.util import EnvironmentVariableRetriever


class Initialiser:

    @classmethod
    def initialise(cls) -> Emerald:
        logger = cls.__create_logger()
        logger.info(f"Emerald initialisation started at {datetime.now()}")

        try:
            return cls.__try_to_initialise(logger)
        except Exception as exc:
            logger.error("Exception occurred during initialisation...", exc_info=exc)
            raise
        finally:
            logger.info(f"Emerald initialisation finished at {datetime.now()}")

    @classmethod
    def __create_logger(cls) -> Logger:
        logger_config_path = EnvironmentVariableRetriever.retrieve("EMERALD_LOGGER_CONFIG_PATH")
        logging.config.fileConfig(fname=logger_config_path, disable_existing_loggers=False)
        return logging.getLogger("root")

    @classmethod
    def __try_to_initialise(cls, logger: Logger) -> Emerald:
        config = cls.create_config()
        emerald_repository_reader = cls.__create_emerald_repository_reader(config, logger)
        email_sender = cls.__create_email_sender(config, logger)
        return Emerald(emerald_repository_reader, email_sender, logger)

    @classmethod
    def create_config(cls) -> Config:
        config_path = EnvironmentVariableRetriever.retrieve("EMERALD_CONFIG_PATH")
        config_parser = ConfigParser()
        config_parser.read(config_path)
        return ConfigRetriever.retrieve(config_parser)

    @classmethod
    def __create_emerald_repository_reader(cls, config, logger) -> EmeraldRepositoryReader:
        engine = create_engine(config.database.connection_string)
        table_factory = TableFactory()
        template_loader = FileSystemLoader(config.asset.html_path)
        env = Environment(loader=template_loader, autoescape=select_autoescape())
        template = env.get_template(config.asset.notification_file)
        email_body_generator = EmailBodyGenerator(template, config.asset.html_path)
        return EmeraldRepositoryReader(engine, table_factory, email_body_generator, logger)

    @classmethod
    def __create_email_sender(cls, config, logger) -> EmailSender:
        smtp_server = SMTP(config.email.host, config.email.port)
        return EmailSender(config.email, smtp_server, logger)