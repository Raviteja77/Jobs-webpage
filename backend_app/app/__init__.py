from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "jobs_webapp.db"

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app) 

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)
    
    return app


def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)