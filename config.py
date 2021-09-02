import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('You will fucked')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ToDoS.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
