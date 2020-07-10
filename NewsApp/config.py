import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'f02f560898fef9da7266a7ae9f7d1d69'
    SQLALCHEMY_DATABASE_URI = 'YOUR_DATABASE_URI'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
