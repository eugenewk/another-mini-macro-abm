from typing import Dict, List
import uuid
from mini_macro_abm.core.data_collector import MarketDataObject

class MarketListing:
    def __init__(self, seller_id: str, good_type: str, quantity: int, price: int):
        self.listing_id = str(uuid.uuid4())
        self.seller_id = seller_id
        self.good_type = good_type
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"{self.seller_id}: {self.good_type} | {self.quantity}"

class BasicMarket:
    def __init__(self):
        # structure: {good_type: {listing_id: MarketListing}}
        self.listings: Dict[str, Dict[str, MarketListing]] = {}
        self.market_data = MarketDataObject('basic_market')

        self.market_data.add_data_attributes(['total_goods_listed', 'listings'])

    # define custom data classes like this
    @property
    def total_goods_listed(self) -> Dict[str, int]:
        goods_totals = {}
        for good_type, listings in self.listings.items():
            total_qty = 0
            for listing in listings.values():
                total_qty += listing.quantity
            goods_totals[good_type] = total_qty
        return goods_totals

    def add_listing(self, seller: str, good: str, qty: int, price: int) -> str:
        listing = MarketListing(seller, good, qty, price)

        # create new dict of good listings if not exists
        if good not in self.listings:
            self.listings[good] = {}

        self.listings[good][listing.listing_id] = listing

        return listing.listing_id
    
    def remove_listing(self, listing_id: str) -> bool:
        for good_type, listings in self.listings.items():
            if listing_id in listings:
                listings.pop(listing_id)
                return True # if successful
            
        return False # if listing ID not found
    
    def update_listing_price(self, listing_id: str, new_price: int) -> bool:
        # update price of listing in self.listings where ID matches
        for good_type, listings in self.listings.items():
            if listing_id in listings:
                listing = listings[listing_id]
                listing.price = new_price
                return True
            
        return False # listing not found

    def update_listing_qty(self, listing_id: str, new_qty: int) -> bool:
        # update qty listed
        for good_type, listings in self.listings.items():
            if listing_id in listings:
                listing = listings[listing_id]
                listing.quantity = new_qty

    def active_listings_for_good(self, good:str) -> List[MarketListing]:
        all_good_listings = self.listings[good]

        # filters only listings with active quantities
        active_listings = [
            listing for listing in all_good_listings.values() 
            if listing.quantity > 0
        ]
        return active_listings

    