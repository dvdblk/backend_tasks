from app import create_app
from database import db
from tools import auth
from models.user import User


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(username="Arual",
                    password=auth.hash_password("root"),
                    email="zdenko.hives@gmail.com")
        db.session.add(user)
        db.session.commit()
