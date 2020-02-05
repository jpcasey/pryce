from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound
from pryce.database.dal import db
from pryce.database.models import Item


class DALItem:

    def get_items(self):
        items = Item.query.all()
        return items

    def add_item(self, item):
        db.session.add(item)
        db.session.commit()

    def get_item(self, code):
        try:
            item = Item.query.filter_by(code=code).one()
        except MultipleResultsFound as mrf:
            raise MultipleResultsFound
        return item

    def update_item(self, item_dict):
        item = Item.query.filter_by(item_id=item_dict['item_id']).first()
        item.update(item_dict, synchronize_session=False)
        db.session.commit()

    def delete_item(self, item_id):
        try:
            item = Item.query.filter_by(item_id=item_id).one()
            db.session.delete(item)
            db.session.commit()
        except NoResultFound as nrf:
            raise NoResultFound
