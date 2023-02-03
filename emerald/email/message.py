import abc


class MessageGenerator(abc.ABC):

    @abc.abstractmethod
    def generate(self, customer_name: str) -> str:
        pass


class WelcomeMessageGenerator(MessageGenerator):

    def generate(self, customer_name: str) -> str:
        return f"""Hi {customer_name},
This is a test welcome message!
That is all!
"""


class InvoiceMessageGenerator(MessageGenerator):

    def generate(self, customer_name: str) -> str:
        return f"""Hi {customer_name},
You owe us money for your product!
Please pay us!
"""


class MessageGeneratorFactory:

    def __init__(self):
        self.__message_generators = {
            "welcome": WelcomeMessageGenerator(),
            "invoice": InvoiceMessageGenerator(),
        }

    def create(self, name) -> MessageGenerator:
        message_generator = self.__message_generators.get(name)

        if not message_generator:
            raise Exception(f"name provided does not exist: {name}")

        return message_generator
