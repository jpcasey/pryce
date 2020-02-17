from flask import jsonify, request
from marshmallow import ValidationError
from pryce.database.schemas import PryceListSchema, PryceListItemSchema
from pryce.controllers.pryce_lists import pryce_lists_bp as bp
from pryce.database.models import PryceList, PryceListItem
from pryce.database.dal.pryce_list import DALPryceList

dal_pl = DALPryceList()

# /- POST
# Adds a list to the user's profile
@bp.route('/', methods=['POST'])
def create_list():
    req_body = request.get_json()
    try:
        pls = PryceListSchema()
        req_list = pls.load(data=req_body)
    except ValidationError as ve:
        #logging.DEBUG(ve)
        return jsonify(message='Invalid JSON'), 400
    sqa_list = dal_pl.create_pryce_list(req_list)
    #TODO: document this for client-side
    return PryceListSchema.jsonify(sqa_list)


# /<pryce_list_id> - PUT
# Adds an item to an exising pryce_list
@bp.route('/<pryce_list_id>', methods=['PUT'])
def add_items_to_list(pryce_list_id):
    req_body = request.get_json()
    item_id = req_body['item_id']
    quant = req_body['quantity']
    if not item_id or not quant:
        return jsonify(message='Invalid JSON. Missing item'), 400
    pli_obj = dal_pl.update_pryce_list(pryce_list_id, item_id, quant)
    pls = PryceListItemSchema()
    mas_json = pls.dump(pli_obj)
    #TODO: document format of this returned JSON for client-side
    return mas_json, 200
