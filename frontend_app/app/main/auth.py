from flask import render_template, redirect, flash, request
from flask_login import login_required
from app import db
from app.models import User
from .forms import LoginForm, RegisterForm
from . import main
from flask import render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

@main.route('/login', methods=['GET', 'POST'])
def login():
    # if request method is POST, attempt to login with provided email and password
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # query the database for the user with the provided email
        user = User.query.filter_by(email=email).first()
        if user:
            # check if provided password matches the hashed password in the database
            if check_password_hash(user.password, password):
                # if password is correct, log the user in and redirect to index page
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('main.index'))
            else:
                # if password is incorrect, display error message
                flash('Incorrect password, try again.', category='error')
        else:
            # if user with provided email does not exist, display error message
            flash('Email does not exist.', category='error')
    
    # if request method is GET, display login form
    loginForm = LoginForm()
    return render_template("login.html", form=loginForm, user=current_user)

@main.route('/logout')
@login_required
def logout():
    # log the user out and redirect to login page
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('main.login'))

@main.route("/register", methods=["POST", "GET"])
def register():
    # if request method is POST, attempt to create a new user
    if request.method == 'POST':
        # get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # check if user with provided email already exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            # if user already exists, display error message
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            # if email is too short, display error message
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            # if first name is too short, display error message
            flash('First name must be greater than 1 character.', category='error')
        elif len(password) < 7:
            # if password is too short, display error message
            flash('Password must be at least 7 characters.', category='error')
        else:
            # create a new user with provided data, hash the password, and add to database
            new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=generate_password_hash(
                password, method='sha256'), role=role)
            db.session.add(new_user)
            db.session.commit()
            # log the new user in and redirect to index page
            login_user(new_user, remember=True)
            flash('Account created! and successfully Logged in', category='success')
            return redirect(url_for('main.index'))
    
    # if request method is GET, display registration form
    registerForm = RegisterForm()
    return render_template("register.html", form=registerForm, user=current_user)
