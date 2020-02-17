from pryce.database.models import PryceListItem
from pryce.database.dal import db


class DALPryceList:

    def create_pryce_list(self, ma_list):
        db.session.add(ma_list)
        db.session.commit()
        return ma_list

    def update_pryce_list(self, list_id, item_id, quant):
        pli = PryceListItem.query.filter_by(pryce_list_id=list_id, item_id=item_id).first()
        # if the list exists, but has no items (ie. does not have a record in pryce_list_item table)
        if pli is None:
            pli = PryceListItem()
            pli.pryce_list_id = list_id
            pli.item_id = item_id
            db.session.add()
        pli.quantity = quant
        db.session.commit()
        return pli
