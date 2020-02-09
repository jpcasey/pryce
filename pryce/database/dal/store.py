from sqlalchemy.exc import IntegrityError
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
        rows = Store.query.filter_by(code=item.code).delete()

        db.session.delete(store)
        db.session.commit()

    """
    :param store_dict: a dictionary containing a place_id value
    :return: the updated store object or None if a store with the given place_id does not exist
    """
    def update_store(self, store_dict):
        store = None
        plid = store_dict['place_id']
        store = Store.query.filter_by(place_id=plid).first()
        if store is not None:
            store.update(store_dict)
            db.session.commit()
        return store
