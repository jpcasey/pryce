import requests
from flask import Blueprint, request, jsonify, current_app
from pryce.database.models import Store, Item, Price
from pryce.database.schemas import StoreSchema, ItemSchema, PriceSchema
from pryce.database.dal.price import DALPrice
from pryce.database.dal.store import DALStore
from pryce.database.dal.item import DALItem
from werkzeug.exceptions import BadRequest
from pryce.database import schemas


bp = Blueprint('prices', __name__, url_prefix='/prices')
store_schema = StoreSchema()
price_schema = PriceSchema()
dalprice = DALPrice()
dalstore = DALStore()
dalitem = DALItem()

# /- POST
# Adds a store to the database.
@bp.route('/', methods=['POST'])
def add_price():
    try:
        req_body = request.get_json()
    except BadRequest as br:
        return br
    item = dalitem.get_item(req_body['item']['code'])
    item_pk = 0
    if item is None:
        item_pk = dalitem.add_item(item)
        #TODO: need return
    else:
        item_pk = item.item_id
    store = dalstore.get_store(req_body['store']['place_id'])
    if store is None:
        #TODO fallback? if so, on what?

        return schemas.ItemSchema.dump(item)

        return jsonify(item)'' not in req_body:
        return jsonify(message='Name is a required attribute'), 400
    store = dalstore.add_store(req_body)
    return store_schema.jsonify(store)