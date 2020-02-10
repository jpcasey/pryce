from datetime import datetime
import unittest
from pryce.database.models import Store
from pryce.database.dal.store import DALStore
from pryce import app
from pryce.database.dal import db
from pryce.database.dal import test_db_cfg
from pryce.database.mock_factory import PryceMockStoreFactory

class TestDALStore(unittest.TestCase):
    tjs = Store(name="Trader Joe's", address="5000 Settlers Market Blvd, Williamsburg, VA 23188", lat=37.277125,
                lng=-76.7478222, place_id='ChIJYz3Zy82LsIkRcM06ika1tJ4',
                image='https://lh5.googleusercontent.com/p/AF1QipNkmO06tYCHigPl25qC1zyJcmz9E70R51cvaFFi=w408-h306-k-no',
                reported='2020-02-09 09:14:34.514533')


    @classmethod
    def setUpClass(cls):
        app.config.from_object(test_db_cfg)

    def setUp(self) -> None:
        db.drop_all()
        db.create_all()
        self.dalstore = DALStore()
        self.store_list = []
        for x in range(1, 5, 1):
            self.store_list.append(PryceMockStoreFactory())

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_get(self):
        stores = self.dalstore.get()
        self.assertIsNotNone(stores)
        self.assertCountEqual(stores, self.store_list)

    def test_add_store_with_dict(self):
        dict = {'name': 'Harris Teeter', 'place_id': 'ChIJFcCvnkuIsIkRmuUL7bEw_fM', 'reported': datetime.now()}
        store = self.dalstore.add_store_with_dict(dict)
        self.assertIsNotNone(store)
        self.assertEqual(store.store_id, 5)

    def test_add_bad_store(self):
        dict = {'name': 'Foo'}
        item = self.dalstore.add_store_with_dict(dict)
        self.assertIsNone(item)

    def test_get_store_by_place_id(self):
        dict = {'name': 'Harris Teeter', 'place_id': 'ChIJFcCvnkuIsIkRmuUL7bEw_fM', 'reported': datetime.now()}
        self.dalstore.add_store_with_dict(dict)
        s = self.dalstore.get_store_by_place_id(dict['place_id'])
        self.assertIsNotNone(s)
        self.assertEqual(s.name, "Harris Teeter")

    def test_update_store(self):
        dict1 = {'name': 'Harris Teeter', 'place_id': 'ChIJFcCvnkuIsIkRmuUL7bEw_fM', 'reported': datetime.now()}
        store1 = self.dalstore.add_store_with_dict(dict1)
        dict2 = {'store_id': store1.store_id, 'lat': 37.248923, 'lng': -76.686613, 'reported': datetime.now()}
        store1.update(dict2)
        store2 = self.dalstore.update_store(store1)
        self.assertEqual(store2.name, 'Harris Teeter')
        self.assertEqual(store2.place_id, 'ChIJFcCvnkuIsIkRmuUL7bEw_fM')
        self.assertEqual( store2.store_id, store1.store_id)

    def test_delete_item(self):
        dict1 = {'name': 'Harris Teeter', 'place_id': 'ChIJFcCvnkuIsIkRmuUL7bEw_fM', 'reported': datetime.now()}
        store = self.dalstore.add_store_with_dict(dict1)
        self.assertEqual(self.dalstore.delete_store(store), 1)
        item2 = self.dalstore.get_store_by_place_id(store.place_id)
        self.assertIsNone(item2)
