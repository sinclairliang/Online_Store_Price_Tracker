class Item(object):
    def __init__(self, name, price, url):
        self.name = name
        self.price = price
        self.url = url

    def __repr__(self):
        if self.price is not None:
            return "---Item {} at the price of {} with the URL {}---".format(self.name,
                                                                             self.price,
                                                                             self.url)
        return "---Item {} with the URL {}---".format(self.name, self.url)
