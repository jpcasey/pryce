from sqlalchemy.exc import IntegrityError
from pryce.database.dal import db
from pryce.database.models import Item
from sqlalchemy import text

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

    def get_search_list_items(self):
        plain_sql = """with table1 as (select row_number() over (partition by pri.item_id order by pri.reported desc) as rn,
                    pri.price, pri.item_id, pri.store_id, pri.reported from price pri ) select itm.name as item_name, itm.code, table1.item_id, table1.reported, table1.price, sto.place_id, sto.name as store_name
                  from item itm inner join table1 on table1.item_id = itm.item_id inner join store sto on table1.store_id = sto.store_id where rn=1;"""
        sql = text(plain_sql)
        result = db.engine.execute(sql)
        return result

