from flask import Blueprint, request, jsonify
from pryce.database.models import Item, Price
from pryce.database.schemas import ItemSchema, PriceSchema
from pryce import db

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
    name = req_body.get('name')
    code = req_body.get('code')
    brand = req_body.get('brand', None)
    weight = req_body.get('weight', 0)
    description = req_body.get('description', '')
    item = Item(name=name, brand=brand, code=code, weight=weight, description=description)
    db.session.add(item)
    db.session.commit()
    return item_schema.jsonify(item)

# /<item_id> - GET
# Returns information for a specific item.
@bp.route('/<item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.filter_by(item_id=item_id).first()
    if item == None:
        return jsonify(message='Item not found'), 404
    return item_schema.jsonify(item)

# /<item_id> - PUT
# Update information for a specific item.
@bp.route('/<item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.filter_by(item_id=item_id).first()
    if item == None:
        return jsonify(message = 'Item not found'), 404
    req_body = request.get_json()
    item.name = req_body.get('name', item.name)
    item.brand = req_body.get('brand', item.brand)
    item.weight = req_body.get('weight', item.weight)
    item.description = req_body.get('description', item.description)
    db.session.commit()
    return item_schema.jsonify(item)

# /<item_id> - DELETE
# Deletes an item from the system.
@bp.route('/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.filter_by(item_id=item_id).first()
    if item != None:
        db.session.delete(item)
        db.session.commit()
        message = f'Successfully deleted "{item.name}"'
        return jsonify(message = message)
    return jsonify(message = 'Item not found'), 404

# /<item_id>/prices - GET
# Returns store & price information for a specific item.
# todo: handle appropriate query parameters (e.g. store, location, price, date last verified).
# todo: currently returns all prices. should group prices by store and only show the most recent for each store
@bp.route('/<item_id>/prices', methods=['GET'])
def get_item_prices(item_id):
    prices = Price.query.filter_by(item_id=item_id).order_by(Price.reported.desc()).all()
    if prices == None:
        return jsonify(message = 'Item not found.'), 404
    price_schema = PriceSchema()
    return price_schema.jsonify(prices, many=True)