from sqlalchemy.orm.exc import NoResultFound
from pryce.database.dal import db
from pryce.database.models import Store

class DALStore():

    def get(self):
        stores = Store.query.all()
        return stores

    def add_store(self, store_dict):
        Store.up
        store = Store(name=name)
        db.session.add(store)
        db.session.commit()

