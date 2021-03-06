import os
import logging

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    if os.getenv('GOOGLE_CLOUD_PROJECT'):
        from google.cloud import datastore
        client = datastore.Client()
        query = client.query(kind='database')
        result = list(query.fetch())
        #assume that only one entity in 'database' kind; so result size is one         
        csql_instance = result[0]['csql_instance']
        csql_database = result[0]['csql_database']
        csql_user = result[0]['csql_user'] 
        csql_pass = result[0]['csql_pass']
        csql_connection_string =\
                'postgres+psycopg2://{}:{}@/{}?host=/cloudsql/{}'.format(\
            csql_user, csql_pass, csql_database, csql_instance)
            #'postgres+pg8000://{}:{}@/{}?unix_sock=/cloudsql/{}/.s.PGSQL.5432'.format(\
        if os.getenv('FLASK_ENV') == 'development':
            logging.debug("csql_connection_string: " + csql_connection_string)
        SQLALCHEMY_DATABASE_URI = csql_connection_string

        # get our google maps api & JWT secret keys
        query = client.query(kind='api_key')
        result = list(query.fetch())
        GOOGLE_API_KEY = result[0]['google']
        JWT_SECRET_KEY = result[0]['JWT_SECRET_KEY']
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
        GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
        JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
