from ipmonitor.monitor import Monitor
import unittest
import mock


class MockParser(object):

    def __init__(self):
        self.get_ip = mock.MagicMock()
        self.get_ip.return_value = '1.2.3.4'


class MockNotifier(object):

    def __init__(self):
        self.notify = mock.MagicMock()


class TestMonitor(unittest.TestCase):

    def setUp(self):
        self.parser = MockParser()
        self.notifiers = [MockNotifier(), MockNotifier()]
        self.monitor = Monitor(self.parser, self.notifiers)
        self.monitor.ip = '4.3.2.1'

    def tearDown(self):
        pass

    def test_notify(self):
        self.monitor.send_notifications('foo', 'bar')
        for notifier in self.notifiers:
            notifier.notify.assert_called_once_with('foo', 'bar')

    @mock.patch('ipmonitor.monitor.sleep')
    def test_monitor(self, mock_sleep):
        self.assertEqual(self.monitor.ip, '4.3.2.1')
        self.monitor.sleep_time = 0
        self.monitor.send_notifications = mock.MagicMock()

        self.monitor.monitor()
        mock_sleep.assert_called_once_with(self.monitor.sleep_time)
        self.monitor.send_notifications.assert_called_once_with('4.3.2.1',
                                                                '1.2.3.4')
        self.assertEqual(self.monitor.ip, '1.2.3.4')

    def test_run(self):
        self.monitor.monitor = mock.MagicMock(
            side_effect=KeyboardInterrupt('mock keyboard interrupt'))
        try:
            self.monitor.run()
        except Exception:
            self.fail('Should have Caught KeyboardInterrupt')
