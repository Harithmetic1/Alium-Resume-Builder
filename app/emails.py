'''Helper module tha helps sends mail asynchronously'''

def send_email(sender, recipient, subject, body, **kwargs):
    '''Helper function that '''
    try:
        msg = Message(subject=subject, 
                sender=sender,
                body=body,
                recipients=[recipient.email])
        msg.html = html if html else None
        if attachments:
            for attachment in msg.attachment:
                msg.attachment = attachment
        mail.send(msg)
    except Exception as e:
        return {
            'error': 'Something went wrong',
            'message': e
        }