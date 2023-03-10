from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . models import User
from . import db

auth = Blueprint('auth',__name__)

@auth.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
        
            else:
                flash('Incorrect password, try again', category='error')
        
        else:
            flash('Email does not exists', category='error')

    return render_template('login.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET','POST'])
def sign_up():
    if request.method == 'POST' :
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        passwrod2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category='error')

        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(name) < 2:
            flash('name must be greather than 1 character ', category='error')
        elif password1 != passwrod2:
             flash('passwords don\'t matches ', category='error')
        elif len(password1) < 7:
            flash('password1 must be at least 7 characters ', category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('account created !', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user = current_user)