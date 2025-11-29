"""simple agent file"""
from mini_macro_abm.core.data_collector import AgentDataObject
from mini_macro_abm.core.agent_utils.stock_matrix import StockMatrix

class BasicHousehold:

    def __init__(self, id, *args, **kwargs):
        # core setup params, requires id given by sim engine
        self.id = id
        self.stock_matrix = StockMatrix() # gives stock matrix
        self.agent_data = AgentDataObject(id, self.stock_matrix) # creates data tracking object


        # define all custom agent params here
        self.agent_param = 0
        self.test_param = 'nothing'

        # add the desired data fields to tracking
        self.agent_data.add_data_attributes(['agent_param', 'test_param'])
        # note that you can add more attributes individually in the mixins
        
        # this will call the inits for each mixin
        super().__init__(*args, **kwargs)

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
