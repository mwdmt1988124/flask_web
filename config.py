import os
#basedir = os.base.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[民生保险]'
    FLASKY_MAIL_SENDER = 'Flasky Admin<13641920160@163.com>'
    FLASKY_ADMIN = '344054296@qq.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG =True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123456@localhost/flask_web?charset=utf8"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123456@localhost/flask_test?charset=utf8"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123456@localhost/flask_web?charset=utf8"

config = {'development':DevelopmentConfig,
          'testing':TestingConfig,
          'production':ProductionConfig,
          'default':DevelopmentConfig}