import dataclasses
import sqlite3

from flask_restful import Resource, reqparse


@dataclasses.dataclass
class User:
    id: int
    username: str
    password: str

    @classmethod
    def get_user_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        data = cursor.execute('SELECT * FROM users WHERE id = ?', (_id,))
        user = data.fetchone()
        result = cls(*user) if user else None

        connection.close()
        return result

    @classmethod
    def get_user_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        data = cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = data.fetchone()
        result = cls(*user) if user else None

        connection.close()
        return result


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='username should be defined')
    parser.add_argument('password', type=str, required=True, help='password should be defined')

    def post(self):
        data = self.parser.parse_args()

        if User.get_user_by_username(data['username']):
            return {'message': 'User with such username is already exists'}, 400

        with sqlite3.connect('data.db') as con:
            cursor = con.cursor()

            query = 'INSERT INTO users VALUES (NULL, ?, ?)'
            cursor.execute(query, (data['username'], data['password']))

            con.commit()

        return {'message': 'User successfully created.'}, 201
