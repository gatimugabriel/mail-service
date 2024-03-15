import unittest
from unittest import mock
from unittest.mock import patch, call
from mail_sender import MailService, Event

class TestMailService(unittest.TestCase):
    def setUp(self):
        self.smtp_host = 'smtp.example.com'
        self.smtp_port = 587
        self.sender_email = 'sender@example.com'
        self.sender_password = 'password'
        self.recipient = 'recipient@example.com'
        self.subject = 'Test Subject'
        self.message = 'Test Message'
        self.event = Event(self.recipient, self.subject, self.message)
        self.mail_service = MailService(self.smtp_host, self.smtp_port, self.sender_email, self.sender_password)

    @patch('smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        mock_server = mock_smtp.return_value
        self.mail_service.send_email(self.event)

        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(self.sender_email, self.sender_password)

        # Ensure that sendmail was called with the correct arguments
        expected_html_content = f"""
        <html>
        <body>
            <p>{self.message}</p>
        </body>
        </html>
        """
        expected_calls = [
            call(self.sender_email, self.recipient, mock.ANY),
            call().sendmail(self.sender_email, self.recipient, mock.ANY)
        ]
        mock_server.mock_calls == expected_calls

        mock_server.quit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
