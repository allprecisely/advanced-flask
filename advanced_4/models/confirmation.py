from time import time
from uuid import uuid4

from db import db

TIME_DELTA = 30 * 60  # 30min
TIME_DELTA_FOR_RESEND = 2 * 60  # 2min


class ConfirmationModel(db.Model):
    __tablename__ = 'confirmations'

    id = db.Column(db.String(20), primary_key=True)
    expired_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.expired_at = time() + TIME_DELTA
        self.id = uuid4().hex

    @property
    def expired(self) -> bool:
        return time() > self.expired_at

    @property
    def wait_to_resend(self) -> int:
        time_passed = time() - (self.expired_at - TIME_DELTA)
        return max(0, int(TIME_DELTA_FOR_RESEND - time_passed))

    @classmethod
    def get_confirmation_by_id(cls, id) -> "ConfirmationModel":
        return cls.query.filter_by(id=id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
