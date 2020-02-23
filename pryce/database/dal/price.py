from sqlalchemy.orm.exc import NoResultFound
from pryce.database.dal import db
from pryce.database.models import Price, Item
from sqlalchemy import text


class DALPrice:

    def get_item_prices(self, code):
      """
        Returns most recently reported price at each store for a given item code.
      """
      sql = text("""
        select p.* from price p
        inner join item i on i.item_id = p.item_id
        where code = '{}'
        and p.reported = (
          select max(reported) 
          from price
            where item_id = p.item_id
            and store_id = p.store_id
        );
      """.format(code))
      return db.engine.execute(sql)
    
    def add_price(self, price):
        db.session.add(price)
        db.session.commit()
        return price.price_id
   
