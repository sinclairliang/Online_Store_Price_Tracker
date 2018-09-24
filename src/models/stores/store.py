import uuid

from src.commom.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreError


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "---Store {}---".format(self.name)

    def get_tag_name(self):
        return self.tag_name

    def test(self):
        pass

    def get_query_name(self):
        return self.query

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.insert(StoreConstants.COLLECTION, {"_id": id}))

    def save_to_mongo(self):
        Database.insert(StoreConstants.COLLECTION, self.json())

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name": store_name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        """
        http://www.amazon -> http://www.amazon.com, etc.
        :param url_prefix:
        :return:
        """
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": "^{}".format(url_prefix)}}))

    @classmethod
    def get_by_url(cls, url):
        for i in range(len(url)):
            try:
                store = cls.get_by_url_prefix(url[:i])
                return store
            except:
                raise StoreError.StoreNotFoundError("We couldn't find stores by this URL...")