from flask_jwt_extended import jwt_required
from flask_restful import Resource

from models.store import StoreModel
from schemas.store import StoreSchema

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):
    @classmethod
    @jwt_required()
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store), 200
        return {"message": f"Store {name} does not exist."}, 404

    @classmethod
    @jwt_required()
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return {"message": "Store with such name exists."}

        store = store_schema.load({"name": name})
        store.save_to_db()
        return store_schema.dump(store), 201

    @classmethod
    @jwt_required()
    def put(cls, name: str):
        store = store_schema.load({"name": name})
        store.save_to_db()
        return store_schema.dump(store), 201

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
        return {"stores": store_list_schema.dump(StoreModel.get_all_items())}, 200
