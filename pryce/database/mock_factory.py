from datetime import timezone, timedelta
import factory
from pryce.database.dal import test_db_cfg
from pryce import app
from flask_sqlalchemy import SQLAlchemy
from factory.alchemy import SQLAlchemyModelFactory
from openlocationcode.openlocationcode import *
from pryce.database.models import db, Acces, Appuser, Item, Badge, Chain, Store, Price

item_names = ['Bounty', 'Cheezits', 'Tootsie Pops', 'NF-S12A PWM', 'CP850PFCLCD', 'Chisel Tip Marker',
              'Glass Fuses', 'iPhone 7+', 'Premium Toner Cartridge', 'Boston Baked Beans', 'X99-Deluxe',
              '5mil Nitrile Gloves', 'NH-C14S', 'Brite-Mark White', 'Super Glue', 'Apple Pie']


def olc(length):
    lat, lng = factory.Faker('local_latlng', country_code='US', coords_only=True)
    return encode(float(lat), float(lng), length)


class PryceMockBadgeModel(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
        model = Badge

    name = factory.Faker('color_name')
    image = factory.Faker('file_path', extension='jpg')


class PryceMockAppuserModel(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
        model = Appuser

    username = factory.Faker('email')
    password = factory.Faker('password', length=16, special_chars=True, digits=True, upper_case=True, lower_case=True)
    lat, _ = factory.Faker('local_latlng', country_code='US', coords_only=True).generate()
    _, lng = factory.Faker('local_latlng', country_code='US', coords_only=True).generate()
    karma = factory.Faker('random_int', min=0, max=99999, step=1)
    image = '/static/item/' + factory.Faker('hexify', text='^^^^^^^^^^', upper="False").generate() + '.jpg'
    badges = factory.List([factory.SubFactory(PryceMockBadgeModel)])


class PryceMockItemModel(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
        model = Item

    code = factory.Faker('ean13', leading_zero=None)
    name = factory.Faker('sentence', nb_words=1, variable_nb_words="False", ext_word_list=item_names)
    brand = factory.Faker('company')
    quantity = factory.Faker('random_number', digits=2)
    quant_unit = factory.Faker('random_sample', elements=('oz', 'fl oz', 'ml', 'g', 'kg', 'gal', 'qt', 'ct', 'l', 'lb'),
                               length=1).generate()[0]
    description = factory.Faker('catch_phrase')
    image = '/static/item/' + factory.Faker('hexify', text='^^^^^^^^^^', upper="False").generate() + '.jpg'


class PryceMockStoreModel(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
        model = Store

    place_id = factory.Faker('lexify', text='????????????????????????????')
    lat, _ = factory.Faker('local_latlng', country_code='US', coords_only=True).generate()
    _, lng = factory.Faker('local_latlng', country_code='US', coords_only=True).generate()
    address = factory.Faker('address')
    #chain_id =
    name = factory.Faker('company')
    image = '/static/item/' + factory.Faker('hexify', text='^^^^^^^^^^', upper="False").generate() + '.jpg'
    reported = (lambda x:  factory.Faker('past_datetime', start_date='-30d', tzinfo=x))\
        (timezone(timedelta(hours=factory.Faker('random_int', min=-12, max=12).generate())))


class PryceMockPriceModel(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
        model = Price

    currency = factory.Faker('currency_code')
    price = factory.Faker('numerify', text='##.##')
    reported = (lambda x:  factory.Faker('past_datetime', start_date='-30d', tzinfo=x)) \
        (timezone(timedelta(hours=factory.Faker('random_int', min=-12, max=12).generate())))
    store = factory.SubFactory(PryceMockStoreModel)
    appuser = factory.SubFactory(PryceMockAppuserModel)
    item = factory.SubFactory(PryceMockItemModel)

'''
class PryceMockListFactory(SQLAlchemyModelFactory):
    class Meta:
        model = List


class PryceMockCommentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Comment

'''

if __name__ == '__main__':
    app.config.from_object(test_db_cfg)
    db.drop_all()
    db.create_all()
    # print("Using {0} to connect to the database.".format(db.get_app().config['SQLALCHEMY_DATABASE_URI']))

    badges = PryceMockBadgeModel.build_batch(5)
    for b in badges:
        db.session.add(b)
        db.session.commit()

    users = PryceMockAppuserModel.build_batch(10)
    # add hard-coded users
    u1 = PryceMockAppuserModel(username='user1', password='Pa55word')
    u2 = PryceMockAppuserModel(username='user2', password='Pa55word')
    for u in users:
        db.session.add(u)
        db.session.commit()

    stores = PryceMockItemModel.build_batch(20)
    for s in stores:
        db.session.add(s)
        db.session.commit()

    items = PryceMockItemModel.build_batch(20)
    for i in items:
        db.session.add(i)
        db.session.commit()

    prices = PryceMockPriceModel.build_batch(100)
    for p in prices:
        db.session.add(p)
        db.session.commit()
