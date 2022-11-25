from flask_mail import Message
from website import mail
from flask import url_for

def send_resend_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender= 'noreply@friendlymoneyapp.com', recipients=[user.email])
    msg.body = f'''To reset your password, go here:

{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request, ignore this email

Friendly Money Team.
'''
    mail.send(msg)