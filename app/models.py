from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    email = db.Column(db.String(64))
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))
    