from sqlalchemy.exc import IntegrityError
from pryce.database.dal import db
from pryce.database.models import PryceList

class DALPryceList:

    def create_list(ma_list):
        db.session.add(ma_list)
        db.session.commit()


