from flask import Flask
from database import db
from views.users import users
from views.tasks import tasks


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    app.register_blueprint(users)
    app.register_blueprint(tasks)
    db.init_app(app)
    return app


if __name__ == "__main__":
    create_app().run(port=1337)
