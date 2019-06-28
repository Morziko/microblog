'''
Created on 13 січ. 2019 р.

@author: YURA
'''
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://***:1****@localhost/***'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

    
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=465
    MAIL_USE_SSL=1
    MAIL_USERNAME = '***'
    MAIL_PASSWORD= '***'
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    
    ADMINS = ['***', '***']
    
    POSTS_PER_PAGE = 20
    
    LANGUAGES = ['ukr', 'en']
    
    # ELASTICSEARCH_URL = 'http://localhost:9200'
    
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True