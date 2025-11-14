"""simple agent file"""
from models.simple_model.agents.simple_agent.mixins import simple_mixin
from mini_macro_abm.core.agent_factory.base_agent import BaseAgent
from mini_macro_abm.core.data_collector import AgentDataObject
from mini_macro_abm.core.agent_utils.stock_matrix import StockMatrix

class SimpleAgent:

    def __init__(self, id):
        # core setup params, requires id given by sim engine
        self.id = id
        self.agent_data = AgentDataObject(id) # creates data tracking object
        self.stock_matrix = StockMatrix() # gives stock matrix

        # define all custom agent params here
        self.agent_param = 0
        self.mixin_param = 0 # note that this is used by a mixin function
        self.test_param = 'nothing'

        # add the desired data fields to tracking
        # must include stock matrix
        self.agent_data.add_data_attributes(self.stock_matrix, ['agent_param', 'mixin_param', 'test_param'])
        
        # this will call the inits for each mixins
        # call this AFTER initializing the agent params, then the mixins can validate their required params exist
        super().__init__()

    def __repr__(self):
        return f"{self.id}"

    def increment_agent_param(self):
        self.agent_param += 2
    
    def add_cash(self, amount):
        self.stock_matrix.manage_cash(amount)

    def remove_cash(self, amount):
        self.stock_matrix.manage_cash(-amount)

    def add_item(self, item: str, amount: int):
        self.stock_matrix.manage_inventory_item(item, amount)
       


    
