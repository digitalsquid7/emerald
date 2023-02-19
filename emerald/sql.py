from sqlalchemy import MetaData, Column, Integer, String, Table, DateTime


class TableFactory:
    def __init__(self):
        meta = MetaData()
        self.__tables = {
            "email_request": Table(
                "email_request", meta,
                Column("id", Integer, primary_key=True),
                Column("email_recipient_id", Integer),
                Column("email_type_id", Integer),
                Column("created_datetime", DateTime),
                Column("sent_datetime", DateTime),
            ),
            "email_type": Table(
                "email_type", meta,
                Column("id", Integer, primary_key=True),
                Column("name", String),
                Column("subject", String),
                Column("file_name", String),
            ),
            "email_recipient": Table(
                "email_recipient", meta,
                Column("id", Integer, primary_key=True),
                Column("email_address", String),
                Column("first_name", String),
            )
        }

    def create(self, name: str):
        table = self.__tables.get(name)

        if table is None:
            raise ValueError(f"name provided does not exist: {name}")

        return table
