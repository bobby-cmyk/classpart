from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required
from yourapp.models import db, User
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('general.index'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():

    session.pop('custom_data', None)
    logout_user()
    return redirect(url_for('general.index'))

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username:
            flash('Username cannot be blank', 'danger')
            return redirect(url_for('auth.signup'))

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('auth.signup'))

        email_exists = User.query.filter_by(email=email).first() is not None

        if email_exists:
            flash('Email is already registered', 'warning')
            return redirect(url_for('auth.signup'))

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, email=email, password_hash=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except SQLAlchemyError as e:  # Catching general SQLAlchemy errors
            db.session.rollback()  # Roll back the session to a clean state
            flash('An error occurred while creating your account. Please try again.', 'danger')

    return render_template('signup.html')


