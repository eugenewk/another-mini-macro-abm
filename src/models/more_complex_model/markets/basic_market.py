from typing import Dict
import uuid

class MarketListing:
    def __init__(self, seller_id: str, good_type: str, quantity: int, price: int):
        self.listing_id = str(uuid.uuid4())
        self.seller_id = seller_id
        self.good_type = good_type
        self.quantity = quantity
        self.price = price

class BasicMarket:
    def __init__(self):
        # structure: {good_type: {listing_id: MarketListing}}
        self.listings: Dict[str, Dict[str, MarketListing]] = {}

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