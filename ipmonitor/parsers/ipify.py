from requests import get
from requests.exceptions import ConnectionError
from base import BaseParser


class Ipify(BaseParser):

    URL = 'https://api.ipify.org'

    def get_ip(self):
        try:
            return get(self.URL).text
        except ConnectionError:
            return 'ConnectionError'
