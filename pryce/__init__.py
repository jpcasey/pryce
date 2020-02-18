__all__ = ['app', 'jwt']

from flask import Flask, request, jsonify, render_template
from pryce.config import Config
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

import pryce.controllers.items as items_controller
import pryce.controllers.stores as stores_controller
import pryce.controllers.prices as prices_controller
import pryce.controllers.auth as auth_controller
from pryce.controllers.pryce_lists import pryce_lists_bp, pryce_lists

# don't require trailing slash after endpoints
app.url_map.strict_slashes = False
app.register_blueprint(items_controller.bp)
app.register_blueprint(stores_controller.bp)
app.register_blueprint(prices_controller.bp)
app.register_blueprint(auth_controller.bp)
app.register_blueprint(pryce_lists_bp)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')