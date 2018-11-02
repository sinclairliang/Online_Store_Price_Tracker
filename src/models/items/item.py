import requests
import bs4
import re
import uuid

from src.commom.database import Database
import src.models.items.constants as ItemConstants
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        store = Store.get_by_url(url)
        self.tag_name = store.get_tag_name()
        self.query = store.get_query_name()
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        # overriding print method
        if self.price is not None:
            return "---Item {} at the price of {} with the URL {}---".format(self.name,
                                                                             self.price,
                                                                             self.url)
        return "---Item {} with the URL {}---".format(self.name, self.url)

    def load_item_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = bs4.BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()
        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)
        self.price = match.group()
        return self.price

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        # return the json representation of this object
        return {
            "name": self.name,
            "url": self.url,
            "price": self.price,
            "_id": self._id
        }

    @classmethod
    def retrieve_item(cls, url):
        item_data = Database.find_one(ItemConstants.COLLECTION, url)
        return cls(**item_data)

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))
