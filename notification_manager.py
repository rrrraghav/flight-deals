import smtplib
import os


class NotificationManager:
    def __init__(self, message, email):
        self.message = message
        self.email = email

    def send_message(self):
        my_email = os.environ['EMAIL']
        email_password = os.environ['PASSWORD']
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=email_password)
            connection.sendmail(from_addr=my_email, to_addrs=self.email, msg=self.message)
