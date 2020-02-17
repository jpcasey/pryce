# Schemas for Flask-Marshmallow to easily JSON serialize SQLAlchemy resultsets
from flask_marshmallow.sqla import SQLAlchemySchema, SQLAlchemyAutoSchema
from pryce.database.dal import ma
from marshmallow import fields, post_load
from pryce.database.models import *
import simplejson


class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True
        include_fk = True


class StoreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Store
        load_instance = True
        include_fk = True


class PriceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Price
        load_instance = True
        include_fk = True

    #item = fields.Nested(ItemSchema(only=("item_id", "brand", "name", "code")))
    #store = fields.Nested(StoreSchema(only=("store_id", "name", "place_id")))


class AppuserSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_fk = True
        model = Appuser


class PryceListSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PryceList
        load_instance = True
        include_fk = True


class PryceListItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PryceListItem
        load_instance = True
        include_fk = True

    #@post_load
    #def deserialize_to_list(self, data, **kwargs):
    #    return PryceList(**data)

    #list_id = fields.Int(dump_only=True)
    #name = fields.String()
