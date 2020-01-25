# Just a test app to get the deployment and DB connection stuff straight...
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

if os.environ.get('ENV_TYPE') == 'GCP':
    # Build the database connection string for our Google Cloud Platform PostgreSQL instance
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASS')
    db_name = os.environ.get('DB_NAME')
    instance_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
    db_connection_string = 'postgres+pg8000://{}:{}@/{}?unix_sock=/cloudsql/{}/.s.PGSQL.5432'.format(db_user, db_pass, db_name, instance_connection_name)
else:
    # use a local sqlite db. We might want to use SQL Proxy to develop locally with the Google DB https://cloud.google.com/sql/docs/postgres/sql-proxy
    db_connection_string = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_connection_string
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    barcode = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name, barcode):
        self.name = name
        self.barcode = barcode

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