from flask import Blueprint, request, jsonify
from pryce.database.models import Item, Price
from pryce.database.schemas import ItemSchema, PriceSchema
from pryce.database.dal.item import DALItem as dalitem
from pryce.database.dal.price import DALPrice as dalprice

bp = Blueprint('items', __name__, url_prefix='/items')
item_schema = ItemSchema()

# / - GET
# Returns a list of items in the system.  Can be filtered using query parameters (e.g. name, brand)
@bp.route('/', methods=['GET'])
def get_items():
    items = Item.query.all()
    return item_schema.jsonify(items, many=True)

# /- POST
# Adds an item to the system.
@bp.route('/', methods=['POST'])
def add_item():
    req_body = request.get_json()
    if 'name' not in req_body or 'code' not in req_body:
        return jsonify(message='Name and brand are required attributes.'), 400
    # other options here would be handing the DAL the json dict (see update_item)
    # or deserializing to an SQLA object via marshmallow and passing that in
    name = req_body.get('name')
    code = req_body.get('code')
    brand = req_body.get('brand', None)
    weight = req_body.get('weight', 0)
    description = req_body.get('description', '')
    item = Item(name=name, brand=brand, code=code, weight=weight, description=description)
    dalitem.add_item(item)
    return item_schema.jsonify(item)

# /<item_id> - GET
# Returns information for a specific item.
# How is the client going to know the PK of the item?
# @bp.route('/<item_id>', methods=['GET'])
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
@bp.route('/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        dalitem.delete_item(item_id)
    # ideally there'd be controller-specific exception caught here
    except Exception as e:
        return jsonify(message='Item not found'), 404
    message = f'Success'
    return jsonify(message=message)

# /<item_id>/prices - GET
# Returns store & price information for a specific item.
# todo: handle appropriate query parameters (e.g. store, location, price, date last verified).
# todo: currently returns all prices. should group prices by store and only show the most recent for each store
@bp.route('/<item_id>/prices', methods=['GET'])
def get_item_prices(item_id):
    prices = dalprice.get_item_prices(item_id)
    if prices == None:
        return jsonify(message = 'Item not found.'), 404
    price_schema = PriceSchema()
    return price_schema.jsonify(prices, many=True)

