from logging import Logger

from sqlalchemy import Engine, select, Select

from emerald.email.body import EmailBodyGenerator
from emerald.repository.dataclass import EmailRequest
from emerald.sql import TableFactory


class EmeraldRepositoryReader:
    def __init__(
            self,
            engine: Engine,
            table_factory: TableFactory,
            email_body_generator: EmailBodyGenerator,
            logger: Logger,
    ):
        self.__engine = engine
        self.__table_factory = table_factory
        self.__email_body_generator = email_body_generator
        self.__logger = logger

    def read_email_requests(self) -> list[EmailRequest]:
        query = self.__create_email_requests_query()

        with self.__engine.connect() as conn:
            rows = conn.execute(query)

        return self.__create_email_requests(rows)

    def __create_email_requests_query(self) -> Select:
        email_request = self.__table_factory.create("email_request")
        email_type = self.__table_factory.create("email_type")
        email_recipient = self.__table_factory.create("email_recipient")

        joins = email_request \
            .join(email_type, email_request.c.email_type_id == email_type.c.id) \
            .join(email_recipient, email_request.c.email_recipient_id == email_recipient.c.id)

        return select(
            email_request.c.id,
            email_type.c.name,
            email_type.c.subject,
            email_type.c.file_name,
            email_recipient.c.email_address,
            email_recipient.c.first_name) \
            .select_from(joins) \
            .filter(email_request.c.sent_datetime.is_(None))

    def __create_email_requests(self, rows) -> list[EmailRequest]:
        email_requests = []

        for row in rows:
            email_requests.append(self.__create_email_request(row))

        self.__logger.info(f"Found {len(email_requests)} emails that need sending.")

        return email_requests

    def __create_email_request(self, row) -> EmailRequest:
        return EmailRequest(row[0], row[4], row[2], self.__email_body_generator.generate(row[2], row[3]))
