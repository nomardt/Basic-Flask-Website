from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_required, current_user, login_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Checks POSTed email & passwd against the database"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()

        if user and password and check_password_hash(user.password, password):
            flash('Logged in!', category='success')
            login_user(user, remember=True)
            return redirect('/')
        else:
            flash('Incorrect email or password!', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    """Default flask_login logout, redirection to login"""
    logout_user()
    flash("You've logged out!", category='error')
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """Gets email, passwd1, passwd2; Compares passwd1 passwd2; If success redirect /"""
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if len(email) < 5:
            flash('Email length must be greater than 4 characters!', category='error')
        elif len(password1) < 8 or not password1.isalnum():
            print(type(password1), password1, len(password1), sep='\n')
            flash("Something's wrong with the password! It should be alfanumerical and longer than 7 characters...", category='error')
        elif password1 != password2:
            flash("Passwords do not match...", category='error')
        else:
            try:
                new_user = User(email=email, password=generate_password_hash(password1))
                db.session.add(new_user)
                db.session.commit()
                flash("Account created!", category='success')
                login_user(new_user, remember=True)
                return redirect('/')
            except:
                flash("A user with this email already exists!", category='error')

    return render_template("signup.html", user=current_user)

