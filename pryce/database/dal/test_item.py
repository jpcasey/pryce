import os
import unittest

import psycopg2
import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pryce.database.models import Item
from pryce.database.dal.item import DALItem
from pryce import app
from pryce.database.dal import db
from pryce.database.dal import test_db_cfg


class TestDALItem(unittest.TestCase):
    TABLE = 'item'
    TRUNC_SQL = f"TRUNCATE {TABLE} CASCADE"
    SQL_FILE = 'mock_data.sql'
    # app = None
    # db = None
    mock_data = None

    @classmethod
    def setUpClass(self):
        # TestDALItem.app = Flask(__name__)
        app.config.from_object(test_db_cfg)
        print(os.getenv('SQLALCHEMY_DATABASE_URI'))
        '''
        db_uri = test_db_cfg['DATABASE_URI']
        db_admin = test_db_cfg['PG_ADMIN_USER']
        admin_db_name = test_db_cfg['PG_ADMIN_DBNAME']
        db_passwd = test_db_cfg['PG_PSSWD'] = os.getenv('PG_PSSWD')
        app.config['SQLALCHEMY_DATABASE_URI'] = test_db_cfg['ADMIN_DB_URI']
        conn = psycopg2.connect("dbname=postgres host=localhost user=chb password=F00m4tic!")
        cur = conn.cursor()
        cur.execute("DROP DATABASE pryce")
        conn.commit()
        #db.engine.execute("DROP DATABASE pryce")
        cur.execute("CREATE DATABASE pryce")
        cur.close()
        conn.close()
        #db.engine.execute("CREATE DATABASE pryce")
        db.create_all()
        '''

    '''
    def tearDownClass(self):
        db.drop_all()
    '''

    def setUp(self) -> None:
        db.drop_all()
        db.create_all()
        tjs = Item(code='0000000959742', brand="Trader Joe's", name='Turkey Jerky Teriyaki', quantity=4,
                   quant_unit='oz', description='Snap into a Slim Jim')
        db.session.add(tjs)
        db.session.commit()
        self.dalitem = DALItem()
        # get the file containing mock data
        #mock_data_f = open(TestDALItem.SQL_FILE, mode='r')
        # TestDALItem.mock_data = mock_data_f.read()
        #engine = sqlalchemy.create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'))
        #escaped_sql = sqlalchemy.text(mock_data_f.read())
        #result = engine.execute(escaped_sql)
        #mock_data_f.close()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_get_item(self):
        i = self.dalitem.get_item("0000000959742")
        self.assertEqual(i.brand, "Trader Joe's")

    '''def test_add_item():
        # i = Item()
        return True
    '''


if __name__ == '__main__':
    pass
