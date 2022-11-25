from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea
from website.models import *
from website.config import CurrenciesChoices, RateChoices


CurrenciesChoices=CurrenciesChoices()
RateChoices=RateChoices()

class ProfileInfo_1(FlaskForm):
    seeuser = SubmitField('See')
    details = SubmitField('I want to contact this user')

class ProfileInfo_2(FlaskForm):
    rate = SubmitField('I want to rate this user')

class RateUser(FlaskForm):
    positive_or_negative = SelectField('Transaction was', choices=RateChoices)
    user_giving_rate_curr = SelectField('This Person payed me in', choices=CurrenciesChoices)
    user_receving_rate_curr = SelectField('I payed to this person in', choices=CurrenciesChoices)
    comments = StringField('Comments', widget=TextArea(), validators=[DataRequired(), Length(min=5, max=50)])
    rateperson = SubmitField('Rate This User')
