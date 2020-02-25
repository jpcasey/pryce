import requests
from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from pryce.database.models import Store, Item, Price
from pryce.database.schemas import StoreSchema, ItemSchema, PriceSchema, CommentSchema
from pryce.database.dal.price import DALPrice
from pryce.database.dal.store import DALStore

bp = Blueprint('stores', __name__, url_prefix='/stores')
store_schema = StoreSchema()
price_schema = PriceSchema()
comment_schema = CommentSchema()
dalprice = DALPrice()
dalstore = DALStore()

# / - GET
# Returns a list of stores in the system.
# allows filtering by name
@bp.route('/', methods=['GET'])
def get_stores():
    stores = dalstore.get(request.args.get('name'))
    return store_schema.jsonify(stores, many=True)

# /- POST
# Adds a store to the database.
@bp.route('/', methods=['POST'])
def add_store():
    if not request.is_json:
        return jsonify(message='Missing JSON in request'), 400

    try:
        store = store_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(message='Bad Request', validation_errors=err.messages), 400

    store = dalstore.add_store(store)
    return store_schema.jsonify(store)

# /<store_id> - GET
# Returns information for a specific store.
@bp.route('/<store_id>', methods=['GET'])
def get_store(store_id):
    store = dalstore.get_store(store_id)
    if store is None:
        return jsonify(message='Store not found'), 404
    return store_schema.jsonify(store)

# /<store_id> - PUT
# Update information for a specific store.
@bp.route('/<store_id>', methods=['PUT'])
def update_store(store_id):
    if not request.is_json:
        return jsonify(message='Missing JSON in request'), 400

    try:
        store = store_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(message='Bad Request', validation_errors=err.messages), 400

    db_store = dalstore.update_store(store)

    if db_store is None:
        return jsonify(message = 'Store not found.'), 404

    return store_schema.jsonify(db_store)

# /<store_id> - DELETE
# Deletes a store from the system.
@bp.route('/<store_id>', methods=['DELETE'])
def delete_store(store_id):
    rows_deleted = dalstore.delete_store(store_id)
    if rows_deleted == 0:
        return jsonify(message = 'Store not found'), 404
    return jsonify(message = f'Successfully deleted store')

# /find - GET
# Returns a list of nearby stores, ranked by distance, using the google maps nearby search API
@bp.route('/find', methods=['GET'])
def find_stores():
    lat = request.args.get('lat')
    lng = request.args.get('long')
    uri = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={current_app.config["GOOGLE_API_KEY"]}&location={lat},{lng}&type=store&rankby=distance'
    stores = requests.get(uri)
    return stores.json()

# /<store_id>/comments - GET
# Returns all shopping experience comments and ratings for a store.
@bp.route('/<store_id>/comments', methods=['GET'])
def get_comments(store_id):
    comments = dalstore.get_comments(store_id)
    return comment_schema.jsonify(comments, many=True)

# /<store_id>/comments - POST
# Adds a shopping experience comment and rating for a store.
@bp.route('/<store_id>/comments', methods=['POST'])
@jwt_required
def add_comment(store_id):
    store = dalstore.get_store(store_id)
    if store is None:
        return jsonify(message= 'Store not found.'), 404

    if not request.is_json:
        return jsonify(message='Missing JSON in request'), 400
    
    req_body = request.get_json()

    # associate comment with logged in user
    appuser = get_jwt_identity()
    if appuser:
        req_body['appuser_id'] = appuser.get('appuser_id')

    req_body['store_id'] = store_id

    try:
        comment = comment_schema.load(req_body)
    except ValidationError as err:
        return jsonify(message='Bad Request', validation_errors=err.messages), 400

    comment = dalstore.add_comment(comment)
    return comment_schema.jsonify(comment)

# /<store_id>/comments/<comment_id> - GET
# Gets a specific shopping experience comment and rating.
@bp.route('/<store_id>/comments/<comment_id>', methods=['GET'])
def get_comment(store_id, comment_id):
    comment = dalstore.get_comment(comment_id)
    if comment is None:
        return jsonify(message= 'Comment not found.'), 404
    return comment_schema.jsonify(comment)