from dataclasses import dataclass
from emerald.repository import EmailRequestData


@dataclass
class Email:
    request_data: EmailRequestData
    mime_message: str
