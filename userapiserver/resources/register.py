from flask_restful import Resource, reqparse
from userapiserver.models import User

class Register(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username')
        parser.add_argument('password', type=str, help='Password')
        args = parser.parse_args(strict=True)
        username = args['username']
        password = args['password']
        if not (username and password):
            return 'Bad Request', 400
        user = User.query.filter_by(username=username).first()
        if user:
            return 'Conflict', 409
        else:
            user = User(username=username, password=password)
            self.db.session.add(user)
            self.db.session.commit()
            return 'Created', 201
