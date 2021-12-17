from flask import Flask, request
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api, reqparse

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'ilnar'

api = Api(app)
jwt = JWT(app, authenticate, identity)

students = []


class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('book', type=str, required=True, help='Book cannot be blank!')

    @jwt_required()
    # curl -X POST -H "Content-Type: application/json" 127.0.0.1:5000/auth -d '{"username":"bob", "password": "asdf"}'
    # curl 127.0.0.1:5000/student/ilnar -H "Authorization: JWT token"
    def get(self, name):
        student = next(filter(lambda x: x['name'] == name, students), None)
        return {'student': student}, 200 if student else 401

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, students), None):
            return {'message': f'Student {name} is already exists.'}
        item = {'name': name, 'book': self.parser.parse_args()['book']}
        students.append(item)
        return item, 201


# curl -X POST -H "Content-Type: application/json" 127.0.0.1:5000/student/ilnar -d '{"book":"hello, world!"}'
api.add_resource(Student, '/student/<string:name>')

app.run()
