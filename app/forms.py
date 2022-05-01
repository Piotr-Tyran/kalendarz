from flask_wtf import FlaskForm
import flask_wtf
from wtforms import StringField, PasswordField, SubmitField, SelectField,\
    IntegerField, BooleanField, FieldList, Form, FormField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, ValidationError, Email,\
    EqualTo, NumberRange
from app.models import Users
from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField('Użytkownik:', validators=[DataRequired()])
    password = PasswordField('Hasło:', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')


class RegistrationForm(FlaskForm):
    username = StringField('Użytkownik:', validators=[DataRequired()])
    email = StringField('Adres email:', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło:', validators=[DataRequired()])
    password_repeat = PasswordField(
        'Powtórz hasło:', validators=[DataRequired(),
                                      EqualTo('password',
                                              message='Hasła muszą się zgadzać.')])
    submit = SubmitField('Zarejestruj się')

    def validate_username(self, username):
        if Users.query.filter_by(username=username.data).first() is not None:
            raise ValidationError('Nazwa użytkownika jest zajęta.')

    def validate_email(self, email):
        if Users.query.filter_by(email=email.data).first() is not None:
            raise ValidationError('Adres email jest już zajęty.')


class EntryForm(Form):
    value = IntegerField('Ilość', validators=[NumberRange(min=0)])
    time = SelectField('Czas',
                       choices=[('week', 'tygodni'),
                                ('day', 'dni'),
                                ('hour', 'godzin'),
                                ('minute', 'minut')])
    delete = BooleanField('Usuń')


class AddEventForm(FlaskForm):
    name = StringField('Wydarzenie:', default='')
    start = DateField('Rozpoczęcie:', default=datetime.today(),
                      validators=[DataRequired()])
    stop = DateField('Zakończenie:', default=datetime.today(),
                     validators=[DataRequired()])
    reminders = FieldList(FormField(EntryForm))
    submit = SubmitField('Utwórz wydarzenie')


class ViewEventForm(flask_wtf.FlaskForm):
    name = StringField('Wydarzenie:')
    start = DateField('Rozpoczęcie:', validators=[DataRequired()])
    stop = DateField('Zakończenie:', validators=[DataRequired()])
    reminders = FieldList(FormField(EntryForm))
    submit = SubmitField('Zmień wydarzenie')
