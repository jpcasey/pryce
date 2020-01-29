from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pryce.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from pryce.database.models import *
import pryce.controllers.items as items
import pryce.controllers.stores as stores

# don't require trailing slash after endpoints
app.url_map.strict_slashes = False
app.register_blueprint(items.bp)
app.register_blueprint(stores.bp)

@app.route('/login')
def login():
    usr = Appuser(username='testing3')
    db.session.add(usr)
    db.session.commit()
    #return render_template('login.html')
    return "Looks good"

@app.route('/')
def root():
    return render_template('index.html')
