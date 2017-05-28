from database import db
from tools.modelmixin import ModelMixin


class User(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    tasks = db.relationship("Task", backref="user")

    def __init__(self, **kwargs):
        self.username = kwargs["username"]
        self.password = kwargs["password"]
        self.email = kwargs["email"]

    def __repr__(self):
        return "User id: {id}, username: {username}".format(id=self.id, username=self.username)

    def for_user(self):
        return {key: self[key] for key in dict(self) if key not in "password"}
