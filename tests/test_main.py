import unittest
import mock


MOCK_CFG = {
    'monitor': [
        {
            'parser': 'TestParser1',
            'notifiers': [
                {'name': 'TestNotifier1'},
                {'name': 'TestNotifier2'}
            ]
        },
        {
            'parser': 'TestParser2',
            'notifiers': {'name': 'TestNotifier3'}
        },
        {
            'parser': 'TestParser3',
            'notifiers': 'TestNotifier4',
            'sleep_time': '1234'
        }
    ]
}


class TestMain(unittest.TestCase):

    def setUp(self):
        self.mock_cfg = MOCK_CFG

    def tearDown(self):
        pass

    @mock.patch('ipmonitor.monitor.Monitor.start')
    @mock.patch('ipmonitor.main.signal.pause')
    @mock.patch('ipmonitor.config_manager.ConfigManager.get_monitors')
    @mock.patch('ipmonitor.main.get_monitor')
    def test_main(self, mock_get, mock_get_monitors, mock_pause, mock_start):
        mock_get_monitors.return_value = MOCK_CFG['monitor']
        from ipmonitor.main import main as test_main
        mock_pause.side_effect = KeyboardInterrupt("Mock Keyboard Interrupt")
        try:
            test_main()
        except Exception as e:
            self.fail("Should have caught KeyboardInterrupt, caught:" + str(e))

    @mock.patch('ipmonitor.parsers.parser_factory.ParserFactory.create')
    def test_get_parser(self, mock_factory):
        from ipmonitor.main import get_parser
        mock_factory.return_value = 'foo'
        self.assertEqual('foo', get_parser(self.mock_cfg['monitor'][0]))
        mock_factory.assert_called_with('TestParser1')

    @mock.patch('ipmonitor.notifiers.notifier_factory.NotifierFactory.create')
    def test_get_notifiers(self, mock_factory):
        from ipmonitor.main import get_notifiers
        get_notifiers(self.mock_cfg['monitor'][0])
        mock_factory.assert_any_call('TestNotifier1')
        mock_factory.assert_any_call('TestNotifier2')
        self.assertEqual(mock_factory.call_count, 2)
        mock_factory.reset_mock()

        get_notifiers(self.mock_cfg['monitor'][1])
        mock_factory.assert_called_once_with('TestNotifier3')
        mock_factory.reset_mock()

        get_notifiers(self.mock_cfg['monitor'][2])
        mock_factory.assert_called_once_with('TestNotifier4')
        mock_factory.reset_mock()

    @mock.patch('ipmonitor.main.get_parser')
    @mock.patch('ipmonitor.main.get_notifiers')
    @mock.patch('ipmonitor.monitor.Monitor')
    def test_get_monitor(self, mock_monitor, mock_notifiers, mock_parser):
        from ipmonitor.main import get_monitor
        get_monitor(self.mock_cfg['monitor'][0])
        mock_monitor.assert_called_once_with(mock_parser.return_value,
                                             mock_notifiers.return_value,
                                             None)
        mock_monitor.reset_mock()

        get_monitor(self.mock_cfg['monitor'][2])
        mock_monitor.assert_called_once_with(mock_parser.return_value,
                                             mock_notifiers.return_value,
                                             '1234')
        mock_monitor.reset_mock()
