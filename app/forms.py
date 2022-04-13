from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Users


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
    start = DateField('Rozpoczęcie:', validators=[DataRequired()])
    stop = DateField('Zakończenie:', validators=[DataRequired()])
    submit = SubmitField('Utwórz wydarzenie')
    
class CalendarForm(FlaskForm):
    submit = SubmitField('Dodaj wydarzenie')
