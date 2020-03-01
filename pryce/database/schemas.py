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
    
    store = fields.Nested(StoreSchema, only=("name", "place_id", "lat", "lng"))


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


# eg. of serialization of SQLA obj: {'item': 125, 'pryce_list': 55, 'quantity': 49}
class PryceListItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PryceListItem
        load_instance = True
        include_relationships = True


class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_fk = True
        model = Comment

    appuser = fields.Nested(AppuserSchema, exclude=(["password"]))