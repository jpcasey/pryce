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
        try:
            item = Item.query.filter_by(code=code).one()
        except MultipleResultsFound as mrf:
            raise MultipleResultsFound
        return item

    def update_item(self, item_dict):
        item = None
        code = item_dict['code']
        try:
            item = Item.query.filter_by(code=code).one()
            item.update(item_dict)
            db.session.commit()
        except NoResultFound as nrf:
            pass
        return item

    def delete_item(self, item_id):
        try:
            item = Item.query.filter_by(item_id=item_id).one()
            db.session.delete(item)
            db.session.commit()
        except NoResultFound as nrf:
            raise NoResultFound
