import os


class Config(object):
    SECRET_KEY = '1b4c194e40bf07cc616c4a86f28587ab'
    SQLALCHEMY_DATABASE_URI =\
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                    'todo.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
