import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    '''if os.environ.get('ENV_TYPE') == 'GCP':
        # Build the database connection string for our Google Cloud Platform PostgreSQL instance
        db_user = os.environ.get('DB_USER')
        db_pass = os.environ.get('DB_PASS')
        db_name = os.environ.get('DB_NAME')
        instance_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
        #db_connection_string = 'postgres+pg8000://{}:{}@/{}?unix_sock=/cloudsql/{}/.s.PGSQL.5432'.format(db_user, db_pass, db_name, instance_connection_name)
        db_connection_string = 'postgresql://{}:{}@{}?unix_sock=/cloudsql/{}/.s.PGSQL.5432'.format(db_user, db_pass, db_name, instance_connection_name) 
    else:
        # use local sqlite db. We might want to use SQL Proxy to develop locally with Google DB https://cloud.google.com/sql/docs/postgres/sql-proxy
        db_connection_string = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or db_connection_string

