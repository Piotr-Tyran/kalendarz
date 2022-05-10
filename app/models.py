from app import db, login
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class Users(UserMixin, db.Model):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    id_users_events = db.relationship('Users_Events', backref='Users')
    
    def __repr__(self):
        return f'<{self.username}, {self.id}, {self.email}, {self.password}>'

    def set_password(self, haslo):
        self.password = generate_password_hash(haslo)

    def check_password(self, haslo):
        return check_password_hash(self.password, haslo)
    
    
class Events(UserMixin, db.Model):

    __tablename__ = 'Events'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    stop_date = db.Column(db.DateTime, nullable=False)
    types = db.Column(db.Integer, nullable=False)
    id_users_events = db.relationship('Users_Events', backref='Events')
    
    def __repr__(self):
        return f'<{self.name}, {self.id}, {self.start_date}, {self.stop_date}, {self.types}, {self.id_users_events}>'
    

class Tags(UserMixin, db.Model):

    __tablename__ = 'Tags'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tags = db.Column(db.String(50), nullable=False)
    id_users_events = db.Column(db.Integer, db.ForeignKey('Users_Events.id'))
    
    
    def __repr__(self):
        return f'<{self.tags}, {self.id}, {self.id_users_events}>'


class Reminders(UserMixin, db.Model):

    __tablename__ = 'Reminders'

    id = db.Column(db.Integer, primary_key=True)
    rem_before = db.Column(db.Interval, nullable=False)
    id_users_events = db.Column(db.Integer, db.ForeignKey('Users_Events.id'))
    
    def __repr__(self):
        return f'<{self.rem_before}, {self.id}, {self.id_users_events}>'

    
class Users_Events(UserMixin, db.Model):

    __tablename__ = 'Users_Events'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    owner = db.Column(db.Boolean, nullable=False)
    finish = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    aprove = db.Column(db.Boolean)
    users_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    events_id = db.Column(db.Integer, db.ForeignKey('Events.id'))
    tags_id = db.relationship('Tags', backref='Users_Events')
    reminders_id = db.relationship('Reminders', backref='Users_Events')
    
    def __repr__(self):
        return f'<{self.owner}, {self.id}, {self.finish}, {self.description}, {self.aprove}, {self.users_id}, {self.events_id}, {self.tags_id}, {self.reminders_id} >'


class Regular_Events(UserMixin, db.Model):

    __tablename__ = 'Regular_Events'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    daily = db.Column(db.Boolean, nullable=False, default=False)
    weekly = db.Column(db.Boolean, nullable=False, default=False)
    monthly = db.Column(db.Boolean, nullable=False, default=False)
    yearly = db.Column(db.Boolean, nullable=False, default=False)
    events_id = db.Column(db.Integer, db.ForeignKey('Events.id'))

    def __repr__(self):
        return f'<id:{self.id}, daily:{self.daily}, weekly:{self.weekly} ' \
               f'monthly:{self.monthly}, yearly:{self.yearly}, ' \
               f'event_id:{self.events_id}'


@login.user_loader
def load_user(id_user):
    return Users.query.get(int(id_user))
