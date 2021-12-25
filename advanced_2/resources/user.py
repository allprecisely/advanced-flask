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
from marshmallow import ValidationError

from db import jwt_redis_blocklist, ACCESS_EXPIRES
from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        try:
            data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        if UserModel.get_user_by_username(data["username"]):
            return {"message": "User with such username is already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User successfully created."}, 201


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
            return {"message": "You don't have enough power to do this"}

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
        try:
            data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

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
