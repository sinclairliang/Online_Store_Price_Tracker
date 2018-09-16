import requests
import bs4
import re
import uuid

from src.commom.database import Database
import src.models.items.constants as ItemConstants
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, _id=None):
        self.name = name
        self.url = url
        store = Store.get_by_url(url)
        tag_name = store.get_tag_name()
        query = store.get_query_name()
        self.price = self.load_item_price(tag_name, query)
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        if self.price is not None:
            return "---Item {} at the price of {} with the URL {}---".format(self.name,
                                                                             self.price,
                                                                             self.url)
        return "---Item {} with the URL {}---".format(self.name, self.url)

    def load_item_price(self, tag_name, query):
        request = requests.get(self.url)
        content = request.content
        soup = bs4.BeautifulSoup(content, "html.parser")
        element = soup.find(tag_name, query)
        string_price = element.text.strip()
        pattern = re.compile("(\d+.\d+)") # 74.37
        match = pattern.search(string_price)
        return match.group()

    def save_to_mongo(self):
        Database.insert(ItemConstants.COLLECTION, self.json())

    def json(self):
        return {
            "name": self.name,
            "url": self.url,
            "price": self.price,
            "id": self._id
        }

    @classmethod
    def retrieve_item(cls, url):
        item_data = Database.find_one(ItemConstants.COLLECTION, url)
        return cls(**item_data)
