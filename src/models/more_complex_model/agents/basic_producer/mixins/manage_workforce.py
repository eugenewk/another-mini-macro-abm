from models.more_complex_model.markets.labor_market import LaborMarket, LaborMarketListing

class HiringMixin:
    def __init__(self):
        self.positions_to_hire = 1
        self.wage_offer = 10
        self.labor_market_listing_id = None

        super().__init__()

    def post_jobs(self, labor_market: LaborMarket):
        # very simple logic for now, should just keep the posting open. 
        if self.labor_market_listing_id is None:
            self.labor_market_listing_id = labor_market.add_job_listing(self, self.positions_to_hire, self.wage_offer)
        else: 
            labor_market.update_listing_wage(self.labor_market_listing_id, self.wage_offer)

    