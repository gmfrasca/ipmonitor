class BaseNotifier(object):

    NOTIFICATION_TEXT = "Public IP has Changed from {0} to {1}!"

    def __init__(self, *args, **kwargs):
        pass

    def notify(self, old_ip, new_ip):
        raise NotImplementedError
