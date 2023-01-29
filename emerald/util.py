from configparser import ConfigParser


def create_config_parser(config_file_path) -> ConfigParser:
    config_parser = ConfigParser()
    config_parser.read(config_file_path)
    return config_parser
