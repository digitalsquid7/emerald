import os
from configparser import ConfigParser

from emerald.config.dataclass import EmailConfig, Config, DatabaseConfig, AssetConfig


class EnvVarRetriever:
    @staticmethod
    def retrieve(name: str):
        env_var = os.getenv(name)

        if env_var is None:
            raise Exception(f"required environment variable not set: {name}")

        return env_var


class PathRetriever:
    @staticmethod
    def get_emerald_path() -> str:
        return EnvVarRetriever.retrieve("EMERALD_CONFIG_PATH")

    @staticmethod
    def get_logger_path() -> str:
        return EnvVarRetriever.retrieve("EMERALD_LOGGER_CONFIG_PATH")


class ConfigRetriever:

    __config_parser = None

    @classmethod
    def retrieve(cls, config_parser: ConfigParser) -> Config:
        cls.__config_parser = config_parser
        return Config(
            cls.__retrieve_email_config(),
            cls.__retrieve_database_config(),
            cls.__retrieve_asset_config(),
        )

    @classmethod
    def __retrieve_email_config(cls) -> EmailConfig:
        return EmailConfig(
            cls.__config_parser.get("email", "host"),
            cls.__config_parser.getint("email", "port"),
            cls.__config_parser.get("email", "from_address"),
            cls.__config_parser.getboolean("email", "use_ssl"),
        )

    @classmethod
    def __retrieve_database_config(cls) -> DatabaseConfig:
        return DatabaseConfig(
            cls.__config_parser.get("database", "connection_string")
        )

    @classmethod
    def __retrieve_asset_config(cls) -> AssetConfig:
        return AssetConfig(
            cls.__config_parser.get("asset", "html_path"),
            cls.__config_parser.get("asset", "notification_file"),
        )
