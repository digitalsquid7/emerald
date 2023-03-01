from sqlalchemy import create_engine, insert
from sqlalchemy import select, bindparam

from emerald.initialiser import Initialiser
from emerald.repository.sql import TableFactory


class TestDataInserter:

    @classmethod
    def insert(cls):
        table_factory = TableFactory()
        email_request = table_factory.create("email_request")
        email_type = table_factory.create("email_type")
        email_recipient = table_factory.create("email_recipient")
        config = Initialiser.create_config()
        engine = create_engine(config.database.connection_string)

        recipient_sub_query = (
            select(email_recipient.c.id)
            .where(email_recipient.c.email_address == bindparam("email_address"))
            .scalar_subquery()
        )

        type_sub_query = (
            select(email_type.c.id)
            .where(email_type.c.name == bindparam("email_type"))
            .scalar_subquery()
        )

        with engine.connect() as conn:
            conn.execute(insert(email_recipient), cls.__create_email_recipient_data())
            conn.execute(
                insert(email_request)
                .values(email_recipient_id=recipient_sub_query, email_type_id=type_sub_query),
                cls.__create_email_request_data()
            )
            conn.commit()

    @classmethod
    def __create_email_recipient_data(cls) -> list[dict]:
        return [
            {"email_address": "jane@email.com", "first_name": "Jane"},
            {"email_address": "james@email.com", "first_name": "James"},
            {"email_address": "andrew@email.com", "first_name": "Andrew"},
            {"email_address": "meredith@email.com", "first_name": "Meredith"},
            {"email_address": "sam@email.com", "first_name": "Sam"},
            {"email_address": "charlie@email.com", "first_name": "Charlie"},
        ]

    @classmethod
    def __create_email_request_data(cls) -> list[dict]:
        return [
            {"email_address": "jane@email.com", "email_type": "Welcome"},
            {"email_address": "james@email.com", "email_type": "Welcome"},
            {"email_address": "andrew@email.com", "email_type": "Welcome"},
            {"email_address": "meredith@email.com", "email_type": "Invoice"},
            {"email_address": "sam@email.com", "email_type": "Invoice"},
            {"email_address": "charlie@email.com", "email_type": "Invoice"},
        ]


if __name__ == "__main__":
    TestDataInserter.insert()
