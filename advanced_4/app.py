import os

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from marshmallow import ValidationError

from resources.confirmation import Confirmation, ResendConfirmation
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import (
    User,
    UserLogin,
    UserLogout,
    UserRegister,
    TokenRefresh,
)

app = Flask(__name__)
# https://stackoverflow.com/questions/66690321
database_url = os.getenv("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url.replace(
    "postgres://", "postgresql://", 1
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = os.getenv('APP_SECRET_KEY')

api = Api(app)
api.add_resource(Item, "/items/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(User, "/users/<string:name>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserRegister, "/register")
api.add_resource(Confirmation, "/confirm/<string:confirmation_id>")
api.add_resource(ResendConfirmation, "/resend_confirm/<string:name>")
api.add_resource(Store, "/stores/<string:name>")
api.add_resource(StoreList, "/stores")

jwt = JWTManager(app)


@jwt.additional_claims_loader
def jwt_claims(identity):
    return {"is_admin": identity == 1}


@app.errorhandler(ValidationError)
def handle_marshmallow_error(err):
    return jsonify(err.messages), 400
