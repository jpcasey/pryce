import unittest
from pryce.database.models import Item
from pryce.database.dal.item import DALItem
from pryce import app
from pryce.database.dal import db
from pryce.database.dal import test_db_cfg


# noinspection PyArgumentList
class TestDALItem(unittest.TestCase):

    fud = Item(code='0012345679011', brand='Foo', name='Bar Baz', quantity=0.1,
               quant_unit='oz', description='Fear, Uncertainty, and Doubt',
               image='/path/to/fud.png')

    book = Item(code='9780141979243', brand='Penguin', name='The Master Algorithm', quantity=1,
               quant_unit='ct', description='How the quest for the ultimate learning machine will remake our world',
               image='/path/to/book.png')

    @classmethod
    def setUpClass(cls):
        # TestDALItem.app = Flask(__name__)
        app.config.from_object(test_db_cfg)

    def setUp(self) -> None:
        db.drop_all()
        db.create_all()
        tjs = Item(code='0000000959742', brand="Trader Joe's", name='Turkey Jerky Teriyaki', quantity=4,
                   quant_unit='oz', description='Snap into a Slim Jim')

        vitc = Item(code='0041250500735', brand="Meijer", name='Vitamin C 500 mg', quantity=100,
                    quant_unit='ct', description='100 caplets of Vitamin C',
                    image='https://d2b9vdin3yve6y.cloudfront.net/c5e1720d-dd04-42d3-bc53-eeaeb76b6599.jpg')

        rbw = Item(code='0080432106419', brand="Redbreast", name='Single Pot Still Irish Whiskey 15 Years',
                   quantity=750, quant_unit='ml', description='Irish Whiskey',
                   image='https://d2b9vdin3yve6y.cloudfront.net/f8870767-ff9f-49d1-8cfd-580c530df14b.jpg')

        tid = Item(code='0037000138082', brand="Tide", name='Plus Downy Clean Breeze', quantity=50, quant_unit='fl oz',
                   description='24 loads')

        lor = Item(code='0071249175446', brand="L'Oréal", name='EverStrong Hydrate Shampoo', quantity=8.5,
                   quant_unit='oz', description='Strengthens and Nourishes, Bio-ceramide Complex, Natural Botanicals',
                   image='https://d2b9vdin3yve6y.cloudfront.net/fb33cba4-6d23-41ba-9e5c-8afe3ba5b1ae.jpg')

        db.session.add(tjs)
        db.session.add(vitc)
        db.session.add(rbw)
        db.session.add(tid)
        db.session.add(lor)
        db.session.commit()
        self.item_list = [tjs, vitc, rbw, tid, lor]
        self.dalitem = DALItem()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_get_items(self):
        il = self.dalitem.get_items()
        self.assertIsNotNone(il)
        self.assertCountEqual(il, self.item_list)

    def test_add_item(self):
        fud_added = self.dalitem.add_item(TestDALItem.fud)
        self.assertIsNotNone(fud_added)
        self.assertEqual(fud_added, 6)

    def test_get_item(self):
        i = self.dalitem.get_item("0000000959742")
        self.assertIsNotNone(i)
        self.assertEqual(i.brand, "Trader Joe's")

    def test_update_item(self):
        d = {'code': '0080432106419', 'description': 'Rotgut from Dublin', 'quantity': 1, 'quant_unit': 'gal'}
        item = self.dalitem.update_item(d)
        self.assertEqual(item.item_id, 3)
        self.assertEqual(item.brand, 'Redbreast')
        self.assertEqual(item.quant_unit, 'gal')

    def test_delete_item(self):
        book_id = self.dalitem.add_item(TestDALItem.book)
        self.assertGreater(book_id, 0)
        item = self.dalitem.get_item(TestDALItem.book.code)
        self.assertTrue(self.dalitem.delete_item(item))
        item2 = self.dalitem.get_item(item.code)
        self.assertIsNone(item2)

if __name__ == '__main__':
    pass
