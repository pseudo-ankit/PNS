import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'f02f560898fef9da7266a7ae9f7d1d69'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                            'mysql://root:@localhost/pns_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
