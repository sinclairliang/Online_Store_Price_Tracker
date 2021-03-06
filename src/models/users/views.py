from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect

import src.models.users.errors as UserErrors
from src.models.users.user import User
import src.models.users.decorators as user_decorators

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        # read the form data
        email = request.form['email']
        password = request.form.get('password')
        try:
            # then try to match with user's email and password
            if User.login_valid(email, password):
                # matching the email with the email in session
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except UserErrors.UserError as e:
            # raise an error if not matched
            return e.message
    return render_template("users/login.jinja2")  # wish to return a pop-up window


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # print(request.form)
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except UserErrors.UserError as e:
            return e.message
    return render_template("users/register.jinja2")  # wish to return a pop-up window


@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session['email'])
    alerts = user.get_alerts()
    return render_template('users/alerts.jinja2', alerts=alerts)


@user_blueprint.route('/logout')
def logout_user():
    # empty the session
    session['email'] = None
    return redirect(url_for('home'))


@user_blueprint.route('/check_alerts/string:user_id')
def check_user_alerts(user_id):
    pass
