import uuid
import smtplib
import src.models.alerts.constants as AlertConstants
import src.models.alerts.login_info as LoginInfo
import datetime
from src.commom.database import Database
from src.models.items.item import Item
from email.mime.text import MIMEText


class Alert(object):

    # Alert object
    def __init__(self, user_email, price_limit, item_id, active=True, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.active = active
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        # overriding print method
        return "---Alert for {} on item {} with the price limit {}---".format(self.user_email,
                                                                              self.item.name,
                                                                              self.price_limit)

    def send(self):
        # sending emails to users by using Mailgun API
        msg = MIMEText(
            "We found you a deal for you. Click on link: {}".format(self.item.url))
        msg['Subject'] = 'Price Reached for item {}!'.format(self.item.name)
        msg['From'] = LoginInfo.LOGIN
        msg['To'] = self.user_email
        s = smtplib.SMTP('smtp.mailgun.org', 587)
        s.login(LoginInfo.LOGIN, LoginInfo.PASSWORD)
        if len(s.sendmail(msg['From'], msg['To'], msg.as_string())) == 0:
            return True
        else:
            return False

    @classmethod
    def find_update(cls, time_since_update=AlertConstants.ALERT_TIMEOUT):
        # update alerts status if last update was more than ALERT_TIMEOUT minutes ago,
        # default 10 minutes
        last_updated_limit = datetime.datetime.utcnow(
        ) - datetime.timedelta(minutes=time_since_update)
        return [cls(**element) for element in Database.find(AlertConstants.COLLECTION,
                                                            {"last_checked":
                                                                 {"$lte": last_updated_limit}, "active": True})]

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {
            "_id": self._id}, self.json())

    def json(self):
        # returns a JSON object to represent alerts
        return {
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "_id": self._id,
            "user_email": self.user_email,
            "item_id": self.item._id,
            "active": self.active
        }

    def load_item_price(self):
        # calling methods in item class to update price
        self.item.load_item_price()
        # update last checked time
        self.last_checked = datetime.datetime.utcnow()
        # save to data base
        self.item.save_to_mongo()
        self.save_to_mongo()
        return self.item.price

    def send_email_if_price_reached(self):
        if float(self.item.price) <= float(self.price_limit):
            self.send()

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {'user_email': user_email})]

    @classmethod
    def find_by_id(cls, alert_id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {'_id': alert_id}))

    def deactivate(self):
        self.active = False
        self.save_to_mongo()

    def activate(self):
        self.active = True
        self.save_to_mongo()

    def delete(self):
        Database.remove(AlertConstants.COLLECTION, {'_id': self._id})
