from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='username should be defined')
    parser.add_argument('password', type=str, required=True, help='password should be defined')

    def post(self):
        data = self.parser.parse_args()
        if UserModel.get_user_by_username(data['username']):
            return {'message': 'User with such username is already exists'}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()
        return {'message': 'User successfully created.'}, 201
