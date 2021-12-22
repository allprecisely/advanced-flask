from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import User, UserLogin, UserRegister

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'ilnar'

api = Api(app)
api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(User, '/users/<string:name>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/stores/<string:name>')
api.add_resource(StoreList, '/stores')

jwt = JWTManager(app)


@jwt.additional_claims_loader
def jwt_claims(identity):
    return {'is_admin': identity == 1}


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run()
