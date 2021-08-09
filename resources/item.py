from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True)

    @classmethod
    @jwt_required()
    def get(cls, name):
        item = ItemModel.find_an_item(name)
        if item:
            return {"item": item.to_json}, 200
        return {"message": "Item not found"}

    @jwt_required(fresh=True)
    def post(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_an_item(name)
        if item:
            return {"message": "Item already present"}
        item = ItemModel(name, data["price"])
        item.add_update_item()
        return {"item": item.to_json}, 200

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, name):
        item = ItemModel.find_an_item(name)
        if item:
            item.delete_item()
            return {"message": "Item deleted successfully"}
        return {"message": "Item not present"}

    @jwt_required(fresh=True)
    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_an_item(name)
        if item:
            item.price = data["price"]
        else:
            item = ItemModel(name, data["price"])
        item.add_update_item()


class ItemList(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        items = [item.to_json for item in ItemModel.get_all_items()]
        user_id = get_jwt_identity()
        if items:
            return {"items": items if user_id else [item["name"] for item in items]}
        return {"message": "No items present"}
