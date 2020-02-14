from flask import jsonify, request
from marshmallow import ValidationError
from pryce.database.schemas import PryceListSchema
from pryce.controllers.pryce_lists import pryce_lists_bp as bp
from pryce.database.models import PryceList
from pryce.database.dal.pryce_list import DALPryceList

# /- POST
# Adds a list to the user's profile
@bp.route('/', methods=['POST'])
def create_list():
    req_body = request.get_json()
    try:
        ls = ListSchema()
        req_list = ls.load(data=req_body)
    except ValidationError as ve:
        return jsonify(message='Invalid JSON'), 400
    sqa_list = create_list(req_list)
    return ListSchema.jsonify(sqa_list)
