from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from website.models import *
from website.config import CurrenciesChoices

CurrenciesChoices=CurrenciesChoices()

class Home(FlaskForm):
    name = StringField('Name', validators=[Length(max=20)])
    ineed = SelectField('I Need', choices=CurrenciesChoices)
    submit = SubmitField('Search')

    
class MyApp(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])
    fb = StringField('Facebook Profile Link', validators=[DataRequired(), Length(min=8, max=30)])
    wa = StringField('WhatsApp', validators=[DataRequired(), Length(min=8, max=20)])
    needcurr = CurrenciesChoices
    offrcurr = CurrenciesChoices
    submit = SubmitField('Update')