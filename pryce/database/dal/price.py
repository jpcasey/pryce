from sqlalchemy.orm.exc import NoResultFound
from pryce.database.dal import db
from pryce.database.models import Price, Item
from sqlalchemy import text


class DALPrice:

    def get_item_prices(self, code):
      """
        Returns most recently reported price at each store for a given item code.
      """
      # subquery to get most recent "reported" timestamp for each item/store combo
      most_recently_reported = db.session.query(Price.item_id, Price.store_id, db.func.max(Price.reported).label('last_reported')).group_by(Price.item_id, Price.store_id).subquery()

      # get all most recent prices and filter by the given item barcode
      prices = Price.query.join(most_recently_reported, (Price.item_id == most_recently_reported.c.item_id) & (Price.store_id == most_recently_reported.c.store_id) 
        & (Price.reported == most_recently_reported.c.last_reported)).join(Item).filter(Item.code == code).order_by(Price.reported.desc()).all()
      return prices

    def add_price(self, price):
        db.session.add(price)
        db.session.commit()
        return price.price_id
   
