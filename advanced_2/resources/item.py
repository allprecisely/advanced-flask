from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource
from sqlalchemy import exc

from models.item import ItemModel
from schemas.item import ItemSchema

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    @classmethod
    @jwt_required()
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200
        return {"message": f"Item {name} does not exist."}, 404

    @classmethod
    @jwt_required()
    def post(cls, name: str):
        if ItemModel.find_by_name(name):
            return {"message": f"Item {name} already exists."}, 400

        item = item_schema.load({"name": name, **request.get_json()})

        try:
            item.save_to_db()
            return item_schema.dump(item), 201
        except exc.IntegrityError:
            return {"message": "Problems while saving object within db."}

    @classmethod
    @jwt_required()
    def put(cls, name: str):
        item_json = request.get_json()
        item = ItemModel.find_by_name(name)
        if item:
            # TODO: прокрался баг с отсутствием валидации тут
            if item_json.get("price"):
                item.price = item_json["price"]
            if item_json.get("store_id"):
                item.store_id = item_json["store_id"]
        else:
            item = item_schema.load({"name": name, **item_json})

        try:
            item.save_to_db()
            return item_schema.dump(item), 201
        except exc.IntegrityError:
            return {"message": "Probably store id is missing."}

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message": "You don't have enough power to do this"}

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": f"Item deleted."}, 200


class ItemList(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        user_id = get_jwt_identity()
        items = item_list_schema.dump(ItemModel.get_all_items())
        if user_id:
            return {"items": items}, 200
        else:
            return {"items": [item["name"] for item in items]}, 200
