from flask_restful import Resource

from models.confirmation import ConfirmationModel
from models.user import UserModel


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        confirmation = ConfirmationModel.get_confirmation_by_id(confirmation_id)
        if not confirmation:
            return {"message": "Wrong link."}, 404

        if confirmation.confirmed:
            return {"message": "User has already been activated."}, 403

        if confirmation.expired:
            return {"message": "Confirmation link has expired. Request new one."}, 419

        confirmation.confirmed = True
        confirmation.save_to_db()

        return {"message": "User was activated."}


class ResendConfirmation(Resource):
    @classmethod
    def get(cls, name):
        user = UserModel.get_user_by_username(name)
        if not user:
            return {"message": "Not existed user"}, 404

        confirmation = user.most_recent_confirmation

        if confirmation.confirmed:
            return {"message": "User has already been activated."}, 403

        if confirmation.wait_to_resend:
            return {
                "message": (
                    "To resend confirmation link you should wait for "
                    f"{confirmation.wait_to_resend} seconds."
                )
            }, 403

        # confirmation.delete_from_db()
        user.send_email()

        return {"message": "Activation link was resend."}
