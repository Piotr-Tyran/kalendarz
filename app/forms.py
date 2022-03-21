from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Użytkownik: ', validators=[DataRequired()])
    password = PasswordField('Hasło: ', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')
