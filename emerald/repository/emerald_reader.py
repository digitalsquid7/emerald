from logging import Logger

from sqlalchemy import Engine, select, Select

from emerald.repository.dataclass import EmailRequestData
from emerald.repository.sql import TableFactory


class EmeraldRepositoryReader:
    def __init__(
            self,
            engine: Engine,
            table_factory: TableFactory,
            logger: Logger,
    ):
        self.__engine = engine
        self.__table_factory = table_factory
        self.__logger = logger

    def read_email_requests(self) -> list[EmailRequestData]:
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

    def __create_email_requests(self, rows) -> list[EmailRequestData]:
        email_requests = []

        for row in rows:
            email_requests.append(EmailRequestData(row[0], row[4], row[2], row[3], row[5]))

        self.__logger.info(f"Found {len(email_requests)} emails that need sending.")

        return email_requests
