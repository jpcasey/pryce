__all__ = ["user", "item"]

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pryce import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)

'''
class DALBase():
    db = None

    def __init__(self):
        db = SQLAlchemy(app)
        migrate = Migrate(app, db)
'''

