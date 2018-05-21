from ipmonitor.notifiers.base import BaseNotifier
from ipmonitor.notifiers.email_notifier import EmailNotifier
from ipmonitor.notifiers.groupme_notifier import GroupmeNotifier
from ipmonitor.notifiers.groupme_notifier import GROUPME_BOT_URL
from ipmonitor.notifiers.stdout_notifier import StdoutNotifier
from ipmonitor.notifiers.notifier_factory import NotifierFactory

from email.mime.text import MIMEText
import unittest
import mock


class TestNotifierFactory(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_bad_notifier(self):
        self.assertRaises(RuntimeError, NotifierFactory.create,
                          'FooBarBadNotifier')

    def test_create_stdout(self):
        stdout = NotifierFactory.create('stdout')
        self.assertEqual(type(stdout), StdoutNotifier)

    def test_create_groupme(self):
        self.assertRaises(TypeError, NotifierFactory.create, 'groupme')

        groupme = NotifierFactory.create('groupme', '12345')
        self.assertEqual(type(groupme), GroupmeNotifier)

        groupme = NotifierFactory.create('groupme', bot_id='12345')
        self.assertEqual(type(groupme), GroupmeNotifier)

    def test_create_email(self):
        self.assertRaises(TypeError, NotifierFactory.create, 'email')
        self.assertRaises(TypeError, NotifierFactory.create, 'email',
                          'noreply@example.com')

        email = NotifierFactory.create('email', 'noreply@example.com',
                                       'smtp.google.com', 587,
                                       'noreply@example.com', 'password1')
        self.assertEqual(type(email), EmailNotifier)


class TestBaseNotifier(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_notify(self):
        self.assertRaises(NotImplementedError, BaseNotifier().notify, 'a', 'b')


class TestEmailNotifier(unittest.TestCase):

    def setUp(self):
        self.email = EmailNotifier('noreply@example.com', 'smtp.gmail.com',
                                   587, 'noreply@example.com', 'testpassword')

    def tearDown(self):
        pass

    @mock.patch('ipmonitor.notifiers.email_notifier.smtplib.SMTP')
    def test_notify(self, mock_smtp):
        test_old = '1.2.3.4'
        test_new = '4.3.2.1'
        test_email = 'noreply@example.com'
        exp_txt = MIMEText('Public IP has Changed from {0} to {1}!'.format(
            test_old, test_new))
        exp_txt['Subject'] = EmailNotifier.SUBJECT
        exp_txt['From'] = test_email
        exp_txt['To'] = test_email

        self.email.notify(test_old, test_new)
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
        smtp_inst = mock_smtp.return_value
        smtp_inst.login.assert_called_once_with(test_email, 'testpassword')
        smtp_inst.sendmail.assert_called_once_with(test_email,
                                                   [test_email],
                                                   exp_txt.as_string())
        smtp_inst.close.assert_called_once()


class TestGroupmeNotifier(unittest.TestCase):

    def setUp(self):
        self.groupme = GroupmeNotifier('12345')

    def tearDown(self):
        pass

    @mock.patch('ipmonitor.notifiers.groupme_notifier.post')
    def test_notify(self, mock_post):
        test_old = '1.2.3.4'
        test_new = '4.3.2.1'
        exp_txt = 'Public IP has Changed from {0} to {1}!'.format(test_old,
                                                                  test_new)
        exp_data = dict(bot_id='12345', text=exp_txt)

        mock_post.return_value.status_code = 200
        self.groupme.notify(test_old, test_new)

        mock_post.assert_called_once_with(GROUPME_BOT_URL, data=exp_data)


class TestStdoutNotifier(unittest.TestCase):

    def setUp(self):
        self.stdout = StdoutNotifier()

    def tearDown(self):
        pass

    @mock.patch('__builtin__.print')
    def test_notify(self, mock_print):
        test_old = '1.2.3.4'
        test_new = '4.3.2.1'
        exp_txt = 'Public IP has Changed from {0} to {1}!'.format(test_old,
                                                                  test_new)

        self.stdout.notify(test_old, test_new)
        mock_print.assert_called_once_with(exp_txt)
