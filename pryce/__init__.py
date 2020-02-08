from flask import Flask, request, jsonify
from pryce.config import Config
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.config.from_object(Config)
ma = Marshmallow(app)

jwt = JWTManager(app)

import pryce.controllers.items as items_controller
import pryce.controllers.stores as stores_controller
import pryce.controllers.price as price_controller

# don't require trailing slash after endpoints
app.url_map.strict_slashes = False
app.register_blueprint(items_controller.bp)
app.register_blueprint(stores_controller.bp)
app.register_blueprint(price_controller.bp)

# route to authenticate users and create & provide access tokens.
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"message": "Missing username parameter"}), 400
    if not password:
        return jsonify({"message": "Missing password parameter"}), 400

    # mock user/passwords for testing
    valid_users = {
        'user1': 'Pa55word',
        'user2': 'Pa55word'
    }

    if username not in valid_users or valid_users[username] != password:
        return jsonify({"message": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# route that is restricted to anyone with a JWT
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user, message="Hello from a protected route!"), 200

# route that only logged in, authorized users can see
@app.route('/user2', methods=['GET'])
@jwt_required
def partially_protected():
    authorized_users = ['user2']
    current_user = get_jwt_identity()
    if current_user not in authorized_users:
        return jsonify(logged_in_as=current_user, message="You are not allowed to view this resource."), 403
    return jsonify(logged_in_as=current_user, message="Welcome to your profile! Nobody else can see this."), 200
