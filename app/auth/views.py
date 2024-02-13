from flask import render_template, redirect, request, url_for, flash
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm, PasswdChangeForm, ChangeEmailForm, YesNoForm
from flask_login import current_user, login_required, login_user, logout_user
from .. import db
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_passwd(form.password.data):
            login_user(user, form.remember_me.data)
            '''
                Here (request.args.get('next')) returns the url of the page that the user was trying to
                access before being redirected to login page.
            '''
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data.strip())
        db.session.add(user)
        db.session.commit()
        login_user(user)
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.', 'info')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>', methods=['GET', 'POST'])
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,
               'Confirm Your Account',
               'auth/email/confirm',
               user=current_user,
               token=token)
    flash('A new confirmation email has been sent to you by email.', 'info')
    return redirect(url_for('main.index'))


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswdChangeForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Password has been updated!', 'info')
        return redirect(url_for('main.index'))
    return render_template('auth/pass_change.html', form=form)


@auth.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    form = YesNoForm()
    if form.is_submitted():
        if form.yes_button.data:
            user = User.query.filter_by(email=current_user.email).first()
            logout_user()
            db.session.delete(user)
            db.session.commit()
            flash('Account deleted successfully!', 'info')
        return redirect(url_for('main.index'))
    print(url_for('static', filename='images/delete.png', _external=True))
    return render_template('auth/delete_account.html', form=form, image_url=url_for('static', filename='images/delete.png'))


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Email has been updated!', 'info')
        return redirect(url_for('main.index'))
    return render_template('auth/email_change.html', form=form)
