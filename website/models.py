from website import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Seralizer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    fb = db.Column(db.String(30))
    wa = db.Column(db.String(30))
    needcurr = db.Column(db.String(15))
    offrcurr = db.Column(db.String(15))
    register_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update_date = db.Column(db.DateTime)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    account_hidden = db.Column(db.Boolean, nullable=False, default=0)



    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.name}')"

# https://realpython.com/handling-email-confirmation-in-flask/
    def get_reset_token(self):
        serializer = Seralizer(current_app.config['SECRET_KEY'])
        return serializer.dumps({'user_id': self.id}, salt=current_app.config['SECRET_KEY'])

    @staticmethod        
    def verify_reset_token(token):
        serializer = Seralizer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(
                token,
                salt=current_app.config['SECRET_KEY'],
                max_age=1200
            )['user_id']
        except:
            return None
        return User.query.get(user_id)

class Rate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid_giving = db.Column(db.Integer,db.ForeignKey("user.id"), nullable=False)
    name_surname_giving = db.Column(db.String(62), nullable=False)
    rate = db.Column(db.String(8), nullable=False) #positive or negative
    userid_receiving = db.Column(db.Integer,db.ForeignKey("user.id"), nullable=False)
    name_surname_receving = db.Column(db.String(62), nullable=False)
    comments = db.Column(db.String(50), nullable=False)
    user_giving_rate_curr = db.Column(db.String(3), nullable=False)
    user_receving_rate_curr = db.Column(db.String(3), nullable=False)
    rate_date = db.Column(db.DateTime, default=datetime.utcnow)

    user_giving = db.relationship("User", foreign_keys=[userid_giving])
    user_receiving = db.relationship("User", foreign_keys=[userid_receiving])


    def __repr__(self):
        return f"User('{self.id}', '{self.userid_giving}', '{self.userid_receiving}', '{self.comments}')"