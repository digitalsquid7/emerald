from datetime import datetime

from sqlalchemy import Engine, update

from emerald.repository.dataclass import EmailRequestData
from emerald.repository.sql import TableFactory


class EmeraldRepositoryUpdater:
    def __init__(
            self,
            engine: Engine,
            table_factory: TableFactory,
    ):
        self.__engine = engine
        self.__table_factory = table_factory

    def update_email_request_sent_datetime(self, email_request: EmailRequestData):
        email_request_table = self.__table_factory.create("email_request")

        statement = update(email_request_table)\
            .values({"sent_datetime": datetime.now()})\
            .where(email_request_table.c.id == email_request.identifier)

        with self.__engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
