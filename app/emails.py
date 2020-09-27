'''Helper module tha helps sends mail asynchronously'''
from threading import Thread
from app import mail
from flask_mail import Message

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(sender, recipient, subject, body, **kwargs):
    '''Helper function that '''
    try:
        msg = Message(subject=subject, 
                sender=sender,
                body=body,
                recipients=[recipient.email])
        msg.html = html if html else None
        if attachment:
            with app.open_resource(attachment) as fp:
                msg.attach(attachment, "application/pdf", fp.read())
        Thread(target=send_async_email, args=(app, msg)).start()
    except Exception as e:
        return {
            'error': 'Something went wrong',
            'message': e
        }