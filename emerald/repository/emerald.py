from emerald.email.body import EmailBodyGenerator
from emerald.email.message import MessageGeneratorFactory


class EmailRequest:

    def __init__(self, email_address, name, subject, body):
        self.email_address = email_address
        self.name = name
        self.subject = subject
        self.body = body


class EmeraldRepository:

    def __init__(
            self,
            message_generator_factory: MessageGeneratorFactory,
            email_body_generator: EmailBodyGenerator,
    ):
        self.message_generator_factory = message_generator_factory
        self.email_body_generator = email_body_generator

    def retrieve_email_requests(self):
        email_requests = [
            EmailRequest(
                "squid@email.com",
                "Squid",
                "Invoice Due!",
                self.email_body_generator.generate("Invoice!", self.message_generator_factory.create("invoice").generate("Squid"))
            ),
            EmailRequest(
                "octopus@email.com",
                "Octopus",
                "Welcome!",
                self.email_body_generator.generate("Welcome!", self.message_generator_factory.create("welcome").generate("Octopus"))
            ),
        ]

        return email_requests
