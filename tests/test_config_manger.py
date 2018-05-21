from ipmonitor.config_manager import ConfigManager
import unittest
import mock


class TestConfigManager(unittest.TestCase):

    MOCK_YAML = '''
monitors:
    - parser: ipify
      notifiers:
        - name: stdout
'''

    def setUp(self):
        with mock.patch('__builtin__.open',
                        mock.mock_open(read_data=self.MOCK_YAML)):
            assert open('/fake/config.yaml').read() == self.MOCK_YAML
            self.cfg_mgr = ConfigManager()

    def tearDown(self):
        pass

    def test_load_config(self):
        expected = {
            'monitors': [
                {
                     'parser': 'ipify',
                     'notifiers': [{'name': 'stdout'}]
                 }
            ]
        }
        self.assertEqual(expected, self.cfg_mgr.cfg)

    def test_get_monitors(self):
        expected = [dict(parser='ipify', notifiers=[dict(name='stdout')])]
        actual = self.cfg_mgr.get_monitors()
        self.assertTrue(isinstance(actual, list))
        self.assertEqual(expected, actual)
