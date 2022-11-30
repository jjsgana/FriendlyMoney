from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from website.models import *
from website.config import CurrenciesChoices

CurrenciesChoices=CurrenciesChoices()

class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=10, max=50), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Register(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=50)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])
    needcurr = CurrenciesChoices
    offrcurr = CurrenciesChoices
    fb = StringField('Facebook Link', validators=[DataRequired(), Length(min=8, max=30)])
    wa = StringField('WhatsApp', validators=[DataRequired(), Length(min=8, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password'), Length(min=5, max=20)])
    submit = SubmitField('Create Account')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already exists')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password'), Length(min=5, max=20)])
    submit = SubmitField('Reset Password')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=50)])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('There is no account with that email. Please Register first')