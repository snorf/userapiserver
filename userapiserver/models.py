import datetime
from database import db
from resources.auth import get_hashed_password

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(10))
    registered_on = db.Column(db.DateTime)
    requests = db.relationship('Request', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = get_hashed_password(password)
        self.registered_on = datetime.datetime.utcnow()

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            'user_id': self.id,
            'username': self.username,
            'password': self.password,
            'registered_on': self.registered_on
        }


class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column('request_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    access_date = db.Column(db.DateTime)

    def __init__(self, user_id):
        self.user_id = user_id
        self.access_date = datetime.datetime.utcnow()

    def __repr__(self):
        return '<Request %r>' % self.id

    def __str__(self):
        return 'access_date: %s, user_id: %s' % (self.access_date, self.user_id)

    def serialize(self):
        return {
            'request_id': self.id,
            'user_id': self.user_id,
            'access_date': self.access_date
        }