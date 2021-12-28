from flask import request, url_for
import requests

from db import db
from libs.mailgun import send_email as mailgun_send_email
from models.confirmation import ConfirmationModel


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    jti = db.Column(db.String(36))

    confirmation = db.relationship(
        "ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan"
    )

    @classmethod
    def get_user_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_user_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(username=email).first()

    @property
    def most_recent_confirmation(self):
        return self.confirmation.order_by(db.desc(ConfirmationModel.expired_at)).first()

    @property
    def activated(self):
        return self.most_recent_confirmation.confirmed

    def send_email(self) -> requests.Response:
        confirmation = ConfirmationModel(user_id=self.id)
        confirmation.save_to_db()
        link = request.url_root[:-1] + url_for(
            "confirmation", confirmation_id=confirmation.id
        )
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
