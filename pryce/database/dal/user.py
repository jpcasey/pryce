from pryce.database.models import Appuser
from pryce.database.dal import db


class DALUser:

    def get_password_for_username(self, name):
        user = Appuser.query.filter_by(username=name).first()
        return user

    def user_add(self, user):
        db.session.add(user)
