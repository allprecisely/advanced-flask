from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='price cannot be blank!')
    parser.add_argument('store_id', type=int, required=True, help='store_id cannot be blank!')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': f'Item {name} does not exist.'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'Item {name} already exists.'}, 400

        data = self.parser.parse_args()

        item = ItemModel(name, **data)
        item.save_to_db()
        return item.json()

    @jwt_required()
    def put(self, name):
        data = self.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item:
            item.price, item.store_id = data['price'], data['store_id']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()
        return item.json()

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': f'Item deleted.'}, 200


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.get_all_items()]}, 200
