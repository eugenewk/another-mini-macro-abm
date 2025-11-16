"""simple agent file"""
from mini_macro_abm.core.data_collector import AgentDataObject
from mini_macro_abm.core.agent_utils.stock_matrix import StockMatrix
from models.more_complex_model.markets.basic_market import BasicMarket

class BasicProducer:

    def __init__(self, id):
        # core setup params, requires id given by sim engine
        self.id = id
        self.stock_matrix = StockMatrix() # gives stock matrix
        self.agent_data = AgentDataObject(id, self.stock_matrix) # creates data tracking object

        # add production
        self.daily_production = 1

        # add the desired data fields to tracking
        self.agent_data.add_data_attributes(['daily_production'])
        
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
       


    
