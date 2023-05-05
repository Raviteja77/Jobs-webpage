# Import necessary modules
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from os import path

# Initialize SQLAlchemy, set database name and Bootstrap
db = SQLAlchemy()
DB_NAME = "jobs_webapp.db"
bootstrap = Bootstrap()

# Create a Flask app
def create_app(config_name):
    app = Flask(__name__)

    # Load configuration from config.py file
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize the database and Bootstrap
    db.init_app(app)
    bootstrap.init_app(app)

    # Register the main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Import User model and create all tables
    from .models import User
    with app.app_context():
        db.create_all()

    # Initialize the LoginManager and set the login view
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    # Load the user by ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Return the Flask app
    return app
