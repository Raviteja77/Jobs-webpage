
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = "mariadb://root:mysqlpassword@localhost/jobs_webapp"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "mscs3150"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default':DevelopmentConfig
}