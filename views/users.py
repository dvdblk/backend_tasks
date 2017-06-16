from flask import Blueprint, jsonify, request
from tools import auth
from sqlalchemy.exc import IntegrityError
from database import db
from models.user import User


users = Blueprint("users", __name__)


@users.route("/")
def index():
    return jsonify(status="pong")


@users.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    data['password'] = auth.hash_password(data["password"])
    try:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return auth.get_token(user), 200
    except IntegrityError:
        return "Username or email already exists", 409


@users.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        return 'username does not exist', 401

    if user.password != auth.hash_password(data["password"], user.password):
        return "wrong password", 401

    return jsonify(user=user.for_user(), token=auth.get_token(user)), 200
