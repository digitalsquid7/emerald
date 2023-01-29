from configparser import ConfigParser
from os import getenv
from os.path import join

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

from emerald.config import EmailConfigRetriever, DatabaseConfigRetriever, ConfigFilePathRetriever
from emerald.email.body import EmailBodyGenerator
from emerald.email.message import WelcomeMessageGenerator, Recipient
from emerald.util import create_config_parser


def main():
    config_file_path = ConfigFilePathRetriever().retrieve()
    config_parser = create_config_parser(config_file_path)
    email_config = EmailConfigRetriever(config_parser).retrieve()
    connection_string = DatabaseConfigRetriever(config_parser).retrieve()

    template_loader = FileSystemLoader(searchpath=join("asset", "html"))
    env = Environment(loader=template_loader, autoescape=select_autoescape())
    template = env.get_template("notification.html")

    recipient = Recipient("Squid", "Some Product Name")
    message_generator = WelcomeMessageGenerator()
    message_generator.generate(recipient)
    EmailBodyGenerator()

    print(template.render())



if __name__ == "__main__":
    main()
