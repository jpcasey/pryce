__all__ = ['user', 'item', 'db', 'test_db_cfg']

from flask import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pryce import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)

test_db_cfg = {}
test_db_cfg['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
test_db_cfg['FLASK_ENV'] = 'development'
test_db_cfg['TESTING'] = True


'''
test_db_cfg['PG_HOST'] = 'localhost'
test_db_cfg['PG_ADMIN_USER'] = 'postgres'
test_db_cfg['PG_ADMIN_DBNAME'] = 'postgres'
test_db_cfg['PG_USER'] = 'pryce_admin'
test_db_cfg['PG_DBNAME'] = 'pryce'
test_db_cfg['PG_PSSWD'] = ''
test_db_cfg['DATABASE_URI'] = 'postgresql+psycopg2://{0}:{1}@{2}/{3}'

'''
