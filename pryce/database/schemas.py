# Schemas for Flask-Marshmallow to easily JSON serialize SQLAlchemy resultsets
from pryce.database.dal import ma
from marshmallow import fields, post_load
from pryce.database.models import *
import simplejson


class ItemSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Item
        #exclude = ["prices", "list_items"]


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
    store = fields.Nested(StoreSchema(only=("store_id", "name", "place_id")))


class AppuserSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Appuser

    #appuser_id = fields.Int(dump_only=True)


class PryceListSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = PryceList
        #load_instance = True

    appuser = fields.Nested(AppuserSchema(only=('appuser_id',)))
    exclude = ['access_id', 'access']

    @post_load
    def deserialize_to_list(self, data, **kwargs):
        return PryceList(**data)

    #list_id = fields.Int(dump_only=True)
    #name = fields.String()
