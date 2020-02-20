from pryce.database.models import PryceListItem, PryceList
from pryce.database.dal import db


class DALPryceList:

    def get_pryce_lists(self, appuser_id):
        plists = PryceList.query.filter_by(owner=appuser_id).all()
        return plists

    def create_pryce_list(self, ma_list):
        db.session.add(ma_list)
        db.session.commit()
        return ma_list

    def update_pryce_list(self, pryce_list_id, item_id, quant):
        """
        Updates the price_list_item table, adding an entry if necessary. Note that pryce_list_id and item_id form a
        composite key.
        :param pryce_list_id:
        :param item_id:
        :param quant: an integer >= 1
        :return: a PryceListItem object representing the updated (or newly created) record
        """
        pli = PryceListItem.query.filter_by(pryce_list_id=pryce_list_id, item_id=item_id).first()
        # if the list exists, but has no items (ie. does not have a record in pryce_list_item table)
        if pli is None:
            pli = PryceListItem()
            pli.pryce_list_id = pryce_list_id
            pli.item_id = item_id
            pli.quantity = quant
            db.session.add(pli)
            db.session.commit()
        else:
            pli.quantity = quant
            db.session.commit()
        return pli
