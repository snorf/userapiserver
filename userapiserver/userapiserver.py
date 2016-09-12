from flask import Flask
from database import db
from resources import Requests, Register, auth, api

app = Flask(__name__)
app.config.from_object('config')
auth.init_app(app)
api.add_resource(Requests, '/users/requests')
api.add_resource(Register, '/users/register', resource_class_kwargs={ 'db': db })
api.init_app(app)

def setup_database(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()