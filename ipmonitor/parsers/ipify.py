from requests import get
from base import BaseParser


class Ipify(BaseParser):

    URL = 'https://api.ipify.org'

    def get_ip(self):
        return get(self.URL).text
