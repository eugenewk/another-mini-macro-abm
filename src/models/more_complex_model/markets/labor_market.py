from typing import Dict, List
import uuid
from mini_macro_abm.core.data_collector import MarketDataObject
from dataclasses import dataclass, field

@dataclass
class EmploymentContract:
    employer: object
    employee: object
    wage: int

    def __repr__(self):
        return f"Employer: {self.employer.id} | Employee: {self.employee.id} | Wage: {self.wage}"

@dataclass
class LaborMarketListing:
    hiring_firm: object
    roles_open: int
    wage: int
    listing_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __repr__(self):
        return f"{self.hiring_firm.id} hiring at wage: {self.wage}"

class LaborMarket:
    def __init__(self):
        # structure: {listing_id: LaborMarketListing}
        self.listings: Dict[str, LaborMarketListing] = {}
        self.market_data = MarketDataObject('labor_market')

        self.market_data.add_data_attributes(['total_openings', 'listings'])

    # define custom data classes like this
    @property
    def total_openings(self) -> Dict[str, int]:
        total_openings = 0
        for listing in self.listings.values():
            total_openings += listing.roles_open
        return total_openings

    def add_job_listing(self, hiring_firm: object, roles_open: int, wage: int) -> str:
        listing = LaborMarketListing(hiring_firm, roles_open, wage)
        self.listings[listing.listing_id] = listing
        return listing.listing_id
    
    def remove_listing(self, listing_id: str) -> bool:
        if listing_id in self.listings.items():
            self.listings.pop(listing_id)
            return True # if successful
        return False # if listing ID not found
    
    def update_listing_wage(self, listing_id: str, new_wage: int) -> bool:
        # update price of listing in self.listings where ID matches
        if listing_id in self.listings.items():
            self.listings[listing_id].wage = new_wage
            return True
        else:
            return False # listing not found

    def active_job_listings(self) -> List[LaborMarketListing]:
        all_job_listings = self.listings

        # filters only listings with active quantities
        active_listings = [
            listing for listing in all_job_listings.values() 
            if listing.quantity > 0
        ]
        return active_listings

    