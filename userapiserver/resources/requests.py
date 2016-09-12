import flask
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from userapiserver.models import Request

class Requests(Resource):
    @jwt_required()
    def get(self):
        last_five = Request.query.filter_by(user_id=current_identity.id).order_by(Request.access_date.desc()).limit(5).all()
        return flask.jsonify(last_five=[r.serialize() for r in last_five])