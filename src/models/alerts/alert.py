import uuid
import smtplib
from email.mime.text import MIMEText
import src.models.alerts.constants as AlertConstants
import src.models.alerts.login as LoginInfo

import datetime
from src.commom.database import Database
from src.models.items.item import Item


class Alert(object):
    def __init__(self, user_email, price_limit, item_id, last_check=None, _id=None):
        self.user_email = user_email.email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.last_check = datetime.datetime.utcnow() if last_check is None else last_check
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "---Alert for {} on item {} with the price limit {}---".format(self.user_email,
                                                                              self.item.name,
                                                                              self.item.price_limit)

    def send(self):
        msg = MIMEText("We found you a deal for you. Click on link: {}".format(self.item.url))
        msg['Subject'] = 'Price Reached for item{}!'.format(self.item.name)
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
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=time_since_update)
        return [cls(**element) for element in Database.find(AlertConstants.COLLECTION,
                                                            {"last_checked":
                                                            {"$gte": last_updated_limit}})]

    def save_to_mongo(self):
        Database.insert(AlertConstants.COLLECTION, self.json())

    def json(self):
        return{
            "price_limit": self.price_limit,
            "last_check": self.last_check,
            "_id": self._id,
            "user_email": self.user_email,
            "item_id": self.item._id
        }

    def load_item_price(self):
        self.item.load_item_price()
        self.last_check = datetime.datetime.utcnow()
        self.save_to_mongo()
        return self.item.price

    def send_email_if_price_reached(self):
        if float(self.item.price) <= float(self.price_limit):
            self.send()
