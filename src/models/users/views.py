from flask import Blueprint

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/login')
def login_user():
    pass


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
