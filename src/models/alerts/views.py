from flask import Blueprint, render_template, request, session, redirect, url_for

from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as user_decorators

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
def index():
    return "Log in to see your alerts!"


@alert_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_login
def create_alert():
    if request.method == 'POST':
        # reading data input from form submission
        name = request.form['name']
        url = request.form['url']
        price_limit = float(request.form['price_limit'])
        item = Item(name, url)
        item.save_to_mongo()
        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price()  # saved to Mongo already
    return render_template('alerts/new_alert.jinja2')


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_alert(alert_id):
    # method to modify existing alerts
    alert = Alert.find_by_id(alert_id)
    # we first find it
    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])
        alert = Alert.find_by_id(alert_id)
        alert.price_limit = price_limit
        # change the price limit
        alert.save_to_mongo()
        # then save to database

        return redirect(url_for('users.user_alerts'))
    return render_template('alerts/edit_alert.jinja2', alert=alert)



@alert_blueprint.route('/deactivate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    # we deactivate an alert by calling the method defined in Alert class
    Alert.find_by_id(alert_id).deactivate()
    return redirect(url_for('alerts.get_alert_page', alert_id=alert_id))


@alert_blueprint.route('/activate/<string:alert_id>')
@user_decorators.requires_login
def activate_alert(alert_id):
    # we activate an alert by calling the method defined in Alert class
    Alert.find_by_id(alert_id).activate()
    return redirect(url_for('alerts.get_alert_page', alert_id=alert_id))


@alert_blueprint.route('/delete/<string:alert_id>')
@user_decorators.requires_login
def delete_alert(alert_id):
    # we delete an alert by calling the method defined in Alert class
    Alert.find_by_id(alert_id).delete()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    # redirect users to the specific alert page
    alert = Alert.find_by_id(alert_id)
    return render_template('alerts/alert.jinja2', alert=alert)


@alert_blueprint.route('/check/<string:alert_id>')
def check_alert_price(alert_id):
    # run a checker on alert price
    Alert.find_by_id(alert_id).load_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))
