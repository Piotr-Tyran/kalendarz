import os


class Config(object):
    SECRET_KEY = '1b4c194e40bf07cc616c4a86f28587ab'
    SQLALCHEMY_DATABASE_URI =\
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                    'todo.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'kalendarz.no.reply@gmail.com'
    MAIL_PASSWORD = 'Rafi4ever!'
    ADMINS = ['kalendarz.no.reply@gmail.com']
