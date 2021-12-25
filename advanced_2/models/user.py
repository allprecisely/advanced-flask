from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    jti = db.Column(db.String(36))

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @classmethod
    def get_user_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_user_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    def set_jti(self, jti: str) -> None:
        self.jti = jti
        db.session.commit()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
