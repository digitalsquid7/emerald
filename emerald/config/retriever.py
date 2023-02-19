from configparser import ConfigParser

from emerald.config.dataclass import EmailConfig, Config, DatabaseConfig, AssetConfig


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
