import os


class Config:
    SECRET_KEY = '0917b13a9091915d54b6336f45909539cce452b3661b21f386418a257883b30a'
    PROJECT_ID = os.environ.get('PROJECT_ID')
    DATA_BACKEND = os.environ.get('DATA_BACKEND')
    CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
    CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
    CLOUDSQL_DATABASE = os.environ.get('CLOUDSQL_DATABASE')
    CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://{user}:{password}@localhost/{database}?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD, database=CLOUDSQL_DATABASE,
        connection_name=CLOUDSQL_CONNECTION_NAME)
#    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENDPOINT_ROUTE = 'http://habby.thinger.appspot.com'
    GET_CAT_URL = '/event/cat/get_sorted'
    ADD_HABIT_URL = '/event/habit/attach'
    NORMAL_REGISTER_URL = '/register'
    LOGIN_URL = '/login'
    USER_HABIT_DATA_URL = '/event/habit/get_all'
    RECORD_ACTIVITY_URL = '/event/activity/report'
