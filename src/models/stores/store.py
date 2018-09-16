class Store(object):
    def __init__(self, name, url_prefix, tag_name, query):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query

    def __repr__(self):
        return "---Store {}---".format(self.name)

    def get_tag_name(self):
        return self.tag_name

    def get_query_name(self):
        return self.query
