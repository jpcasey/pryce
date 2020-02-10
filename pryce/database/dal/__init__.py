__all__ = ['user', 'item', 'db', 'ma', 'migrate', 'test_db_cfg']

from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pryce import app

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

test_db_cfg = {}
test_db_cfg['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
test_db_cfg['FLASK_ENV'] = 'development'
test_db_cfg['TESTING'] = True


