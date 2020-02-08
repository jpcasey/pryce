from sqlalchemy.orm.exc import NoResultFound
from pryce.database.dal import db
from pryce.database.models import Price


# noinspection PyMethodMayBeStatic
class DALPrice:

    def get_item_prices(self, item_id):
        prices = None
        prices = Price.query.filter_by(item_id=item_id).order_by(Price.reported.desc()).all()
        return prices

    def add_price(self, price):
        db.session.add(price)
        db.session.commit()
        return price.price_id
