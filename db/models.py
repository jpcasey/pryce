# coding: utf-8
from sqlalchemy import BigInteger, CheckConstraint, Column, DateTime, Float, ForeignKey, Integer, Numeric, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.postgresql.base import MONEY
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Acces(db.Model):
    __tablename__ = 'access'

    access_id = db.Column(db.Integer, primary_key=True)



class Badge(db.Model):
    __tablename__ = 'badge'

    badge_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image_id = db.Column(db.BigInteger)

    usrs = db.relationship('Usr', secondary='badge_usr', backref='badges')



t_badge_usr = db.Table(
    'badge_usr',
    db.Column('badge_id', db.ForeignKey('badge.badge_id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False),
    db.Column('usr_id', db.ForeignKey('usr.usr_id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False)
)



class Chain(db.Model):
    __tablename__ = 'chain'

    chain_id = db.Column(db.Integer, primary_key=True)



class Comment(db.Model):
    __tablename__ = 'comment'
    __table_args__ = (
        db.CheckConstraint('(content IS NOT NULL) OR (rating IS NOT NULL)'),
    )

    object_id = db.Column(db.Integer, primary_key=True, nullable=False)
    usr_id = db.Column(db.ForeignKey('usr.usr_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    rating = db.Column(db.Numeric)
    content = db.Column(db.Text)
    type = db.Column(db.Integer, primary_key=True, nullable=False)

    usr = db.relationship('Usr', primaryjoin='Comment.usr_id == Usr.usr_id', backref='comments')



class Image(db.Model):
    __tablename__ = 'image'

    image_id = db.Column(db.Integer, primary_key=True)
    fspath = db.Column(db.String, unique=True)
    imgtype = db.Column(db.String)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)



class List(db.Model):
    __tablename__ = 'list'

    list_id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.ForeignKey('usr.usr_id', ondelete='RESTRICT', onupdate='CASCADE'))
    access_id = db.Column(db.ForeignKey('access.access_id', ondelete='RESTRICT', onupdate='CASCADE'))

    access = db.relationship('Acces', primaryjoin='List.access_id == Acces.access_id', backref='lists')
    usr = db.relationship('Usr', primaryjoin='List.owner == Usr.usr_id', backref='lists')



class ListProduct(db.Model):
    __tablename__ = 'list_product'

    product_id = db.Column(db.ForeignKey('product.product_id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False)
    list_id = db.Column(db.ForeignKey('list.list_id', ondelete='RESTRICT', onupdate='CASCADE'), db.ForeignKey('list.list_id'), primary_key=True, nullable=False)
    quantity = db.Column(db.Integer, server_default=db.FetchedValue())

    list = db.relationship('List', primaryjoin='ListProduct.list_id == List.list_id', backref='list_list_products')
    list1 = db.relationship('List', primaryjoin='ListProduct.list_id == List.list_id', backref='list_list_products_0')
    product = db.relationship('Product', primaryjoin='ListProduct.product_id == Product.product_id', backref='list_products')



class Location(db.Model):
    __tablename__ = 'location'

    location_id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)



class Price(db.Model):
    __tablename__ = 'price'

    price_id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3))
    product_id = db.Column(db.ForeignKey('product.product_id', ondelete='RESTRICT', onupdate='CASCADE'))
    usr_id = db.Column(db.ForeignKey('usr.usr_id', ondelete='RESTRICT', onupdate='CASCADE'))
    price = db.Column(db.MONEY)
    reported = db.Column(db.DateTime(True))
    store_id = db.Column(db.ForeignKey('store.store_id', ondelete='RESTRICT', onupdate='CASCADE'))

    product = db.relationship('Product', primaryjoin='Price.product_id == Product.product_id', backref='prices')
    store = db.relationship('Store', primaryjoin='Price.store_id == Store.store_id', backref='prices')
    usr = db.relationship('Usr', primaryjoin='Price.usr_id == Usr.usr_id', backref='prices')



class Product(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    brand = db.Column(db.String)
    weight = db.Column(db.Numeric, nullable=False)
    weight_unit = db.Column(db.String, server_default=db.FetchedValue())
    image_id = db.Column(db.ForeignKey('image.image_id', ondelete='RESTRICT', onupdate='CASCADE'))
    description = db.Column(db.Text, nullable=False)

    image = db.relationship('Image', primaryjoin='Product.image_id == Image.image_id', backref='products')



class Store(db.Model):
    __tablename__ = 'store'

    store_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.ForeignKey('location.location_id', ondelete='RESTRICT', onupdate='CASCADE'))
    chain_id = db.Column(db.ForeignKey('chain.chain_id', ondelete='RESTRICT', onupdate='CASCADE'))
    name = db.Column(db.String)
    image_id = db.Column(db.ForeignKey('image.image_id', ondelete='RESTRICT', onupdate='CASCADE'))

    chain = db.relationship('Chain', primaryjoin='Store.chain_id == Chain.chain_id', backref='stores')
    image = db.relationship('Image', primaryjoin='Store.image_id == Image.image_id', backref='stores')
    location = db.relationship('Location', primaryjoin='Store.location_id == Location.location_id', backref='stores')



class Usr(db.Model):
    __tablename__ = 'usr'

    usr_id = db.Column(db.Integer, primary_key=True)
    usrname = db.Column(db.String)
    password = db.Column(db.String)
    home = db.Column(db.ForeignKey('location.location_id', ondelete='RESTRICT', onupdate='CASCADE'))
    karma = db.Column(db.Integer)
    avatar = db.Column(db.ForeignKey('image.image_id', ondelete='RESTRICT', onupdate='CASCADE'))

    image = db.relationship('Image', primaryjoin='Usr.avatar == Image.image_id', backref='usrs')
    location = db.relationship('Location', primaryjoin='Usr.home == Location.location_id', backref='usrs')
