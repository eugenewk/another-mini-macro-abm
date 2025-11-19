from models.more_complex_model.markets.basic_market import BasicMarket, MarketListing
from models.more_complex_model.agents.basic_producer.producer import BasicProducer
import random
from typing import List

class GoodsMarketInteractions:
    def __init__(self):
        # don't define any attributes here, just interaction functions
        pass

    def buy_goods(self, good: str, market: BasicMarket):
        # main function for goods purchasing
        chosen_listing: MarketListing = self._choose_listing(good, market)

        if not chosen_listing: # if no listings available and none chosen
            print(f'no listings available')
            return None
        
        seller: BasicProducer = chosen_listing.seller
        chosen_qty: int = self._choose_qty(chosen_listing) # returns the desired qty from the listing, set to 1 right now
        total_price = chosen_qty * chosen_listing.price # note: add budgeting logic later in _choose_qty()
    
        # below returns a bool if successful
        purchase_successful = seller.receive_purchase_order(market, self.id, chosen_listing.good_type, chosen_qty, total_price)

        if purchase_successful:
            self.stock_matrix.manage_inventory_item(good, chosen_qty) # use stock matrix function
            self.stock_matrix.manage_cash(-total_price) # use stock matrix function
            print(f"purchase successful, bought {chosen_qty} of {good} from {seller.id} for {total_price}")
        else:
            print("failed to purchase")


        
        
    def _choose_listing(self, good:str, market: BasicMarket):
        all_listings: List[MarketListing] = market.active_listings_for_good(good)
        
        if not all_listings:
            return None # none available
        
        chosen_listing: MarketListing = random.choice(all_listings)
        
        print(f"chose listing: {chosen_listing}, id: {chosen_listing.listing_id}")
        return chosen_listing
    
    def _choose_qty(self, listing: MarketListing):
        qty_available = listing.quantity
        return 1