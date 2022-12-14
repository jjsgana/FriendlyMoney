from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from website.config import Config
import os
from os import path
import mysql.connector

db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from website.main.routes import main
    from website.auth.routes import auth
    from website.users.routes import users
    from website.errors.handlers import errors

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(errors, url_prefix='/')


    mydb = mysql.connector.connect(
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    host=Config.MYSQL_HOST,
    db=Config.MYSQL_DB,
    port=Config.MYSQL_PORT,
    )
    
    my_cursor = mydb.cursor()
    my_cursor.execute("CREATE DATABASE IF NOT EXISTS railway")

    with app.app_context():
        db.create_all()

    return app



