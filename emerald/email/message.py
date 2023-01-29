import abc


class Recipient:

    def __init__(self, first_name, product_name):
        self.first_name = first_name
        self.product_name = product_name


class MessageGenerator(abc.ABC):

    @abc.abstractmethod
    def generate(self, recipient: Recipient) -> str:
        pass


class WelcomeMessageGenerator(MessageGenerator):

    def generate(self, recipient: Recipient) -> str:
        return f"""Hi {recipient.first_name},
This is a test welcome message!
That is all!
"""


class InvoiceMessageGenerator(MessageGenerator):

    def generate(self, recipient: Recipient) -> str:
        return f"""Hi {recipient.first_name},
You owe us money for your product {recipient.product_name}!
Please pay us!
"""


class MessageGeneratorFactory:

    def __init__(self):
        self.__message_generators = {
            "welcome": WelcomeMessageGenerator(),
            "invoice": InvoiceMessageGenerator(),
        }

    def create_message_generator(self, name) -> MessageGenerator:
        message_generator = self.__message_generators.get(name)

        if not message_generator:
            raise Exception(f"name provided does not exist: {name}")

        return message_generator
