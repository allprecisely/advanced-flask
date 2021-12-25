from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):
    @classmethod
    @jwt_required()
    def get(cls, name: str):
        item = StoreModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"message": f"Item {name} does not exist."}, 404

    @classmethod
    @jwt_required()
    def post(cls, name: str):
        item = StoreModel(name)
        item.save_to_db()
        return item.json()

    @classmethod
    @jwt_required()
    def put(cls, name: str):
        item = StoreModel(name)
        item.save_to_db()
        return item.json()

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        item = StoreModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": f"Item deleted."}, 200


class StoreList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        return {"stores": [item.json() for item in StoreModel.get_all_items()]}, 200
