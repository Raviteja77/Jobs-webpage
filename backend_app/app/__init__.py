from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from os import path

# create a SQLAlchemy object
db = SQLAlchemy()

# set the name of the database
DB_NAME = "jobs_webapp.db"

def create_app(config_name):
    # create a Flask app
    app = Flask(__name__)
    
    # load configuration from config.py
    app.config.from_object(config[config_name])
    
    # initialize the configuration
    config[config_name].init_app(app) 

    # initialize the SQLAlchemy object with the Flask app
    db.init_app(app)

    # import and register the main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # create the database tables
    with app.app_context():
        db.create_all()

    # initialize the LoginManager for user authentication
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)
    
    # return the Flask app
    return app
