import sqlite3

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price cannot be blank!')

    @jwt_required()
    def get(self, name):
        data = self.find_by_name(name)
        if data:
            return data, 200
        return {'message': f'Item {name} does not exist.'}

    @staticmethod
    def find_by_name(name):
        with sqlite3.connect('data.db') as con:
            cursor = con.cursor()

            query = 'SELECT * FROM items WHERE name = ?'
            cursor.execute(query, (name,))
            return cursor.fetchone()

    @jwt_required()
    def post(self, name):
        data = self.parser.parse_args()
        if self.find_by_name(name):
            return {'message': f'Item {name} already exists.'}

        with sqlite3.connect('data.db') as con:
            cursor = con.cursor()

            query = 'INSERT INTO items VALUES (NULL, ?, ?)'
            cursor.execute(query, (name, data['price']))
            con.commit()
            return {'name': name, 'price': data['price']}, 201


class ItemsList(Resource):
    def get(self):
        with sqlite3.connect('data.db') as con:
            cursor = con.cursor()

            cursor.execute('SELECT * FROM items')
            return cursor.fetchall(), 200
