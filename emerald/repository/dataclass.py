from dataclasses import dataclass


@dataclass
class EmailRequest:
    identifier: int
    email_address: str
    subject: str
    body: str

