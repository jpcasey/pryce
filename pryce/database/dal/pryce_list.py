from pryce.database.models import PryceListItem, PryceList, Item
from pryce.database.dal import db
from sqlalchemy import text

class DALPryceList:

    def get_pryce_lists(self, appuser_id):
        plists = PryceList.query.filter_by(owner=appuser_id).all()
        return plists

    def get_list_items(self, appuser_id):
        plists = PryceList.query.filter_by(owner=appuser_id).all()
        return plists

    def get_list_details(self, appuser_id):
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

    def get_pryce_list_items(self, pryce_list_id):
        items = db.query(PryceListItem).join(Item).filter_by(pryce_list_id=pryce_list_id).all()
        return items

    def get_detailed_pryce_list(self, pryce_list_id):
        plain_sql = """with table1 as
                (select row_number() over (partition by pri.item_id order by pri.reported desc) as rn,
                    pri.price, pri.item_id, pri.store_id, pri.reported from price pri ) 
                select itm.name, table1.item_id, table1.reported, table1.price, sto.place_id, sto.name
                  from item itm 
                    inner join table1 on table1.item_id = itm.item_id 
                    inner join store sto on table1.store_id = sto.store_id
                 where rn=1 and table1.item_id in 
                 (select pli.item_id from pryce_list_item pli where pli.pryce_list_id = {});""".format(pryce_list_id)
        sql = text(plain_sql)
        result = db.engine.execute(sql)
        return result
