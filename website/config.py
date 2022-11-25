import os

class Config:
    # secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')

    #db uri
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # email sender
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME ='friendlymoneyapp@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


def CurrenciesChoices():
    CurrenciesChoices=[ ('NZD'), ('AUD'), ('CLP') ]
    return CurrenciesChoices

def RateChoices():
    RateChoices=[ ('Positive'), ('Negative') ]
    return RateChoices