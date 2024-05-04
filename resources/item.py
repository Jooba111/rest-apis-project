from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from db import db
import models

from models import ItemModel

from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    # @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401 ,"Admin privilege required!")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}
    
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    
    
    @jwt_required(fresh = True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        
        return item














# import uuid
# from flask import request
# from flask.views import MethodView
# from flask_smorest import Blueprint, abort
# from schemas import ItemSchema, ItemUpdateSchema

# from db import items

# blp = Blueprint("Items", __name__, description="Operations on items")


# @blp.route("/item/<string:item_id>")
# class Item(MethodView):
#     def get(self, item_id):
#         try:
#             return items[item_id]
#         except KeyError:
#             abort(404, message="Item not found.")

#     def delete(self, item_id):
#         try:
#             del items[item_id]
#             return {"message": "Item deleted."}
#         except KeyError:
#             abort(404, message="Item not found.")

#     # def put(self, item_id):
#     #     item_data = request.get_json()
#     #     # There's  more validation to do here!
#     #     # Like making sure price is a number, and also both items are optional
#     #     # Difficult to do with an if statement...
#     #     if "price" not in item_data or "name" not in item_data:
#     #         abort(
#     #             400,
#     #             message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
#     #         )
    
#     @blp.arguments(ItemUpdateSchema)
#     @blp.response(200, ItemUpdateSchema)
#     def put(self, item_data, item_id):
#         try:
#             item = items[item_id]

#             # https://blog.teclado.com/python-dictionary-merge-update-operators/
#             item |= item_data

#             return item
#         except KeyError:
#             abort(404, message="Item not found.")


# @blp.route("/item")
# @blp.response(200, ItemSchema(many=True))
# class ItemList(MethodView):
#     def get(self):
#         return {"items": list(items.values())}

#     # def post(self):
#     #     item_data = request.get_json()
#     #     # Here not only we need to validate data exists,
#     #     # But also what type of data. Price should be a float,
#     #     # for example.
#     #     if (
#     #         "price" not in item_data
#     #         or "store_id" not in item_data
#     #         or "name" not in item_data
#     #     ):
#     #         abort(
#     #             400,
#     #             message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
#     #         )
    
#     @blp.arguments(ItemSchema)
#     @blp.response(201, ItemSchema)
#     def post(self, item_data):
#         for item in items.values():
#             if (
#                 item_data["name"] == item["name"]
#                 and item_data["store_id"] == item["store_id"]
#             ):
#                 abort(400, message=f"Item already exists.")

#         item_id = uuid.uuid4().hex
#         item = {**item_data, "id": item_id}
#         items[item_id] = item

#         return item