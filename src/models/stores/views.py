from flask import Blueprint, render_template

from src.models.stores.store import Store

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/store_index.jinja2', stores=stores)


@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    return "This is the store page"


@store_blueprint.route('/new', methods=['GET', 'POST'])
def create_store():
    return "Store creation page"
