from sqlalchemy.orm.exc import NoResultFound
from pryce.database.dal import db
from pryce.database.models import Store

class DALStore():

    def get(self):
        stores = Store.query.all()
        return stores

    def add_store(self, store_dict):
        store = Store()
        store.update(store_dict)
        db.session.add(store)
        db.session.commit()

    def delete_store(self, store):
        db.session.delete(store)
        db.session.commit()

    def update_store(self, store_dict):
        store = None
        plid = store_dict['place_id']
        try:
            store = Store.query.filter_by(place_id=plid).one()
            store.update(store_dict)
            db.session.commit()
        except NoResultFound as nrf:
            pass
        return store

