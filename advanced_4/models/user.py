from flask import request, url_for
import requests

from db import db
from libs.mailgun import send_email as mailgun_send_email


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    jti = db.Column(db.String(36))
    activated = db.Column(db.Boolean, default=False)

    @classmethod
    def get_user_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_user_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(username=email).first()

    def send_email(self) -> requests.Response:
        link = request.url_root[:-1] + url_for("userconfirm", name=self.username)
        return mailgun_send_email(
            self.email, "Hello", f"Testing some Mailgun awesomness! {link}"
        )

    def set_jti(self, jti: str) -> None:
        self.jti = jti
        db.session.commit()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
