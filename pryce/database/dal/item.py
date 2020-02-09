from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound
from pryce.database.dal import db
from pryce.database.models import Item


# noinspection PyMethodMayBeStatic
class DALItem:

    def get_items(self):
        items = Item.query.all()
        return items

    def add_item(self, item):
        db.session.add(item)
        db.session.commit()
        return item.item_id

    def get_item(self, code):
        item = None
        item = Item.query.filter_by(code=code).first()
        return item

    def update_item(self, item_dict):
        item = None
        code = item_dict['code']
        item = Item.query.filter_by(code=code).first()
        if item is not None:
            item.update(item_dict)
            db.session.commit()
        return item

    def delete_item(self, item):
        item = Item.query.filter_by(code=item.code).first()
        if item is not None:
            try:
                db.session.delete(item)
                db.session.commit()
            except:
                db.session.rollback()
                raise
            return True
