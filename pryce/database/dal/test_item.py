from flask_migrate import Migrate
from pryce.database import models
from database import models
import os
import inspect

def pathtest():
    print(os.getcwd())
    migrate_dir = os.path.dirname(inspect.getfile(inspect))
    migrate_dir += os.path.join(migrate_dir, "database", "migrations")
    print(migrate_dir)

class TestDALItem(unitest.TestCase):

    migrate_dir = ''
    def __init__():
        #https://stackoverflow.com/a/12154601/148680 
        migrate_dir = os.path.dirname(inspect.getfile(inspect))
        migrate_dir += os.path.join(migrate_dir, "database", "migrations")

    def setUp(self):
        app.config.from_object(Config)
        db = SQLAlchemy(app)
        migrate = Migrate(app, db, directory=migrate_dir) 

    def tearDown(self): 
        app.config.from_object(Config)
        db = SQLAlchemy(app)
        db.drop_all()

    def test_add_item():
        #i = Item()
        return True

if __name__ == '__main__':
    pathtest()
