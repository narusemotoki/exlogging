import unittest
import mock  # unittest.mock is from Python 3.3
import exlogging
import logging.handlers
import os
import sys

if sys.version_info > (3, 4):
    import importlib
    reload = importlib.reload
else:
    import imp
    reload = imp.reload


class ExloggingTest(unittest.TestCase):
    filepath = '/tmp/exlogging.log'

    def tearDown(self):
        if os.path.isfile(ExloggingTest.filepath):
            os.remove(ExloggingTest.filepath)

        exlogging.loggers = {}
        reload(logging)

    def test_file_hander(self):
        exlogging.init({
            'file': {
                'filepath': '/tmp/exlogging.log',
                'level': 'debug',
            }
        })
        message = "This is debug message"
        exlogging.debug(message)

        with open(ExloggingTest.filepath) as f:
            actual = f.read()

        self.assertTrue(message in actual, "Should record logging message.")

    @mock.patch('logging.handlers.SMTPHandler')
    def test_email_handler(self, MockSMTPHandler):
        smtp_host = 'smtp host'
        smtp_port = 21
        email_from = 'email_from@example.com'
        email_to = 'email_to@example.com'
        email_subject = "email subject"
        smtp_username = 'smtp username'
        smtp_password = 'smtp password'

        exlogging.init({
            'email': {
                'level': 'error',
                'smtp_host': smtp_host,
                'smtp_port': smtp_port,
                'email_from': email_from,
                'email_to': email_to,
                'email_subject': email_subject,
                'smtp_username': smtp_username,
                'smtp_password': smtp_password,
            }
        })

        MockSMTPHandler.assert_called_with(**{
            'mailhost': (smtp_host, smtp_port),
            'fromaddr': email_from,
            'toaddrs': (email_to, ),
            'subject': email_subject,
            'credentials': (smtp_username, smtp_password),
            'secure': (),
        })