from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,\
    SelectMultipleField, widgets
from wtforms.fields import DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
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


class AddEventForm(FlaskForm):
    name = StringField('Wydarzenie:', default='')
    start = DateField('Rozpoczęcie:', default=datetime.today(),
                      validators=[DataRequired()])
    stop = DateField('Zakończenie:', default=datetime.today(),
                     validators=[DataRequired()])
    submit = SubmitField('Utwórz wydarzenie')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ViewEventForm(FlaskForm):
    name = StringField('Wydarzenie:')
    start = DateField('Rozpoczęcie:', validators=[DataRequired()])
    stop = DateField('Zakończenie:', validators=[DataRequired()])
    choices = MultiCheckboxField('Lista:', choices=[('week', 'tydzień,'),
                                                  ('day', 'dzień,'),
                                                  ('hour', 'godzinę,'),
                                                  ('15min', '15 minut,'),
                                                  ('5min', '5 minut')])
    submit = SubmitField('Zmień wydarzenie')
