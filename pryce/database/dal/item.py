from sqlalchemy.orm.exc import NoResultFound
from pryce.database.dal import db
from pryce.database.models import Item


class DALItem():

    def get_items(self):
        items = Item.query.all()
        return items

    def add_item(self, item):
        db.session.add(item)
        db.session.commit()

    def get_item(self, item_id):
        item = Item.query.filter_by(item_id=item_id).first()
        return item

    def update_item(item_dict):
        item = Item.query.filter_by(item_id=item_dict['item_id']).first()
        item.update(item_dict, synchronize_session=False)
        db.session.commit()

    def delete_item(item_id):
        try:
            item = Item.query.filter_by(item_id=item_id).one()
            db.session.delete(item)
            db.session.commit()
        except NoResultFound as nrf:
            raise NoResultFound
