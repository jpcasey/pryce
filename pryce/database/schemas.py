# Schemas for Flask-Marshmallow to easily JSON serialize SQLAlchemy resultsets
from pryce import ma
from pryce.database.models import *
import simplejson

class ItemSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Item
        
class PriceSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Price

class StoreSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Store

class AppuserSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Appuser

class BadgeSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Badge

class CommentSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Comment

class ImageSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Image

class ListSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = List

class ListItemSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = ListItem

class LocationSchema(ma.ModelSchema):
    class Meta:
        json_module = simplejson
        model = Location
