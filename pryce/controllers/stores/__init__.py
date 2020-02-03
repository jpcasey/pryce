from flask import Blueprint, request, jsonify
from pryce.database.models import Store, Item, Price
from pryce.database.schemas import StoreSchema, ItemSchema, PriceSchema
from pryce import db

bp = Blueprint('stores', __name__, url_prefix='/stores')
store_schema = StoreSchema()
price_schema = PriceSchema()

# / - GET
# Returns a list of stores in the system.
# todo: allow filtering using query parameters (e.g. name, location).
@bp.route('/', methods=['GET'])
def get_stores():
    stores = Store.query.all()
    return store_schema.jsonify(stores, many=True)

# /- POST
# Adds a store to the database.
@bp.route('/', methods=['POST'])
def add_store():
    req_body = request.get_json()
    if 'name' not in req_body:
        return jsonify(message='Name is a required attribute'), 400
    name = req_body.get('name')
    message = f'Successfully added store {name}'
    store = Store(name=name)
    db.session.add(store)
    db.session.commit()
    return store_schema.jsonify(store)

# /<store_id> - GET
# Returns information for a specific store.
@bp.route('/<store_id>', methods=['GET'])
def get_store(store_id):
    store = Store.query.filter_by(store_id=store_id).first()
    if store == None:
        return jsonify(message='Store not found'), 404
    return store_schema.jsonify(store)

# /<store_id> - PUT
# Update information for a specific store.
@bp.route('/<store_id>', methods=['PUT'])
def update_store(store_id):
    store = Store.query.filter_by(store_id=store_id).first()
    if store == None:
        return jsonify(message = 'Item not found'), 404
    req_body = request.get_json()
    store.name = req_body.get('name', store.name)
    db.session.commit()
    return store_schema.jsonify(store)

# /<store_id> - DELETE
# Deletes a store from the system.
@bp.route('/<store_id>', methods=['DELETE'])
def delete_store(store_id):
    store = Store.query.filter_by(store_id=store_id).first()
    if store == None:
        return jsonify(message = 'Store not found'), 404
    db.session.delete(store)
    db.session.commit()
    message = f'Successfully deleted "{store.name}"'
    return jsonify(message = message)

# The below routes need to be reworked somehow... I'm not sure if it makes sense to have all this behind the stores endpoint.

# /<store_id>/prices - GET
# Returns information on all prices at a specific store.  
# todo: allow filtering using query parameters (e.g. name, brand, price, date last verified).
@bp.route('/<store_id>/prices', methods=['GET'])
def get_store_items(store_id):
    prices = Price.query.filter_by(store_id=store_id).all()
    if prices == None:
        return jsonify(message='Store not found'), 404
    return price_schema.jsonify(prices, many=True)

# /<store_id>/items/<item_id> - GET
# Returns price information for a specific item at a specific store
@bp.route('/<store_id>/items/<item_id>', methods=['GET'])
def get_store_item(store_id, item_id):
    prices = Price.query.filter_by(store_id=store_id, item_id=item_id).order_by(Price.reported.desc()).all()
    if prices == None:
        return jsonify(message='No information for item at store.'), 404
    return price_schema.jsonify(prices, many=True)

# /<store_id>/items/<item_id> - POST
# Adds price information for a specific item at a specific store.
@bp.route('/<store_id>/items/<item_id>', methods=['POST'])
def add_store_item(store_id, item_id):
    store = Store.query.filter_by(store_id=store_id).first()
    if store == None:
        return jsonify(message = 'Store not found'), 404
    item = Item.query.filter_by(item_id=item_id).first()
    if item == None:
        return jsonify(message='Item not found'), 404

    req_body = request.get_json()
    if 'price' not in req_body:
        return jsonify(message='Price is a required attribute'), 400
    price = req_body.get('price')
    currency = req_body.get('currency', 'USD')
    item_price = Price(currency=currency, item_id=item_id, price=price, store_id=store_id)
    db.session.add(item_price)
    db.session.commit()
    return price_schema.jsonify(item_price)

# /<store_id>/items/<item_id> - PUT
# Updates price information for a specific item at a specific store.

######## Do we even need to allow this??  Would just add a new record if need to change current price.

# /<store_id>/items/<item_id> - DELETE
# Deletes price information for a specific item at a specific store.

######## Do we even want to allow this??

# /<store_id>/items/<item_id>/comments - GET
# Returns all comments and ratings for a specific item at a specific store.

# /<store_id>/items/<item_id>/comments - POST
# Adds a comment and rating for a specific item at a specific store.

# /<store_id>/items/<item_id>/comments/<comment_id> - PUT
# Update a comment and rating for specific item at a specific store.

# /<store_id>/items/<item_id>/comments/<comment_id> - DELETE
# Deletes a comment and rating for a specific item at a specific store.