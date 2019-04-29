'''
Created on 13 січ. 2019 р.

@author: YURA
'''
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    
   
    #'postgres://xczgdypqwigfgo:99c0cf16659cbde35b7d62bcea57e3c971f91058ee92e7f2780eaff0aac31a5f@ec2-107-20-183-142.compute-1.amazonaws.com:5432/ddasc41j3hnp5v'
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

    
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=465
    MAIL_USE_SSL=1
    MAIL_USERNAME = 'morozov.yra029@gmail.com'
    MAIL_PASSWORD= '12vivozu'
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    
    ADMINS = ['morziko2@gmail.com']
    
    POSTS_PER_PAGE = 20
    
    LANGUAGES = ['en', 'ukr' ]
    
    # ELASTICSEARCH_URL = 'http://localhost:9200'
    
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')