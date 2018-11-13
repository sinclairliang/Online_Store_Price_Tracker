import json

from flask import Blueprint, render_template, request, redirect, url_for

from src.models.stores.store import Store

import src.models.users.decorators as user_decorators

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/store_index.jinja2', stores=stores)


@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    return render_template('stores/store.jinja2', store=Store.get_by_id(store_id))



@store_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_admin_permission
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])
        Store(name, url_prefix, tag_name, query).save_to_mongo()

        return redirect(url_for('.index'))
    return render_template('stores/new_store.jinja2')



@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@user_decorators.requires_admin_permission
def edit_store(store_id):
    store = Store.get_by_id(store_id)

    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form["query"])


        store.name = name
        store.url_prefix = url_prefix
        store.tag_name = tag_name
        store.query = query

        store.save_to_mongo()
        return redirect(url_for('.index'))
    return render_template('stores/edit_store.jinja2', store=store)



@store_blueprint.route('/delete/<string:store_id>')
@user_decorators.requires_admin_permission
def delete_store(store_id):
    Store.get_by_id(store_id).delete()
    return redirect(url_for('.index'))
