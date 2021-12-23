from hmac import compare_digest

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jti,
    get_jwt,
    get_jwt_identity,
)
from flask_restful import Resource, reqparse

from db import jwt_redis_blocklist, ACCESS_EXPIRES
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "username", type=str, required=True, help="username should be defined"
)
_user_parser.add_argument(
    "password", type=str, required=True, help="password should be defined"
)


class UserRegister(Resource):
    @staticmethod
    def post():
        data = _user_parser.parse_args()
        if UserModel.get_user_by_username(data["username"]):
            return {"message": "User with such username is already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User successfully created."}, 201


class User(Resource):
    @staticmethod
    @jwt_required()
    def get(name):
        user = UserModel.get_user_by_username(name)
        if user:
            return user.json()
        return {"message": "User with such name doesn't exist"}, 404

    @staticmethod
    @jwt_required(fresh=True)
    def delete(name):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message": "You don't have enough power to do this"}

        user = UserModel.get_user_by_username(name)
        if user:
            if user.jti:
                jwt_redis_blocklist.set(user.jti, "", ex=ACCESS_EXPIRES)
            user.delete_from_db()
            return {"message": "User deleted."}, 200
        return {"message": "User with such name doesn't exist"}, 404


class UserLogin(Resource):
    @staticmethod
    def post():
        data = _user_parser.parse_args()

        user = UserModel.get_user_by_username(data["username"])

        if user and compare_digest(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            user.set_jti(get_jti(access_token))
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        return {"message": "Invalid authentication."}, 401


class UserLogout(Resource):
    @staticmethod
    @jwt_required()
    def post():
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        return {"message": "User has logged out."}


class TokenRefresh(Resource):
    @staticmethod
    @jwt_required(refresh=True)
    def post():
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {"access_token": access_token}, 200
