from parsers.parser_factory import ParserFactory
from notifiers.notifier_factory import NotifierFactory
from config_manager import ConfigManager
from monitor import Monitor
import signal


def get_parser(monitor_cfg):
    return ParserFactory.create(monitor_cfg.get('parser'))


def get_notifiers(monitor_cfg):
    notifiers = list()
    cfgs = monitor_cfg.get('notifiers', list())
    if isinstance(cfgs, basestring) or isinstance(cfgs, dict):
        cfgs = [cfgs]
    for notifier_cfg in cfgs:
        notifier_name = notifier_cfg
        notifier_kwargs = dict()
        if isinstance(notifier_cfg, dict):
            notifier_kwargs = notifier_cfg
            notifier_name = notifier_cfg.pop('name')
        notifiers.append(NotifierFactory.create(notifier_name,
                                                **notifier_kwargs))
    return notifiers


def get_monitor(monitor_cfg):
    sleep_time = monitor_cfg.get('sleep_time', None)
    parser = get_parser(monitor_cfg)
    notifiers = get_notifiers(monitor_cfg)
    return Monitor(parser, notifiers, sleep_time)


def main():
    for monitor_cfg in ConfigManager().get_monitors():
        get_monitor(monitor_cfg).start()

    try:
        while True:
            signal.pause()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
