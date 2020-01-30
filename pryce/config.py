import os
import logging

class Config(object):
    logger = logging.getLogger()
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
            'postgres+pg8000://{}:{}@/{}?unix_sock=/cloudsql/{}/.s.PGSQL.5432'.format(\
            #'postgres+psycopg2://{}:{}@/{}?unix_sock=/cloudsql/{}/.s.PGSQL.5432'.format(\
            csql_user, csql_pass, csql_database, csql_instance)
        logger.log("csql_connection_string: " + csql_connection_string)
        SQLALCHEMY_DATABASE_URI = csql_connection_string
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

