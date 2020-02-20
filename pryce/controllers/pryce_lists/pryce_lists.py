from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from pryce.database.schemas import PryceListSchema, PryceListItemSchema
from pryce.controllers.pryce_lists import pryce_lists_bp as bp
from pryce.database.dal.pryce_list import DALPryceList

dal_pl = DALPryceList()

# /- GET
# Adds a list to the user's profile
@bp.route('/', methods=['GET'])
@jwt_required
def get_lists():
    ident = get_jwt_identity()
    sqa_lists = dal_pl.get_pryce_lists(ident.get('appuser_id'))
    lpls = PryceListSchema(many=True)
    return lpls.dumps(sqa_lists), 200


# /- POST
# Adds a list to the user's profile and returns it
@bp.route('/', methods=['POST'])
@jwt_required
def create_list():
    req_body = request.get_json()
    try:
        pl_sqlao = PryceListSchema().load(transient=True, data=req_body)
    except ValidationError as ve:
        return jsonify(message='Invalid JSON'), 400
    pl_sqlao.owner = get_jwt_identity().get('appuser_id')
    pl_sqlao = dal_pl.create_pryce_list(pl_sqlao)
    return PryceListSchema().dump(pl_sqlao), 200


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
