from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from pryce import jwt
from pryce.database.models import Appuser
from pryce.database.dal.user import DALUser

user_dal = DALUser()

bp = Blueprint('auth', __name__, url_prefix='/')

'''@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return identity
'''

# /register - POST
# Takes a JSON object with a 'username' and 'password'
# Returns HTTP 400 (Bad Request) if missing parameters or password does not meet minimum complexity requirement.
# Returns HTTP 409 (Conflict) if the provided username is already taken.
# Returns HTTP 200 (OK) when the user has been registered successfully.
@bp.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify(message="Missing JSON in request"), 400

    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify(message="Missing username or password parameter."), 400

    # make sure password meets minimum length
    MINIMUM_PASSWORD_LENGTH = 8
    if len(password) < MINIMUM_PASSWORD_LENGTH:
        return jsonify(message=f"Password must be {MINIMUM_PASSWORD_LENGTH} characters or longer."), 400

    password_hash = generate_password_hash(password)

    user = Appuser(username=username, password=password_hash)

    try:
        user_dal.add_user(user)
    except:
        return jsonify(message="Username already taken."), 409
    
    return jsonify(message="User successfully added."), 200

# /login - POST
# Takes a JSON object with a 'username' and 'password'
# Returns HTTP 400 (Bad Request) if missing parameters or password does not meet minimum complexity requirement.
# Returns HTTP 401 (Unauthorized) if username or password is invalid.
# Returns HTTP 200 (OK) and a JWT upon successful authentication. JWT should be passed in Authentication header in 
# all subsequent requests by 'logged in' user.
@bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify(message="Missing JSON in request"), 400

    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify(message="Missing username or password parameter."), 400

    # get password for user
    user = user_dal.get_user(username)

    if not user or not check_password_hash(user.password, password):
        # user didn't exist or password didn't match.
        return jsonify(message="Bad username or password."), 401

    identity = dict(username=username, appuser_id=user.appuser_id)
    access_token = create_access_token(identity=identity, expires_delta=False)
    return jsonify(message="Successfully authenticated.", access_token=access_token), 200


# The following are some test routes for testing authorization using provided JWTs
# route that is restricted to anyone with a JWT
@bp.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user, message="Hello from a protected route!"), 200

# route that only "user3" can view
@bp.route('/user3', methods=['GET'])
@jwt_required
def partially_protected():
    authorized_users = ['user3']
    current_user = get_jwt_identity()
    if current_user.get('username') not in authorized_users:
        return jsonify(logged_in_as=current_user, message="You are not allowed to view this resource."), 403
    return jsonify(logged_in_as=current_user, message="Welcome to your profile! Nobody else can see this."), 200
