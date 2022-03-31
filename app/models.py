from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Users(UserMixin, db.Model):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)
   # id_uzyt_wyd =  db.relationship('uzytkownik_wydarzenie', backref='uzytkownicy')

    def __repr__(self):
        return f'<{self.username}, {self.id_user}, {self.email}, {self.password}>'

    def set_password(self, haslo):
        self.password = generate_password_hash(haslo)

    def check_password(self, haslo):
        return check_password_hash(self.password, haslo)


@login.user_loader
def load_user(id_user):
    return Users.query.get(int(id_user))
