import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    # app
    SECRET_KEY = os.environ.get("SECRET_KEY") or "You will never guess"
    # db
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        'sqlite:///' + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['n.wang.travel@gmail.com']
    # page
    POSTS_PER_PAGE = 2
    # lang
    LANGUAGES = ['en', 'zh', 'fr']
    # search
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    # Log
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    # Redis
    REDIS_URL = os.environ.get("REDIS_URL") or 'redis://'
