'''Helper module tha helps sends mail asynchronously'''
from threading import Thread

from flask import current_app as app
from flask_mail import Message

from app import mail

def send_async_email(app, msg):
    print(app)
    with app.app_context():
        mail.send(msg)

def send_email(sender, recipient, subject, body, html=None, attachment=None):
    msg = Message(subject=subject, 
            sender=sender,
            body=body,
            recipients=recipient if type(recipient) == str else[recipient])
    msg.html = html if html else None
    if attachment:
        with app.open_resource(attachment) as fp:
            msg.attach(attachment, "application/pdf", fp.read())
    # Thread(target=send_async_email, args=(app, msg)).start()