import uuid
import smtplib
from email.mime.text import MIMEText
import src.models.alerts.constants as AlertConstants

import datetime

from src.commom.database import Database


class Alert(object):
    def __init__(self, user, price_limit, item, last_check=None, _id=None):
        self.user = user
        self.price_limit = price_limit
        self.item = item
        self.last_check = datetime.datetime.utcnow() if last_check is None else last_check
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "---Alert for {} on item {} with the price limit {}---".format(self.user.email,
                                                                              self.item.name,
                                                                              self.item.price_limit)

    def send(self):
        msg = MIMEText("We found you a deal for you. Click on link: {}".format(self.item.url))
        msg['Subject'] = 'Price Reached for item{}!'.format(self.item.name)
        msg['From'] = AlertConstants.LOGIN
        msg['To'] = self.user.email

        s = smtplib.SMTP('smtp.mailgun.org', 587)

        s.login(AlertConstants.LOGIN, AlertConstants.PASSWORD)
        if len(s.sendmail(msg['From'], msg['To'], msg.as_string())) == 0:
            return True
        else:
            return False

    @classmethod
    def update(cls, time_since_update=10):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=time_since_update)
        return [cls(**element) for element in Database.find(AlertConstants.COLLECTION,
                                                            {"last_checked": {"$gte": last_updated_limit}})]
