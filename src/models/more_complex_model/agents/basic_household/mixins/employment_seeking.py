from models.more_complex_model.markets.labor_market import EmploymentContract, LaborMarket, LaborMarketListing
from typing import List

class LaborMarketInteractions:
    # helper functions for interacting with the labor market
    def __init__(self):
        super().__init__() # required to continue agent composition

    def apply_to_jobs(self, labor_market: LaborMarket):
        if not self.is_employed:
            listings = labor_market.active_job_listings()
            if listings:
                self._apply_until_employed(listings)

    def _apply_until_employed(self, listings: List[LaborMarketListing]):
        # sort listings by wage offer later, for now just iterate through

        for listing in listings:
            potential_employer = listing.hiring_firm

            # defined in basic_producer/mixins/manage_workforce.py
            # returns a contract if successful
            employment_contract = potential_employer.receive_application(self)
            if employment_contract: 
                # if a contract was received back, the application was successful
                self.employment_contract = employment_contract # self.employment contract defined below in the EmploymentMixin


class EmploymentMixin:
    def __init__(self):
        self.employment_contract: EmploymentContract = None
        self.agent_data.add_data_attributes(['is_employed'])
        super().__init__(*args, **kwargs)

    @property
    def is_employed(self) -> bool:
        return self.employment_contract is not None