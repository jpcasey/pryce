from datetime import timezone, timedelta
import factory
from werkzeug.security import generate_password_hash

from pryce.database.dal import test_db_cfg
from pryce import app
from factory.alchemy import SQLAlchemyModelFactory
from pryce.database.models import db, Appuser, Item, Badge, Store, Price, PryceList, PryceListItem

item_names = ['Bounty', 'Cheezits', 'Tootsie Pops', 'NF-S12A PWM', 'CP850PFCLCD', 'Chisel Tip Marker',
              'Glass Fuses', 'iPhone 7+', 'Premium Toner Cartridge', 'Boston Baked Beans', 'X99-Deluxe',
              '5mil Nitrile Gloves', 'NH-C14S', 'Brite-Mark White', 'Super Glue', 'Apple Pie']

list_names = ['Birthday Party', 'Moving', 'Camping', 'Tailgating', 'Groceries', 'DIY',
              'Home Improvement', 'Bake-off', 'Catering', 'Troop Brunch', 'Improvised Explosives']


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
    lat = factory.Faker('latitude')
    lng = factory.Faker('longitude')
    karma = factory.Faker('random_int', min=0, max=99999, step=1)
    image = factory.Faker('file_path', depth=3, extension='jpg')
    badges = factory.List([factory.SubFactory(PryceMockBadgeModel)])


class PryceMockItemModel(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
        model = Item

    code = factory.Faker('ean13', leading_zero=None)
    name = factory.Iterator(item_names)
    brand = factory.Faker('company')
    quantity = factory.Faker('random_number', digits=2)
    quant_unit = factory.Iterator(['oz', 'fl oz', 'ml', 'g', 'kg', 'gal', 'qt', 'ct', 'l', 'lb'])
    description = factory.Faker('catch_phrase')
    image = factory.Faker('file_path', depth=3, extension='jpg')


class PryceMockStoreModel(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
        model = Store

    place_id = factory.Faker('lexify', text='????????????????????????????')
    lat = factory.Faker('latitude')
    lng = factory.Faker('longitude')
    address = factory.Faker('address')
    #chain_id =
    name = factory.Faker('company')
    image = factory.Faker('file_path', depth=3, extension='jpg')
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


class PryceMockPryceListModel(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
        model = PryceList

    name = factory.Iterator(list_names)
    appuser = factory.SubFactory(PryceMockAppuserModel)


class PryceMockPryceListItemModel(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'
        model = PryceListItem

    quantity = factory.Faker('random_int', min=1, max=99, step=1)
    item = factory.SubFactory(PryceMockItemModel)
    pryce_list = factory.SubFactory(PryceMockPryceListModel)
'''
    @factory.post_generation
    def fks(self, create, extracted, **kwargs):
        if extracted:
            for i in extracted:
                self.items.add(i)

    @factory.post_generation
    def pryce_lists(self, create, extracted, **kwargs):
        if extracted:
            for pl in extracted:
                self.pryce_lists.add(pl)


class PryceMockCommentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Comment

'''

if __name__ == '__main__':
    db.close_all_sessions()
    app.config.from_object(test_db_cfg)
    db.drop_all()
    print("Dropped all")
    db.create_all()
    print("Created all")

    badges = PryceMockBadgeModel.build_batch(5)
    for b in badges:
        db.session.add(b)
        db.session.commit()
    print("Created badges")

    users = PryceMockAppuserModel.build_batch(10)
    # add hard-coded users
    passhash = generate_password_hash('Pa55word')
    u1 = PryceMockAppuserModel.create(username='user1', password=passhash, karma=33496, lat=36.117378, lng=-97.05659)
    for u in users:
        db.session.add(u)
        db.session.commit()
    print("Created users")

    store1 = PryceMockStoreModel(name='Fake Costco')
    store2 = PryceMockStoreModel(name='Test Target')
    store3 = PryceMockStoreModel(name='Phony Walmart')
    stores = PryceMockStoreModel.build_batch(20)
    for s in stores:
        db.session.add(s)
        db.session.commit()
    print("Created stores")

    item1 = PryceMockItemModel(code='9651444131913', name='New Yorker Magazine', brand='Conde Nast', quantity=1, quant_unit='ct', description='NY Magazine',image='/static/path/nym.png')
    item2 = PryceMockItemModel(code='4131913965144', name='Harper\'s Magazine', brand='MacArthur', quantity=1, quant_unit='ct', description='News and Fiction', image='/static/path/harpm.png')
    item3 = PryceMockItemModel(code='1449654913131', name='2TB HDD', brand='Seagate', quantity=1, quant_unit='ct', description='Destined to fail', image='/static/path/shdd.png')
    item4 = PryceMockItemModel(code='9691844838918', name='Coke Zero', brand='Coca-Cola', quantity=500, quant_unit='ml', description='Carbonated poison', image='/static/path/cv.png')
    items = PryceMockItemModel.build_batch(12)
    for i in items:
        db.session.add(i)
        db.session.commit()
    print("Created items")

    price1 = PryceMockPriceModel(price=9.95, store=store1, item=item1)
    price1 = PryceMockPriceModel(price=9.95, store=store1, item=item1, reported="2010-2-21")
    price2 = PryceMockPriceModel(price=12.99, store=store2, item=item2)
    price3 = PryceMockPriceModel(price=89.90, store=store3, item=item3)
    price4 = PryceMockPriceModel(price=1.99, store=store2, item=item4)
    prices = PryceMockPriceModel.build_batch(50)
    for p in prices:
        db.session.add(p)
        db.session.commit()
    print("Created prices")

    owner1 = Appuser.query.filter_by(appuser_id=1).first()
    list1 = PryceMockPryceListModel.create(owner=1, name='Party List', appuser=owner1)
    list2 = PryceMockPryceListModel.create(owner=1, name='Pet Supplies', appuser=owner1)
    list3 = PryceMockPryceListModel.create(owner=1, name='Groceries', appuser=owner1)
    list4 = PryceMockPryceListModel.create(owner=1, name='Bunker Provisions', appuser=owner1)
    pryce_lists = PryceMockPryceListModel.build_batch(20)
    for pl in pryce_lists:
        db.session.add(pl)
        db.session.commit()
    print("Created lists")

    pli1 = PryceMockPryceListItemModel.create(quantity=1, pryce_list=list1, item=item1)
    pli2 = PryceMockPryceListItemModel.create(quantity=5, pryce_list=list1, item=item2)
    pli3 = PryceMockPryceListItemModel.create(quantity=11, pryce_list=list1, item=item3)
    pli4 = PryceMockPryceListItemModel.create(quantity=4, pryce_list=list1, item=item4)
    pryce_lists_items = PryceMockPryceListItemModel.build_batch(100)
    for pli in pryce_lists_items:
        db.session.add(pli)
        db.session.commit()
    print("Created list/items")

    db.close_all_sessions()
    print("Done")
    exit(0)
