import logging.config
from configparser import ConfigParser
from datetime import datetime
from logging import Logger

from dotenv import load_dotenv
from jinja2 import Environment, select_autoescape, FileSystemLoader, BaseLoader
from sqlalchemy import create_engine

from emerald.app import Emerald
from emerald.config import ConfigRetriever, Config, PathRetriever
from emerald.email import EmailGenerator
from emerald.email.sender import EmailSender
from emerald.repository import EmeraldRepositoryReader, EmeraldRepositoryUpdater
from emerald.repository.sql import TableFactory


class Initialiser:

    @classmethod
    def initialise(cls) -> Emerald:
        load_dotenv()
        logger = cls.__create_logger()
        logger.info("Emerald initialisation started at %s", datetime.now())

        try:
            return cls.__try_to_initialise(logger)
        except Exception as exc:
            logger.error("Exception occurred during initialisation...", exc_info=exc)
            raise
        finally:
            logger.info("Emerald initialisation finished at %s", datetime.now())

    @classmethod
    def __create_logger(cls) -> Logger:
        logger_config_path = PathRetriever.get_logger_path()
        logging.config.fileConfig(fname=logger_config_path, disable_existing_loggers=False)
        return logging.getLogger("root")

    @classmethod
    def __try_to_initialise(cls, logger: Logger) -> Emerald:
        config = cls.create_config()
        engine = create_engine(config.database.connection_string)
        table_factory = TableFactory()
        emerald_repository_updater = EmeraldRepositoryUpdater(engine, table_factory)
        email_sender = EmailSender(config.email, emerald_repository_updater, logger)
        base_env = Environment(loader=BaseLoader(), autoescape=select_autoescape())
        file_env = Environment(loader=FileSystemLoader(config.asset.html_path), autoescape=select_autoescape())
        notification_template = file_env.get_template(config.asset.notification_file)
        email_generator = EmailGenerator(notification_template, base_env, config.asset, config.email)
        emerald_repository_reader = EmeraldRepositoryReader(engine, table_factory, logger)
        return Emerald(emerald_repository_reader, email_generator, email_sender, logger)

    @classmethod
    def create_config(cls) -> Config:
        config_path = PathRetriever.get_emerald_path()
        config_parser = ConfigParser()
        config_parser.read(config_path)
        return ConfigRetriever.retrieve(config_parser)
