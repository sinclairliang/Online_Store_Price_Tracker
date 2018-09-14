from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect

from src.models.users.user import User

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/login', method=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['hashed']

        if User.login_valid(email, password):
            session['email'] = email
            return redirect(url_for(".user_alerts"))
        else:
            return "Login invalid"

    return render_template("users/login.html")


@user_blueprint.route('/register')
def register_user():
    pass


@user_blueprint.route('/alerts')
def user_alerts():
    pass


@user_blueprint.route('/logout')
def logout_user():
    pass


@user_blueprint.route('/check_alerts/string:user_id')
def check_user_alerts(user_id):
    pass
