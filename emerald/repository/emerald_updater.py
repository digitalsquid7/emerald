from datetime import datetime
from logging import Logger

from sqlalchemy import Engine, update

from emerald.repository.dataclass import EmailRequest
from emerald.sql import TableFactory


class EmeraldRepositoryUpdater:
    def __init__(
            self,
            engine: Engine,
            table_factory: TableFactory,
            logger: Logger,
    ):
        self.__engine = engine
        self.__table_factory = table_factory
        self.__logger = logger

    def update_email_request_sent_datetime(self, email_request: EmailRequest):
        email_request_table = self.__table_factory.create("email_request")

        statement = update(email_request_table)\
            .values({"sent_datetime": datetime.now()})\
            .where(email_request_table.c.id == email_request.identifier)

        with self.__engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
