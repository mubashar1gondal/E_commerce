from flask_login import login_user, logout_user
from flask import flash, redirect, url_for, render_template, request
from flask_login.utils import login_required
from app.blueprints.authentication.models import User
from .import bp as auth


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out successfully', 'warning')
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user is None or not user.check_password(request.form.get('password')):
            flash('Either that user does not exist or the password is incorrect. Try again', 'warning')
            return redirect(url_for('auth.login'))
        remember_me = True if request.form.get('checked') is not None else False
        login_user(user, remember=remember_me)
        flash(f'Welcome, {user.first_name} {user.last_name}! You have successfully logged in!', 'success')
        return redirect(url_for('main.home'))
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = User()
        u.from_dict(request.form)
        u.save()
        flash("You have Registered", 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')