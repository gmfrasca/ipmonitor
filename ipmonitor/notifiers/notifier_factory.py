from stdout_notifier import StdoutNotifier
from email_notifier import EmailNotifier
from groupme_notifier import GroupmeNotifier


class NotifierFactory(object):

    _cls = dict(stdout=StdoutNotifier, email=EmailNotifier,
                groupme=GroupmeNotifier)

    @classmethod
    def create(cls, notifier_type, *args, **kwargs):
        try:
            return cls._cls[notifier_type](*args, **kwargs)
        except KeyError:
            raise RuntimeError("{} is not a supported notifier: {}".format(
                               notifier_type, cls._cls.keys()))
