import logging
from typing import List, Dict
from mini_macro_abm.core.registry import Registry
from mini_macro_abm.core.data_collector import DataCollector

logger = logging.getLogger(__name__)

class SimEngine:
    def __init__(self, registry: Registry, agents: Dict[str, List[object]], markets: Dict[str, object]):
        self.registry = registry
        self.agents = agents
        self.markets = markets
        self.schedule: object # to be implemented
        self.totalSimSteps: int # total steps for the simulation
    
    def set_simulation_params(self):
        self.totalSimSteps = self.registry.sim_config['steps']
                    
    def run_simulation(self, output_data: bool):

        data = DataCollector(self.agents, self.markets)

        # initialize run
        self._initialize_run()

        # run each step
        for step in range(self.totalSimSteps):
            self._step(step)
            data.collect_data(step)

        data.display_data()
        if output_data:
            data.write_data(self.registry.output_dir)

    def _initialize_run(self):

        # initial setup steps here

        goods_market = self.markets['goods_market']

        # create initial goods listing
        for firm in self.agents['firm']:
            firm.create_goods_listing(goods_market) # note: need to add markets in here as well

    def _step(self, step: int):  
        goods_market = self.markets['goods_market']
        labor_market = self.markets['labor_market']

        for household in self.agents['household']:
            household.increment_agent_param()
            household.increment_mixin_attribute()
            household.add_cash(10)
            household.buy_goods('item', goods_market)
        
        for firm in self.agents['firm']:
            firm.produce_goods()
            firm.update_listing_qty(goods_market)
            firm.post_jobs(labor_market)
