import traceback
from hmac import compare_digest

from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jti,
    get_jwt,
    get_jwt_identity,
)
from flask_restful import Resource

from db import jwt_redis_blocklist, ACCESS_EXPIRES
from libs.mailgun import MailgunError
from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())

        if UserModel.get_user_by_username(user.username):
            return {"message": "User with such username is already exists"}, 400

        if UserModel.get_user_by_email(user.email):
            return {"message": "User with such email is already exists"}, 400

        try:
            user.save_to_db()
            if user.id != 1:
                user.send_email()
            return {"message": "User successfully created."}, 201
        except MailgunError as e:
            user.delete_from_db()
            return {'message': str(e)}, 500
        except:
            user.delete_from_db()
            traceback.print_exc()
            return {"message": "Some problems with sending email. Check logs."}, 500


class User(Resource):
    @classmethod
    @jwt_required()
    def get(cls, name: str):
        user = UserModel.get_user_by_username(name)
        if user:
            return user_schema.dump(user)
        return {"message": "User with such name doesn't exist"}, 404

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, name: str):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message": "You don't have enough power to do this"}, 400

        user = UserModel.get_user_by_username(name)
        if user:
            if user.jti:
                jwt_redis_blocklist.set(user.jti, "", ex=ACCESS_EXPIRES)
            user.delete_from_db()
            return {"message": "User deleted."}, 200
        return {"message": "User with such name doesn't exist"}, 404


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = user_schema.load(request.get_json(), partial=('email',))

        user = UserModel.get_user_by_username(data.username)
        if user and compare_digest(user.password, data.password):
            if user.id != 1 and not user.activated:
                return {'message': 'User is not activated.'}, 400
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            user.set_jti(get_jti(access_token))
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        return {"message": "Invalid authentication."}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        return {"message": "User has logged out."}


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {"access_token": access_token}, 200
