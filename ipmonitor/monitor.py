from time import sleep
import threading


# Ten Minutes
DEFAULT_SLEEP = 600


class Monitor(threading.Thread):

    def __init__(self, parser, notifier_list, sleep_time=DEFAULT_SLEEP):
        sleep_time = sleep_time if sleep_time else DEFAULT_SLEEP

        super(Monitor, self).__init__()
        self.parser = parser
        self.notifiers = notifier_list
        self.sleep_time = sleep_time
        self.daemon = True
        self.ip = self.parser.get_ip()  # Dont want to notify on start-up

    def send_notifications(self, old_ip, new_ip):
        for notifier in self.notifiers:
            notifier.notify(old_ip, new_ip)

    def monitor(self):
        sleep(self.sleep_time)
        new_ip = self.parser.get_ip()
        if new_ip != self.ip:
            self.send_notifications(self.ip, new_ip)
            self.ip = new_ip

    def run(self):
        try:
            while True:
                self.monitor()
        except KeyboardInterrupt:
            pass
