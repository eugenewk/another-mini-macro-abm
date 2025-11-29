
"""simple mixin"""

class ProductionMixin:
    def __init__(self, *args, **kwargs):
        # note: define parameters in the main agent class

        # add production
        self.daily_production = 2

        # add the desired data fields to tracking
        self.agent_data.add_data_attributes(['daily_production'])

        required_attrs = [] # use if any agent attrs are required for this mixin

        for attr in required_attrs:
            if not hasattr(self, attr):
                raise ValueError(f'{attr} not found in agent class')
            
        super().__init__(*args, **kwargs)

    def produce_goods(self):
        production_qty = self.daily_production
        self.stock_matrix.manage_inventory_item('item', production_qty) # adds chosen qty to inventory
