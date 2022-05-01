from flask_mail import Message, Mail
from threading import Thread
from app.models import Reminders, Users_Events, Users, Events
from datetime import datetime
from time import sleep
from app import app
from flask import render_template


class Async:

    def __init__(self):
        self.mail = Mail(app)
        Thread(target=self.reminder).start()

    def reminder(self):
        with app.app_context():
            while True:
                now = datetime.now().replace(second=0, microsecond=0)
                for reminder in Reminders.query.all():
                    user_event = Users_Events.query.filter_by(id=reminder.id_users_events).first()
                    event = Events.query.filter_by(id=user_event.events_id).first()

                    if event.start_date - reminder.rem_before == now:
                        user = Users.query.filter_by(id=user_event.users_id).first()
                        subject = f'{event.name}'
                        sender = app.config['ADMINS'][0]
                        recipients = [user.email]
                        text_body = render_template('email/reminder.txt',
                                                    user=user,
                                                    event=event,
                                                    reminder=reminder)
                        html_body = render_template('email/reminder.html',
                                                    user=user,
                                                    event=event,
                                                    reminder=reminder)
                        self.send_email(subject=subject,
                                        sender=sender,
                                        recipients=recipients,
                                        text_body=text_body,
                                        html_body=html_body)
                sleep(60 - datetime.now().second)

    def async_mail(self, message):
        with app.app_context():
            self.mail.send(message)

    def send_email(self, subject, sender, recipients, text_body, html_body):
        message = Message(subject, sender=sender, recipients=recipients)
        message.body = text_body
        message.html = html_body
        Thread(target=self.async_mail, args=(message,)).start()
