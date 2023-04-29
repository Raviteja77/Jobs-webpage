from flask_login import UserMixin
from app import db
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    email = db.Column(db.String(64))
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))
    
    job_listings = db.relationship('Job', backref='users', lazy='dynamic')


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(140), nullable=False)
    salary_range = db.Column(db.String(140), nullable=False)
    company = db.Column(db.String(140), nullable=False)
    job_category = db.Column(db.String(64), nullable=False)
    job_description = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(140), nullable=False)
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    closed = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))