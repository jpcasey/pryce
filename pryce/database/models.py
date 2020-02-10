from pryce.database.dal import db


class PryceModel:
    def update(self, values):
        for k, v in values.items():
            setattr(self, k, v)


class Acces(db.Model):
    __tablename__ = 'access'
    access_id = db.Column(db.Integer, primary_key=True)


class Appuser(PryceModel, db.Model):
    __tablename__ = 'appuser'
    appuser_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    karma = db.Column(db.Integer)
    image = db.Column(db.String)
    lat = db.Column(db.Numeric(17, 15))
    lng = db.Column(db.Numeric(18, 15))
    badges = db.relationship('Badge', secondary='badge_appuser', backref='appusers')


class Badge(db.Model):
    __tablename__ = 'badge'

    badge_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)


t_badge_appuser = db.Table(
    'badge_appuser',
    db.Column('badge_id', db.ForeignKey('badge.badge_id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True,
              nullable=False),
    db.Column('appuser_id', db.ForeignKey('appuser.appuser_id', ondelete='RESTRICT', onupdate='CASCADE'),
              primary_key=True, nullable=False)
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


class Item(PryceModel, db.Model):
    __tablename__ = 'item'

    item_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    brand = db.Column(db.String)
    quantity = db.Column(db.Numeric, nullable=True)
    quant_unit = db.Column(db.String, server_default=db.FetchedValue())
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String)


class List(PryceModel, db.Model):
    __tablename__ = 'list'

    list_id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.ForeignKey('appuser.appuser_id', ondelete='RESTRICT', onupdate='CASCADE'))
    access_id = db.Column(db.ForeignKey('access.access_id', ondelete='RESTRICT', onupdate='CASCADE'))
    access = db.relationship('Acces', primaryjoin='List.access_id == Acces.access_id', backref='lists')
    appuser = db.relationship('Appuser', primaryjoin='List.owner == Appuser.appuser_id', backref='lists')


class ListItem(db.Model):
    __tablename__ = 'list_item'

    item_id = db.Column(db.ForeignKey('item.item_id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True,
                        nullable=False)
    list_id = db.Column(db.ForeignKey('list.list_id'),
                        db.ForeignKey('list.list_id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True,
                        nullable=False)
    quantity = db.Column(db.Integer, server_default=db.FetchedValue())

    item = db.relationship('Item', primaryjoin='ListItem.item_id == Item.item_id', backref='list_items')
    list = db.relationship('List', primaryjoin='ListItem.list_id == List.list_id', backref='list_list_items')
    list1 = db.relationship('List', primaryjoin='ListItem.list_id == List.list_id', backref='list_list_items_0')


class Store(PryceModel, db.Model):
    __tablename__ = 'store'
    store_id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.String, unique=True, nullable=False)
    lat = db.Column(db.Numeric(17, 15))
    lng = db.Column(db.Numeric(18, 15))
    address = db.Column(db.String)
    chain_id = db.Column(db.ForeignKey('chain.chain_id', ondelete='RESTRICT', onupdate='CASCADE'))
    name = db.Column(db.String)
    image = db.Column(db.String)
    chain = db.relationship('Chain', primaryjoin='Store.chain_id == Chain.chain_id', backref='stores')
    reported = db.Column(db.DateTime(True), nullable=False)


class Price(PryceModel, db.Model):
    __tablename__ = 'price'
    price_id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), default='USD')
    item_id = db.Column(db.ForeignKey('item.item_id', ondelete='RESTRICT', onupdate='CASCADE'))
    appuser_id = db.Column(db.ForeignKey('appuser.appuser_id', ondelete='RESTRICT', onupdate='CASCADE'))
    price = db.Column(db.Numeric(12, 3), nullable=False)
    reported = db.Column(db.DateTime(True), nullable=False)
    store_id = db.Column(db.ForeignKey('store.store_id', ondelete='RESTRICT', onupdate='CASCADE'))
    appuser = db.relationship('Appuser', primaryjoin='Price.appuser_id == Appuser.appuser_id', backref='prices')
    item = db.relationship('Item', primaryjoin='Price.item_id == Item.item_id', backref='prices')
    store = db.relationship('Store', primaryjoin='Price.store_id == Store.store_id', backref='prices')


