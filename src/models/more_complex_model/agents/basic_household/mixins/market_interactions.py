from models.more_complex_model.markets.basic_market import BasicMarket, MarketListing
import random
from typing import List

class GoodsMarketInteractions:
    def __init__(self):
        # don't define any attributes here, just interaction functions
        pass

    def buy_goods(self, good: str, market: BasicMarket):
        # main function for goods purchasing
        chosen_listing = self._pick_listing(good, market)
        

    def _pick_listing(self, good:str, market: BasicMarket):
        all_listings: List[MarketListing] = market.active_listings_for_good(good)
        
        if not all_listings:
            return None # none available
        
        chosen_listing: MarketListing = random.choice(all_listings)
        
        print(f"chose listing: {chosen_listing}, id: {chosen_listing.listing_id}")
        return chosen_listing.listing_id