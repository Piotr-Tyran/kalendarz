from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Users(db.Model):

    __tablename__ = 'uzytkownicy'

    id_user = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)
   # id_uzyt_wyd =  db.relationship('uzytkownik_wydarzenie', backref='uzytkownicy')
    def __repr__(self):
        return f'<{self.username}, {self.id_user}, {self.email}, {self.password}>'




db.create_all()

user1 = Users(id_user=1, email='test@123.com', username='Test', password='1234')
user2 = Users(id_user=2, email='test1@123.com', username='Test1', password='1235')

#db.session.add(user1)
#db.session.add(user2)
#db.session.commit()
