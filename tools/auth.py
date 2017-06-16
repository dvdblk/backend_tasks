from functools import wraps

from flask import current_app, request
import bcrypt
import jwt
from datetime import datetime, timedelta

from models.user import User


def hash_password(password, hashed=None):
    salt = (hashed if not hashed else hashed.encode("utf-8")) or bcrypt.gensalt(14)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def get_token(user):
    """creates a token for the given user with 10 hours duration"""
    return jwt.encode(
        # issuer
        {"iss": current_app.config["JWT_ISS"],
         # subject
         "sub": user.id,
         # issued at
         "iat": datetime.utcnow(),
         # expires
         "exp": datetime.utcnow() + timedelta(hours=10)
         }, current_app.config["SECRET_KEY"]).decode("utf-8")

def decode_token(token):
    return jwt.decode(token, current_app.config["SECRET_KEY"])

def authorize(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        token = request.headers.get("token")
        if not token:
            return "You are not logged in", 401

        token = decode_token(token)
        user = User.query.get(token["sub"])
        return function(user, *args, **kwargs)

    return decorated
