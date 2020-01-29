from flask import Blueprint, request, jsonify

bp = Blueprint('items', __name__, url_prefix='/items')

# mocks for testing some of the routes
mock_items = [
    { 
        'id': '1',
        'name': 'item1',
        'code': '1823924829'
    },
    { 
        'id': '2',
        'name': 'item2',
        'code': '923481239'
    },
]

# / - GET
# Returns a list of items in the system.  Can be filtered using query parameters (e.g. name, brand)
@bp.route('/', methods=['GET'])
def get_items():
    return jsonify({'items': mock_items})

# /- POST
# Adds an item to the system.
@bp.route('/', methods=['POST'])
def add_item():
    content = request.get_json()
    print(content)
    name = content['name']
    barcode= content['barcode']
    message = f'Added item {name}, {barcode}'
    return jsonify(message)

# /<item_id> - GET
# Returns information for a specific item.
@bp.route('/<item_id>', methods=['GET'])
def get_item(item_id):
    item = None
    for mock_item in mock_items:
        print(mock_item)
        print(item_id)
        if mock_item['id'] == item_id:
            item = mock_item
    
    if item != None:
        return jsonify({'message': 'Here\'s your item!', 'item': item})
    else:
        return jsonify({'message': 'Item not found'}), 404

# /<item_id> - PUT
# Update information for a specific item.
@bp.route('/<item_id>', methods=['PUT'])
def update_item(item_id):
    item = {'name': 'item' + item_id, 'price': 8.00},

    return jsonify({'message': 'Here\'s your item!', 'item': item})

# /<item_id> - DELETE
# Deletes an item from the system.
@bp.route('/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = {'name': 'item' + item_id, 'price': 8.00},

    return jsonify({'message': 'Here\'s your item!', 'item': item})

# /<item_id>/prices - GET
# Returns store & price information for a specific item.  Can be filtered using query parameters (e.g. store, location, price, date last verified).
@bp.route('/<item_id>/prices', methods=['GET'])
def get_item_prices(item_id):
    item = {'name': 'item' + item_id, 'price': 8.00},

    return jsonify({'message': 'Here\'s your item!', 'item': item})