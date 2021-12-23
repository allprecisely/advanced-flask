from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):
    @jwt_required()
    def get(self, name):
        item = StoreModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"message": f"Item {name} does not exist."}, 404

    @jwt_required()
    def post(self, name):
        item = StoreModel(name)
        item.save_to_db()
        return item.json()

    @jwt_required()
    def put(self, name):
        item = StoreModel(name)
        item.save_to_db()
        return item.json()

    @jwt_required()
    def delete(self, name):
        item = StoreModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": f"Item deleted."}, 200


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {"stores": [item.json() for item in StoreModel.get_all_items()]}, 200
