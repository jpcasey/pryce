from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from pryce.database.schemas import PryceListSchema, PryceListItemSchema, ItemSchema
from pryce.controllers.pryce_lists import pryce_lists_bp as bp
from pryce.database.dal.pryce_list import DALPryceList

dal_pl = DALPryceList()


# /- GET
@bp.route('/', methods=['GET'])
@jwt_required
def get_lists():
    ident = get_jwt_identity()
    sqa_lists = dal_pl.get_pryce_lists(ident.get('appuser_id'))
    lpls = PryceListSchema(many=True)
    json = lpls.dumps(sqa_lists)
    return json, 200


# /- POST
# Adds a list to the user's profile and returns it
@bp.route('/', methods=['POST'])
@jwt_required
def create_list():
    req_body = None;
    try:
        req_body = request.get_json()
    except ValueError as ve:
        return jsonify(message='Invalid JSON'), 400

    tmp = {};
    tmp['owner'] = get_jwt_identity().get('appuser_id')
    tmp['name'] = req_body;
    pl_sqlao = dal_pl.create_pryce_list(tmp)
    schemaDump = PryceListSchema().dump(pl_sqlao)
    return schemaDump, 200


# /<pryce_list_id> - PUT
# Adds an item to an exising pryce_list
@bp.route('/<pryce_list_id>', methods=['PUT'])
@jwt_required
def add_items_to_list(pryce_list_id):
    req_body = request.get_json()
    item_id = req_body['item_id']
    quant = req_body.get('quantity', 1)
    if not item_id or not quant:
        return jsonify(message='Invalid JSON. Missing item'), 400
    pli_obj = dal_pl.update_pryce_list(pryce_list_id, item_id, quant)
    mas_json = PryceListItemSchema().dump(pli_obj)
    return mas_json, 200


# /<pryce_list_id> - GET
# Gets items for list
@bp.route('/<pryce_list_id>', methods=['GET'])
@jwt_required
def get_list_items(pryce_list_id):
    pl_items = dal_pl.get_pryce_list_items(pryce_list_id)
    mas_json = ItemSchema(many=True).dump(pl_items)
    return jsonify(mas_json), 200


# TODO: decide what exactly is needed by client
# /details/<pryce_list_id> - GET
# Gets item, price and location details for items in a list
@bp.route('/details/<pryce_list_id>', methods=['GET'])
@jwt_required
def get_list_details(pryce_list_id):
    result = dal_pl.get_detailed_pryce_list(pryce_list_id)
    dicts = []
    for r in result:
        dicts.append(dict(r))
    json = jsonify(dicts)
    return json, 200
