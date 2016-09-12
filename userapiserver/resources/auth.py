import bcrypt
from extensions import jwt

@jwt.authentication_handler
def authenticate(username, password):
    from userapiserver.database import db
    from userapiserver.models import User
    from userapiserver.models import Request
    user = User.query.filter_by(username=username).first()
    if user and check_password(password, user.password.encode('utf-8')):
        req = Request(user.id)
        db.session.add(req)
        db.session.commit()
        return user
    else:
        return None

@jwt.identity_handler
def identity(payload):
    from userapiserver.models import User
    user_id = payload['identity']
    user = User.query.filter_by(id=user_id).first()
    if user:
        return user
    else:
        return None, 401

# Password
def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    # Check hased password. Useing bcrypt, the salt is saved into the hash itself
    return bcrypt.hashpw(plain_text_password, hashed_password) == hashed_password
