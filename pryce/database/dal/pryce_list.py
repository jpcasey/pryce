from pryce.database.dal import db

class DALPryceList:

    def create_pryce_list(self, ma_list):
        db.session.add(ma_list)
        db.session.commit()
        return ma_list

    def update_pryce_list(self, list_id, item_id):
        pass
