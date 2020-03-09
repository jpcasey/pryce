from pryce.database.models import Appuser
from pryce.database.dal import db

class DALUser:

    def get_user(self, name):
        user = Appuser.query.filter(Appuser.username.ilike(name)).first()
        return user

    def add_user(self, user):
        db.session.add(user)
        db.session.commit()
