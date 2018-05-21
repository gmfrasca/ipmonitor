from ipmonitor.parsers.base import BaseParser
from ipmonitor.parsers.ipify import Ipify
from ipmonitor.parsers.parser_factory import ParserFactory
import unittest
import mock


class TestBaseParser(unittest.TestCase):

    def setUp(self):
        self.parser = BaseParser()

    def tearDown(self):
        pass

    def test_get_ip(self):
        self.assertRaises(NotImplementedError, self.parser.get_ip)


class TestIpify(unittest.TestCase):

    class MockIpifyResponse(object):
        text = '1.2.3.4'

    def setUp(self):
        self.ipify = Ipify()

    def tearDown(self):
        pass

    @mock.patch('ipmonitor.parsers.ipify.get')
    def test_get_ip(self, mock_get):
        mock_get.return_value = TestIpify.MockIpifyResponse()
        self.assertEqual(self.ipify.get_ip(), '1.2.3.4')

    def test_url(self):
        self.assertTrue('ipify' in self.ipify.URL)
        

class TestParserFactory(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_ipify(self):
        parser = ParserFactory.create('ipify')
        self.assertEqual(type(parser), Ipify)   

        parser = ParserFactory.create('ipify', 'extraarg')
        self.assertEqual(type(parser), Ipify)   

        parser = ParserFactory.create('ipify', extrakwarg='test')
        self.assertEqual(type(parser), Ipify)   

        parser = ParserFactory.create('ipify', 'extraarg', extrakwarg='test')
        self.assertEqual(type(parser), Ipify)   

    def test_create_bad_parser(self):
        self.assertRaises(RuntimeError, ParserFactory.create, 'FooBarFakeParser')
