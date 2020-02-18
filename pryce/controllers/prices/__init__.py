from flask import Blueprint, jsonify, request
from pryce.database.models import Price
from pryce.database.schemas import PriceSchema, StoreSchema, ItemSchema
from pryce.database.dal.item import DALItem
from pryce.database.dal.price import DALPrice
from pryce.database.dal.store import DALStore
from marshmallow import ValidationError
from datetime import datetime
from flask_jwt_extended import jwt_optional, get_jwt_identity

bp = Blueprint('prices', __name__, url_prefix='/prices')
price_schema = PriceSchema()
store_schema = StoreSchema()
item_schema = ItemSchema()
dalitem = DALItem()
dalprice = DALPrice()
dalstore = DALStore()

# Accepts a JSON Object that defines the price, currency, item, and store and adds the price
@bp.route('/', methods=['POST'])
@jwt_optional
def add_price():
    if not request.is_json:
        return jsonify(message="Missing JSON in request"), 400

    req_body = request.get_json()

    req_item = req_body.pop('item', None)
    if req_item is None or req_item.get('code') is None:
        return jsonify(message='"item" is a required property.'), 400

    req_store = req_body.pop('store', None)
    if req_store is None or req_store.get('place_id') is None:
        return jsonify(message='"store" is a required property.'), 400

    # check if item already exists in the db, or validate & create it if not
    item = dalitem.get_item(req_item.get('code'))
    if item is None:
        try:
            item = item_schema.load(req_item)
        except ValidationError as err:
            return jsonify(message="Bad Request", validation_errors=err.messages), 400
        item = dalitem.add_item(item)
    req_body['item_id'] = item.item_id

    # check if store exists, or validate & create it if it doesn't
    store = dalstore.get_store_by_place_id(req_store.get('place_id'))
    if store is None:
        try:
            store = store_schema.load(req_store)
        except ValidationError as err:
            return jsonify(message="Bad Request", validation_errors=err.messages), 400
        store = dalstore.add_store(store)
    req_body['store_id'] = store.store_id

    # associate reported price with logged in user (if applicable)
    appuser = get_jwt_identity()
    if appuser:
        req_body['appuser_id'] = appuser.get('appuser_id')

    # mainly for testing. if no 'reported' property is provided, default to current UTC datetime.
    if req_body.get('reported') is None:
       req_body['reported'] = datetime.utcnow().isoformat()

    # validate and add the price
    try:
        item_price = price_schema.load(req_body)
    except ValidationError as err:
        return jsonify(message="Bad Request", validation_errors=err.messages), 400

    dalprice.add_price(item_price)
    return price_schema.jsonify(item_price), 200
