from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        password = request.form.get('password')

        user = User.query.filter_by(first_name=first_name).first()
        if user:
            if check_password_hash(user.password, password):
                if user.type == 'admin' or user.type == 'dansator' :
                    flash('Logged in successfuly!')
                    login_user(user, remember=True)
                    return redirect(url_for('views.adminHome'))
                else:
                    flash('This account has not been activated')
            else:
                flash('Incorrect password, try again')
        else:
            flash('user does not exist')
    return render_template("admin/login.html", user=current_user)


@auth.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/admin/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(first_name=first_name).first()
        if user:
            flash('User already exist.', category='error')
        elif len(first_name) < 2:
            flash('First Name must be greater than 2 characters', category='error')
        elif password1 != password2:
            flash('password must be match', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters', category='error')
        else:
            new_user = User(first_name=first_name,
                            password=generate_password_hash(password1, method='sha256'), type='new')
            db.session.add(new_user)
            db.session.commit()
            # login_user(new_user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("admin/sign-up.html", user=current_user)
