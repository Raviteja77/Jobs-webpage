from flask import render_template
from app.models import User
from . import main

@main.route("/")
def index():
    users = User.query.all()
    return render_template("home.html", users = users)