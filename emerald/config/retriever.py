import abc
import os
from configparser import ConfigParser

from emerald.config.model import EmailConfig


class ConfigRetriever(abc.ABC):

    @abc.abstractmethod
    def retrieve(self) -> object:
        pass


class ConfigFilePathRetriever(ConfigRetriever):

    def retrieve(self) -> str:
        return os.getenv("EMERALD_CONFIG_PATH")


class EmailConfigRetriever(ConfigRetriever):

    def __init__(self, config_parser: ConfigParser):
        self.__config_parser = config_parser

    def retrieve(self) -> EmailConfig:
        return EmailConfig(
            self.__config_parser.get("email", "host"),
            self.__config_parser.getint("email", "port"),
        )


class DatabaseConfigRetriever(ConfigRetriever):

    def __init__(self, config_parser: ConfigParser):
        self.__config_parser = config_parser

    def retrieve(self) -> str:
        return self.__config_parser.get("database", "connection_string")
