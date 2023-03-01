from dataclasses import dataclass


@dataclass
class EmailRequestData:
    identifier: int
    email_address: str
    subject: str
    file_name: str
    first_name: str

