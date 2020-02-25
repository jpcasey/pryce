from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from pryce.database.dal import db
from pryce.database.models import Store, Comment


class DALStore():

    def get(self, name = None):
        stores = Store.query
        if name:
            name = f'%{name}%'
            stores = stores.filter(Store.name.ilike(name))
        return stores.all()

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
    
    def get_store(self, store_id):
        store = Store.query.filter_by(store_id=store_id).first()
        return store

    def get_store_by_place_id(self, place_id):
        store = Store.query.filter_by(place_id=place_id).first()
        return store

    def delete_store(self, store_id):
        rows = Store.query.filter_by(store_id=store_id).delete()
        db.session.commit()
        return rows

    def update_store(self, new_store):
        store = Store.query.filter_by(store_id=new_store.store_id).first()
        if store is not None:
            store.update(new_store)
            db.session.commit()
        return store

    def get_comments(self, store_id):
        comments = Comment.query.filter_by(store_id=store_id).all()
        return comments
        
    def get_comment(self, comment_id):
        comment = Comment.query.filter_by(comment_id=comment_id).first()
        return comment

    def add_comment(self, comment):
        db.session.add(comment)
        db.session.commit()
        return comment

