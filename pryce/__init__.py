from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pryce.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from pryce.database.models import *

@app.route('/login')
def login():
    usr = Appuser(username='testing3')
    db.session.add(usr)
    db.session.commit()
    #return render_template('login.html')
    return "Looks good"

@app.route('/')
def root():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/items', methods=['POST'])
def add_item():
    content = request.get_json()
    print(content)
    name = content['name']
    barcode= content['barcode']
    brand = content['brand']
    weight = content['weight']
    description = content['description']
    db.session.add(Item(code=barcode, name=name, brand=brand, weight=weight, description=description))
    db.session.commit()
    return '', 200
