from flask import Blueprint, request, jsonify

bp = Blueprint('stores', __name__, url_prefix='/stores')

# / - GET
# Returns a list of stores in the system. Can be filtered using query parameters (e.g. name, location).
@bp.route('/', methods=['GET'])
def get_items():
    stores = [
        {'name': 'store1'},
        {'name': 'store2'},
        {'name': 'store3'},
    ]
    return jsonify({'message': 'Here are all the stores!!!', 'stores': stores})

# /- POST
# Adds a store to the database.
@bp.route('/', methods=['POST'])
def add_store():
    content = request.get_json()
    print(content)
    name = content['name']
    message = f'Added store {name}'
    return jsonify(message)

# /<store_id> - GET
# Returns information for a specific store.

# /<store_id> - PUT
# Update information for a specific store.

# /<store_id> - DELETE
# Deletes a store from the system.

# /<store_id>/items - GET
# Returns information on all items at a specific store.  Can be filtered using query parameters (e.g. name, brand, price, date last verified).

# /<store_id>/items/<item_id> - GET
# Returns information for a specific item at a specific store, including price

# /<store_id>/items/<item_id> - POST
# Adds price information for a specific item at a specific store.

# /<store_id>/items/<item_id> - PUT
# Updates price information for a specific item at a specific store.

# /<store_id>/items/<item_id> - DELETE
# Deletes price information for a specific item at a specific store.

# /<store_id>/items/<item_id>/comments - GET
# Returns all comments and ratings for a specific item at a specific store.

# /<store_id>/items/<item_id>/comments - POST
# Adds a comment and rating for a specific item at a specific store.

# /<store_id>/items/<item_id>/comments/<comment_id> - PUT
# Update a comment and rating for specific item at a specific store.

# /<store_id>/items/<item_id>/comments/<comment_id> - DELETE
# Deletes a comment and rating for a specific item at a specific store.
