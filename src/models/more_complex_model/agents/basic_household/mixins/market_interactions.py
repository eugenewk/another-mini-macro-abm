from models.more_complex_model.markets.basic_market import BasicMarket, MarketListing

class MarketMixin:
    def __init__(self):
        pass

    def create_listing(self, market: BasicMarket):
        pass

    def manage_listing(self, market: BasicMarket):
        pass