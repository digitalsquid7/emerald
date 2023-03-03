import logging
import unittest
from unittest.mock import patch, MagicMock, Mock

from emerald.config import EmailConfig
from emerald.email import EmailSender, Email
from emerald.repository import EmailRequestData


class TestEmailSender(unittest.TestCase):

    @patch('emerald.email.sender.SMTP', autospec=True)
    def test_send_emails(self, mock_smtp):
        config = EmailConfig("host", 25, "test@email.com", False)
        repository_updater = Mock()
        repository_updater.update_email_request_sent_datetime = MagicMock(return_value=None)
        logger = logging.getLogger()
        email_sender = EmailSender(config, repository_updater, logger)
        emails = [Email(EmailRequestData(1, "", "", "", ""), "")]

        email_sender.send_emails(emails)

        raise Exception("test")

        context = mock_smtp.return_value.__enter__.return_value
        context.sendmail.assert_called_once()
        repository_updater.update_email_request_sent_datetime.assert_called_once()


if __name__ == '__main__':
    unittest.main()
