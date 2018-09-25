from flask import Blueprint

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
def index():
    return "This is the stores index page"


@store_blueprint.route('/store/<string:name>')
def store_page():
    pass

