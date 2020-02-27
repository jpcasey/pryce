from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from pryce.database.models import Item, Price
from pryce.database.schemas import ItemSchema, PriceSchema
from pryce.database.dal.item import DALItem
from pryce.database.dal.price import DALPrice

bp = Blueprint('items', __name__, url_prefix='/items')
item_schema = ItemSchema()
price_schema = PriceSchema()
dalitem = DALItem()
dalprice = DALPrice()

# / - GET
# Returns a list of items in the system.  Can be filtered using query parameters (e.g. name, brand)
@bp.route('/', methods=['GET'])
def get_items():
    items = dalitem.get_items(request.args.get('name'), request.args.get('brand'))
    return item_schema.jsonify(items, many=True)

# /- POST
# Adds an item to the system.
@bp.route('/', methods=['POST'])
def add_item():
    if not request.is_json:
        return jsonify(message="Missing JSON in request"), 400

    try:
        item = item_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(message="Bad Request", validation_errors=err.messages), 400
        
    dalitem.add_item(item)
    return item_schema.jsonify(item)

# /<item_id> - GET
# Returns information for a specific item.
@bp.route('/<code>', methods=['GET'])
def get_item(code):
    item = dalitem.get_item(code)
    if item == None:
        return jsonify(message='Item not found'), 404
    return item_schema.jsonify(item)

# /<item_id> - PUT
# Update information for a specific item.
@bp.route('/<code>', methods=['PUT'])
def update_item(code):
    json_dict = request.get_json()
    item = dalitem.update_item(json_dict)
    if item is None:
        return jsonify(message='Item not found'), 404
    return item_schema.jsonify(item)

# /<item_id> - DELETE
# Deletes an item from the system.
@bp.route('/<code>', methods=['DELETE'])
def delete_item(code):
    row_cnt = dalitem.delete_item(code)
    if row_cnt == 0:
        return jsonify(message='Item not found'), 404
    message = f'Success'
    return jsonify(message=message)

# /<item_id>/prices - GET
# Returns store & price information for a specific item.
# todo: handle appropriate query parameters (e.g. store, location, price, date last verified).
# todo: currently returns all prices. should group prices by store and only show the most recent for each store
@bp.route('/<code>/prices', methods=['GET'])
def get_item_prices(code):
    item = dalitem.get_item(code)
    if item == None:
        return jsonify(message='Item not found'), 404
        
    prices = dalprice.get_item_prices(code)
    return price_schema.jsonify(prices, many=True)

