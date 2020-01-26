# Just a test app to get the deployment and DB connection stuff straight...
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

@app.route('/create_db')
def create_db():
    db.create_all()

@app.route('/items', methods=['POST'])
def add_item():
    content = request.get_json()
    print(content)
    name = content['name']
    barcode= content['barcode']
    db.session.add(Item(name, barcode))
    db.session.commit()
    return '', 200

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
