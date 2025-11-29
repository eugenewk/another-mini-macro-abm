from models.more_complex_model.markets.labor_market import LaborMarket, EmploymentContract
from typing import Dict

class HiringMixin:
    def __init__(self, *args, **kwargs):
        self.desired_workforce = 1
        self.wage_offer = 10
        self.labor_market_listing_id = None
        self.employment_contracts: Dict[str, EmploymentContract] = {}  # usage: {employee.id: ContractObject}
        self.is_hiring: bool = False

        self.agent_data.add_data_attributes(['workforce_count'])

        super().__init__(*args, **kwargs)

    @property
    def workforce_count(self):
        return len(self.employment_contracts)

    def manage_workforce(self, labor_market: LaborMarket):
        # check gap to target workforce
        current_workforce = len(self.employment_contracts)
        if current_workforce < self.desired_workforce: # hiring
            self.is_hiring = True
            gap_to_target = self.desired_workforce - current_workforce
            # make job posting if none exists
            if self.labor_market_listing_id is None:
                self.labor_market_listing_id = labor_market.add_job_listing(self, gap_to_target, self.wage_offer)
            else: # listing already exists, update with roles open
                labor_market.update_listing_role_qty(self.labor_market_listing_id, gap_to_target)
        else: # no gap to target, stop hiring
            self.is_hiring = False
            # remove listing if exists
            if self.labor_market_listing_id is not None:
                labor_market.remove_listing(self.labor_market_listing_id)

    def receive_application(self, applicant: object) -> EmploymentContract:
        if self.is_hiring:
            contract = EmploymentContract(self, applicant, self.wage_offer)
            self.employment_contracts[applicant.id] = contract
            # check if needs have been met, if so set is_hiring to False to reject future applications
            if len(self.employment_contracts) >= self.desired_workforce:
                self.is_hiring = False
            return contract
        else:
            return None
