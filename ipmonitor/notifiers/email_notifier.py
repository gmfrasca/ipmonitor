from base import BaseNotifier
from email.mime.text import MIMEText
import smtplib


class EmailNotifier(BaseNotifier):

    SUBJECT = 'Public IP Change Discovered'

    def __init__(self, email, smtp_server, smtp_port, smtp_username,
                 smtp_password, *args, **kwargs):
        self.email = email
        self.server = smtp_server
        self.server_port = smtp_port
        self.user = smtp_username
        self.password = smtp_password

    def notify(self, old_ip, new_ip):
        msg_txt = self.NOTIFICATION_TEXT.format(old_ip, new_ip)
        msg = MIMEText(msg_txt)
        to = self.email

        # For now, just use self as from (email to self)
        msg['Subject'] = EmailNotifier.SUBJECT
        msg['From'] = to
        msg['To'] = to

        s = smtplib.SMTP(self.server, self.server_port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(self.user, self.password)
        s.sendmail(to, [to], msg.as_string())
        s.close()
