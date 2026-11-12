
from flask import render_template, flash, redirect, url_for, session, request

from app import db
from app.auth import auth_blueprint as bp_auth 
import sqlalchemy as sqla
from app.auth.auth_forms import RegistrationForm, LoginForm, AdminRegistrationForm
from flask_login import login_user, logout_user, login_required, current_user
from app.main.models import Location, User, Admin, Driver
from app.auth.auth0_client import oauth

@bp_auth.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        form = RegistrationForm()
        user = User(username=form.username.data, email=form.email.data, address=form.address.data, user_type = form.user_type.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Admin Registration', form=form)

@bp_auth.route('/user/admin_register', methods=['GET', 'POST'])
def admin_register():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        admin = Admin(username=form.username.data, email=form.email.data, user_type = 'Admin', location_id=int(form.location.data))
        admin.set_password(form.password.data)
        db.session.add(admin)
        db.session.commit()
        flash('Congratulations, you are now a registered admin!')
        return redirect(url_for('auth.login'))
    return render_template('admin_register.html', title='Register', form=form)

@bp_auth.route('/user/driver_register', methods=['GET', 'POST'])  # <-- Unique route path and function name
def driver_register():                                          # <-- Renamed from register
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Driver(
            username=form.username.data,
            email=form.email.data,
            address=form.address.data,
            user_type='Driver'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Driver account successfully registered!')
        return redirect(url_for('auth.login'))
    return render_template(
        'register.html',
        title='Driver Registration',
        form=form
    )

@bp_auth.route('/user/login', methods=['GET', 'POST'])
def login():

    # Redirect users who are already logged in - need to review SSO more to make sure it works but I'll do that later
    if current_user.is_authenticated:

        if current_user.user_type == "Admin":
            return redirect(url_for('main.admin_home'))

        elif current_user.user_type == "Driver":
            return redirect(url_for('main.driver_home'))

        else:
            logout_user()
            flash("Unauthorized account type.")
            return redirect(url_for('auth.login'))

    form = LoginForm()

    if form.validate_on_submit():

        user = db.session.execute(
            sqla.select(User).filter_by(username=form.username.data)
        ).scalar_one_or_none()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)

        if user.user_type == "Admin":
            return redirect(url_for('main.admin_home'))

        elif user.user_type == "Driver":
            return redirect(url_for('main.driver_home'))

        else:
            logout_user()
            flash("Unauthorized account type.")
            return redirect(url_for('auth.login'))

    return render_template('login.html', title='Sign In', form=form)



@bp_auth.route('/user/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.map_page'))

@bp_auth.route('/sso/login')     
def sso_login():
    return oauth.auth0.authorize_redirect(
        redirect_uri="http://127.0.0.1:5000/callback", prompt="login"
    )

@bp_auth.route('/callback', methods=['GET', 'POST'])
def callback():

    if request.args.get('error'):
        error = request.args.get('error')
        if error == 'access_denied':
            flash('Login was cancelled.')
        else:
            flash(f'Login failed: {request.args.get("error_description", error)}')
        return redirect(url_for('auth.login'))

    token = oauth.auth0.authorize_access_token()
    user_info = token.get('userinfo')

    if not user_info:
        flash('SSO login failed.')
        return redirect(url_for('auth.login'))

    email = user_info.get('email')
    user = db.session.execute(
        sqla.select(User).filter_by(email=email)
    ).scalar_one_or_none()

    if user is None:
        session['sso_email'] = email
        session['sso_username'] = user_info.get('nickname', email)
        return redirect(url_for('auth.sso_setup'))

    login_user(user)
    return redirect(url_for('main.map_page'))

from app.auth.auth_forms import SSOSetupForm

@bp_auth.route('/sso/setup', methods=['GET', 'POST'])
def sso_setup():
    if 'sso_email' not in session:
        return redirect(url_for('auth.login'))

    form = SSOSetupForm()

    if form.validate_on_submit():
        email = session.pop('sso_email')
        username = session.pop('sso_username', email)
        user_type = form.user_type.data

        if user_type == 'Admin':
            user = Admin(
                username=form.username.data,
                email=email,
                user_type='Admin',
                location_id=int(form.location.data)
            )
        elif user_type == 'Driver':
            user = Driver(
                username=form.username.data,
                email=email,
                user_type='Driver',
            )
        else:
            user = User(
                username=form.username.data,
                email=email,
                user_type='User',
            )

        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.map_page'))

    form.username.data = form.username.data or session.get('sso_username', '')
    return render_template('sso_setup.html', form=form)
