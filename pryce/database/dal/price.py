from sqlalchemy.orm.exc import NoResultFound
from pryce.database.dal import db
from pryce.database.models import Price, Item


class DALPrice:

    def get_item_prices(self, code):
      prices = None
      prices = Price.query.join(Item).filter(Item.code == code).order_by(Price.reported.desc()).all()
      return prices
    
    def add_price(self, price):
        db.session.add(price)
        db.session.commit()
        return price.price_id
   
