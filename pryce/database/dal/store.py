from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from pryce.database.dal import db
from pryce.database.models import Store


class DALStore():

    def get(self):
        stores = Store.query.all()
        return stores

    def add_store(self, store):
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError as ie:
            store = None
        return store

    def add_store_with_dict(self, store_dict):
        store = Store()
        store.update(store_dict)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError as ie:
            store = None
        return store
    
    def get_store_by_place_id(self, place_id):
        store = Store.query.filter_by(place_id=place_id).first()
        return store

    def delete_store(self, store):
        rows = Store.query.filter_by(store_id=store.store_id).delete()
        db.session.commit()
        return rows

    def update_store(self, store):
        db.session.commit()
        return store


