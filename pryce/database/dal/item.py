from sqlalchemy.exc import IntegrityError
from pryce.database.dal import db
from pryce.database.models import Item


class DALItem:

    def get_items(self):
        items = Item.query.all()
        return items

    def add_item(self, item):
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError as ie:
            item = None
        return item

    def get_item(self, code):
        return Item.query.filter_by(code=code).first()

    def update_item(self, item_dict):
        item = None
        code = item_dict['code']
        item = Item.query.filter_by(code=code).first()
        if item is not None:
            item.update(item_dict)
            db.session.commit()
        return item

    def delete_item(self, code):
        rows = Item.query.filter_by(code=code).delete()
        db.session.commit()
        return rows
