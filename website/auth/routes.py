from flask import Blueprint, render_template, flash, redirect, request, url_for
from website import db, bcrypt
from website.auth.forms import *
from website.auth.utils import *
from website.models import *
from flask_login import login_user, current_user, logout_user



auth = Blueprint('auth', __name__)

already_auth_msg = 'Already authenticated, do not need to register again :)'

@auth.route('/login', methods=['GET','POST'])
def login():

    if current_user.is_authenticated:
        flash(already_auth_msg, 'success')
        return redirect(url_for('main.home'))

    form = Login()

    if form.validate_on_submit():

        email = User.query.filter_by(email=form.email.data).first()
        if email and bcrypt.check_password_hash(email.password, form.password.data):
            login_user(email, remember=form.remember.data)
            next_page = request.args.get('next') # access page user is trying to access without login
            flash(f'Logged in with email: {form.email.data}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))

        else:
            flash(f'Username or Password wrong', 'danger')

    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('main.home'))

@auth.route('/register', methods=['GET','POST'])
def register():

    if current_user.is_authenticated:
        flash(already_auth_msg, 'info')
        return redirect(url_for('main.home'))

    form = Register()

    if form.validate_on_submit():
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        needcurr = request.form.getlist('needcurr')
        offrcurr = request.form.getlist('offercurr')

        
        input_from_form = User(
        email = form.email.data,
        name = form.name.data,
        surname = form.surname.data,
        password = hashed_password,
        fb = form.fb.data,
        wa = form.wa.data,
        needcurr = ','.join(needcurr),
        offrcurr = ','.join(offrcurr)
        )

        db.session.add(input_from_form)
        db.session.commit()

        flash(f'Success, {form.email.data}', 'success')

        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth.route('/reset_password', methods=['GET','POST'])
def reset_request():
    form = RequestResetForm()
    if current_user.is_authenticated:
        logout_user()
        flash('Logged out. Please continue using your email', 'info')
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_resend_email(user)
        flash(f"An email has been sent to {form.email.data}. Please check also the spam folder if you can't find it.", 'info')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', form=form)


@auth.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_token.html', form=form)
