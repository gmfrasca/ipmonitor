from ipify import Ipify


class ParserFactory(object):

    _cls = dict(ipify=Ipify)

    @classmethod
    def create(cls, parser_type, *args, **kwargs):
        try:
            return cls._cls[parser_type](*args, **kwargs)
        except KeyError:
            raise RuntimeError("{} is not a supported parser: {}".format(
                               parser_type, cls._cls.keys()))
