from database import db
from tools.modelmixin import ModelMixin


class Task(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(128), nullable=False)
    body = db.Column(db.String(512), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, **kwargs):
        self.topic = kwargs["topic"]
        self.body = kwargs["body"]
        self.user = kwargs["user"]

    def __repr__(self):
        return "Task id: {id}, topic: {topic}".format(id=self.id, topic=self.topic)

    @property
    def for_task(self):
        return {key: self[key] for key in dict(self)}
