from base import BaseNotifier
from requests import post


GROUPME_BOT_URL = 'https://api.groupme.com/v3/bots/post'


class GroupmeNotifier(BaseNotifier):

    def __init__(self, bot_id, *args, **kwargs):
        self.bot_id = bot_id

    def notify(self, old_ip, new_ip):
        msg_txt = self.NOTIFICATION_TEXT.format(old_ip, new_ip)
        data = dict(bot_id=self.bot_id, text=msg_txt)
        resp = post(GROUPME_BOT_URL, data=data)
        assert resp.status_code in range(200, 400)
