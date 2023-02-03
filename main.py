from configparser import ConfigParser
from os import getenv
from os.path import join
from smtplib import SMTP

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

from emerald.config import EmailConfigRetriever, DatabaseConfigRetriever, ConfigFilePathRetriever
from emerald.email.body import EmailBodyGenerator
from emerald.email.message import MessageGeneratorFactory
from emerald.email.sender import EmailSender
from emerald.repository import EmeraldRepository
from emerald.util import create_config_parser


def main():
    config_file_path = ConfigFilePathRetriever().retrieve()
    config_parser = create_config_parser(config_file_path)
    email_config = EmailConfigRetriever(config_parser).retrieve()
    connection_string = DatabaseConfigRetriever(config_parser).retrieve()

    template_loader = FileSystemLoader(searchpath=join("asset", "html"))
    env = Environment(loader=template_loader, autoescape=select_autoescape())
    template = env.get_template("notification.html")
    email_body_generator = EmailBodyGenerator(template)
    message_generator_factory = MessageGeneratorFactory()

    repository = EmeraldRepository(message_generator_factory, email_body_generator)
    email_requests = repository.retrieve_email_requests()
    smtp_server = SMTP(email_config.host, email_config.port)
    email_sender = EmailSender(email_config, smtp_server)
    email_sender.send_emails(email_requests)


if __name__ == "__main__":
    main()
