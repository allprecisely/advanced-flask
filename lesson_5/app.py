from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import authenticate, identity
from items import Items, ItemsList
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'ilnar'

api = Api(app)
jwt = JWT(app, authenticate, identity)

api.add_resource(Items, '/items/<string:name>')
api.add_resource(ItemsList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run()
