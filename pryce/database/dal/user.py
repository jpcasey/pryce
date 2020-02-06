from pryce.database.models import Appuser
from pryce.database.dal import db


class DALUser:

    def get_password_for_username(self):
        pass

    def user_add(self, user):
        db.session.add(user)
