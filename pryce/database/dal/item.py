from sqlalchemy.exc import IntegrityError
from pryce.database.dal import db
from pryce.database.models import Item


class DALItem:

    def get_items(self, name = None, brand = None):
        items = Item.query
        if name:
            name = f'%{name}%'
            items = items.filter(Item.name.ilike(name))
        if brand:
            brand = f'%{brand}%'
            items = items.filter(Item.brand.ilike(brand))
        return items.all()

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

    def delete_item(self, item_id):
        rows = Item.query.filter_by(item_id=item_id).delete()
        db.session.commit()
        return rows
