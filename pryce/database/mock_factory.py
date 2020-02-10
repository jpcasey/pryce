import datetime

import factory
from factory.alchemy import SQLAlchemyModelFactory
from openlocationcode.openlocationcode import *
from faker import Faker
from faker.providers import geo, barcode, company
from pryce.database.models import *

item_names = ['Bounty', 'Cheezits', 'Tootsie Pops', 'NF-S12A PWM', 'CP850PFCLCD', 'Chisel Tip Marker',
              'Glass Fuses', 'iPhone 7+', 'Premium Toner Cartridge', 'Boston Baked Beans', 'X99-Deluxe',
              '5mil Nitrile Gloves', 'NH-C14S', 'Brite-Mark White', 'Super Glue', 'Apple Pie']


def olc(length):
    lat, lng = factory.Faker('local_latlng', country_code='US', coords_only=True)
    return encode(float(lat), float(lng), length)


class PryceMockBadgeModel(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = None
        model = Badge

    name = factory.Faker('color_name')
    image = factory.Faker('file_path', extension='jpg')


class PryceMockUserModel(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = None
        model = Appuser

    username = factory.Faker('email')
    password = factory.Faker('password', length=16, special_chars=True, digits=True, upper_case=True, lower_case=True)
    home = factory.Faker('lexify', text='????????????????????????????????????????????')
    karma = factory.Faker('random_int', min=0, max=99999, step=1)
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


'''

class PryceMockStoreFactory(SQLAlchemyModelFactory):
    pass  # class Meta:
    # sqlalchemy_session = db.session
    # sqlalchemy_session_persistence = 'commit'
    # model = Store


class PryceMockPriceFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Price
'''

'''
class PryceMockListFactory(SQLAlchemyModelFactory):
    class Meta:
        model = List


class PryceMockCommentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Comment

'''
if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    # print("Using {0} to connect to the database.".format(db.get_app().config['SQLALCHEMY_DATABASE_URI']))

    badges = PryceMockBadgeModel.build_batch(5)
    for b in badges:
        db.session.add(b)
        db.session.commit()

    users = PryceMockUserModel.build_batch(10)
    # add hard-coded users
    u1 = PryceMockUserModel(username='user1', password='Pa55word')
    u2 = PryceMockUserModel(username='user2', password='Pa55word')
    users.append(u1)
    users.append(u2)
    for u in users:
        db.session.add(u)
        db.session.commit()

    items = PryceMockItemModel.build_batch(20)
    for i in items:
        db.session.add(i)
        db.session.commit()
