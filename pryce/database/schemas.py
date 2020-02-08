# Schemas for Flask-Marshmallow to easily JSON serialize SQLAlchemy resultsets
from pryce.database.dal import ma
from marshmallow import fields
from pryce.database.models import *
import simplejson

class ItemSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Item
        exclude = ["prices", "list_items"]
        
class StoreSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Store
        exclude = ["prices"]

class PriceSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Price
    item = fields.Nested(ItemSchema(only=("item_id", "brand", "name", "code")))
    store = fields.Nested(StoreSchema(only=("store_id", "name")))
