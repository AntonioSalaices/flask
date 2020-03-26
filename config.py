import os
class Config(object):
    SECRET_KEY="my_secret_key"
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL= False
    MAIL_USE_TLS= True
    MAIL_USERNAME= 'antonio.salaicesm@gmail.com'
    MAIL_PASSWORD='*'

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:@localhost/flask'
    SQLALCHEMY_TRACK_MODIFICATIONS= False

