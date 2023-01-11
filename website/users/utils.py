from flask_mail import Message
from website import mail
from flask import url_for
from flask_login import current_user
from flask import flash

def block_page_when_user_is_hidden(userinfo, user_id):
    if userinfo.account_hidden and user_id == current_user.id:
        #flash('account hidden, but same user logged in, good', 'info')
        return 'allowed'
    elif userinfo.account_hidden:
        flash('Account hidden, not possible to see', 'danger')
        return 'blocked'

def send_notification_when_rating(giving_rate_user, receving_rate_user):
    user_giving_rate_name = giving_rate_user.name
    user_giving_rate_surn = giving_rate_user.surname
    user_giving_rate_id = giving_rate_user.id
    user_receiving_rate_name = receving_rate_user.name
    user_receiving_rate_surn = receving_rate_user.surname
    user_receiving_rate_id = receving_rate_user.id

    msg = Message(f' {user_giving_rate_name} {user_giving_rate_surn} rated you !', sender= 'noreply@friendlymoneyapp.com', recipients=[receving_rate_user.email])
    msg.body = f'''Hi {user_receiving_rate_name} {user_receiving_rate_surn},

User {user_giving_rate_name} {user_giving_rate_surn} rated you in the app.

If you have already rated {user_giving_rate_name} {user_giving_rate_surn}, please discard the mail.

Rate {user_giving_rate_name} {user_giving_rate_surn} now going here:

{url_for('users.rate', user_id=user_giving_rate_id, _external=True)}

See comments that {user_giving_rate_name} {user_giving_rate_surn} gave you going here:

{url_for('users.profileinfo_1', user_id=user_receiving_rate_id, _external=True)}

Friendly Money Team.
'''
    mail.send(msg)

     