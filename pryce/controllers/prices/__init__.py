from flask import Blueprint, jsonify, request
from pryce.database.models import Price
from pryce.database.schemas import PriceSchema
from pryce.database.dal.item import DALItem
from pryce.database.dal.price import DALPrice
from pryce.database.dal.store import DALStore
from pryce.controllers.items import create_item
from datetime import datetime

bp = Blueprint('prices', __name__, url_prefix='/prices')
price_schema = PriceSchema()
dalitem = DALItem()
dalprice = DALPrice()
dalstore = DALStore()

# Accepts a JSON Object that defines the price, currency, item, and store and adds the price
@bp.route('/', methods=['POST'])
def add_price():
    required_fields = ['price', 'currency', 'item', 'store']
    req_body = request.get_json()
    for field in required_fields:
        if field not in req_body:
            message = f'{field} is a required attribute.'
            return jsonify(message=message), 400
    
    # check if item already exists in the db, or create it if not
    item = dalitem.get_item(req_body.get('item').get('code'))
    if item == None:
        item = create_item(req_body.get('item'))
        dalitem.add_item(item)
        
    # check if store exists, and create it if it doesn't
    store = dalstore.get_store_by_place_id(req_body.get('store').get('place_id'))
    if store == None:
            store = dalstore.add_store_with_dict(req_body.get('store'))

    price = req_body.get('price')
    currency = req_body.get('currency', 'USD')
    reported = req_body.get('reported', datetime.utcnow())
    item_price = Price(currency=currency, price=price, item_id=item.item_id, store_id=store.store_id, reported=reported)
    dalprice.add_price(item_price)
    return price_schema.jsonify(item_price), 200
