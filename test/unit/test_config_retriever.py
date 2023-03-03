import unittest
from configparser import ConfigParser

from emerald.config import ConfigRetriever, Config, EmailConfig, DatabaseConfig, AssetConfig


class TestConfigRetriever(unittest.TestCase):

    def test_retrieve(self):
        config_file = """[email]
host = localhost
port = 26
from_address = emerald@email.com
use_ssl = false

[database]
connection_string = postgresql://test:test@localhost/emerald

[asset]
html_path = asset/html
notification_file = notification.html
"""
        config_parser = ConfigParser()
        config_parser.read_string(config_file)
        expected_config = Config(
            email=EmailConfig(
                host="localhost",
                port=26,
                from_address="emerald@email.com",
                use_ssl=False,
            ),
            database=DatabaseConfig(
                connection_string="postgresql://test:test@localhost/emerald",
            ),
            asset=AssetConfig(
                html_path="asset/html",
                notification_file="notification.html",
            )
        )

        actual_config = ConfigRetriever.retrieve(config_parser)

        self.assertEqual(expected_config, actual_config)

