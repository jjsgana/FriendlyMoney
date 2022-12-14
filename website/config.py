import os

class Config:
    # secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # #db sqllite uri
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    #db mysql uri
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_HOST = 'containers-us-west-32.railway.app'
    MYSQL_DB = 'railway'
    MYSQL_PORT = '7716'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + MYSQL_USER + ':' + MYSQL_PASSWORD + '@' + MYSQL_HOST + ':' + MYSQL_PORT + '/' + MYSQL_DB
    
    
    # email sender
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME ='friendlymoneyapp@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # time_able_rank_again (in hours)
    TIME_ABLE_RANK_AGAIN = int(os.environ.get('TIME_ABLE_RANK_AGAIN'))


def CurrenciesChoices():
    CurrenciesChoices=[ ('NZD'), ('AUD'), ('CLP') ]
    return CurrenciesChoices

def RateChoices():
    RateChoices=[ ('Positive'), ('Negative') ]
    return RateChoices