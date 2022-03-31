from app import db


class Users(db.Model):

    __tablename__ = 'uzytkownicy'

    id_user = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)
   # id_uzyt_wyd =  db.relationship('uzytkownik_wydarzenie', backref='uzytkownicy')

    def __repr__(self):
        return f'<{self.username}, {self.id_user}, {self.email}, {self.password}>'
