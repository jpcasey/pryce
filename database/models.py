# coding: utf-8
from sqlalchemy import BigInteger, CheckConstraint, Column, DateTime, Float, ForeignKey, Integer, Numeric, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.postgresql.base import MONEY
from flask_sqlalchemy import SQLAlchemy

from ..main import db


class Acces(db.Model):
    __tablename__ = 'access'

    access_id = db.Column(db.Integer, primary_key=True)



class Appuser(db.Model):
    __tablename__ = 'appuser'

    appuser_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    home = db.Column(db.ForeignKey('location.location_id', ondelete='RESTRICT', onupdate='CASCADE'))
    karma = db.Column(db.Integer)
    avatar = db.Column(db.ForeignKey('image.image_id', ondelete='RESTRICT', onupdate='CASCADE'))

    image = db.relationship('Image', primaryjoin='Appuser.avatar == Image.image_id', backref='appusers')
    location = db.relationship('Location', primaryjoin='Appuser.home == Location.location_id', backref='appusers')
    badges = db.relationship('Badge', secondary='badge_appuser', backref='appusers')



class Badge(db.Model):
    __tablename__ = 'badge'

    badge_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image_id = db.Column(db.BigInteger)



t_badge_appuser = db.Table(
    'badge_appuser',
    db.Column('badge_id', db.ForeignKey('badge.badge_id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False),
    db.Column('appuser_id', db.ForeignKey('appuser.appuser_id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False)
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
    appuser_id = db.Column(db.ForeignKey('appuser.appuser_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    rating = db.Column(db.Numeric)
    content = db.Column(db.Text)
    type = db.Column(db.Integer, primary_key=True, nullable=False)

    appuser = db.relationship('Appuser', primaryjoin='Comment.appuser_id == Appuser.appuser_id', backref='comments')



class Image(db.Model):
    __tablename__ = 'image'

    image_id = db.Column(db.Integer, primary_key=True)
    fspath = db.Column(db.String, unique=True)
    imgtype = db.Column(db.String)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)



class Item(db.Model):
    __tablename__ = 'item'

    item_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    brand = db.Column(db.String)
    weight = db.Column(db.Numeric, nullable=False)
    weight_unit = db.Column(db.String, server_default=db.FetchedValue())
    image_id = db.Column(db.ForeignKey('image.image_id', ondelete='RESTRICT', onupdate='CASCADE'))
    description = db.Column(db.Text, nullable=False)

    image = db.relationship('Image', primaryjoin='Item.image_id == Image.image_id', backref='items')



class List(db.Model):
    __tablename__ = 'list'

    list_id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.ForeignKey('appuser.appuser_id', ondelete='RESTRICT', onupdate='CASCADE'))
    access_id = db.Column(db.ForeignKey('access.access_id', ondelete='RESTRICT', onupdate='CASCADE'))

    access = db.relationship('Acces', primaryjoin='List.access_id == Acces.access_id', backref='lists')
    appuser = db.relationship('Appuser', primaryjoin='List.owner == Appuser.appuser_id', backref='lists')



class ListItem(db.Model):
    __tablename__ = 'list_item'

    item_id = db.Column(db.ForeignKey('item.item_id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False)
    list_id = db.Column(db.ForeignKey('list.list_id'), db.ForeignKey('list.list_id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False)
    quantity = db.Column(db.Integer, server_default=db.FetchedValue())

    item = db.relationship('Item', primaryjoin='ListItem.item_id == Item.item_id', backref='list_items')
    list = db.relationship('List', primaryjoin='ListItem.list_id == List.list_id', backref='list_list_items')
    list1 = db.relationship('List', primaryjoin='ListItem.list_id == List.list_id', backref='list_list_items_0')



class Location(db.Model):
    __tablename__ = 'location'

    location_id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)



class Price(db.Model):
    __tablename__ = 'price'

    price_id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3))
    item_id = db.Column(db.ForeignKey('item.item_id', ondelete='RESTRICT', onupdate='CASCADE'))
    appuser_id = db.Column(db.ForeignKey('appuser.appuser_id', ondelete='RESTRICT', onupdate='CASCADE'))
    price = db.Column(MONEY)
    reported = db.Column(db.DateTime(True))
    store_id = db.Column(db.ForeignKey('store.store_id', ondelete='RESTRICT', onupdate='CASCADE'))

    appuser = db.relationship('Appuser', primaryjoin='Price.appuser_id == Appuser.appuser_id', backref='prices')
    item = db.relationship('Item', primaryjoin='Price.item_id == Item.item_id', backref='prices')
    store = db.relationship('Store', primaryjoin='Price.store_id == Store.store_id', backref='prices')



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
