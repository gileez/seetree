class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://gili:123@localhost/seedb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'seetree'
    PORT = '5000'
    DEBUG = True
    CELERY_BROKER_URL= 'amqp://guest:guest@rabbit:5672//'