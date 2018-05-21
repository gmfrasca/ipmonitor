from __future__ import print_function
from base import BaseNotifier


class StdoutNotifier(BaseNotifier):

    def notify(self, old_ip, new_ip):
        print(self.NOTIFICATION_TEXT.format(old_ip, new_ip))
