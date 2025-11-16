
"""simple mixin"""

class ProductionMixin:
    def __init__(self):
        # note: define parameters in the main agent class

        required_attrs = ['daily_production']

        for attr in required_attrs:
            if not hasattr(self, attr):
                raise ValueError(f'{attr} not found in agent class')

    def produce_goods(self):
        production_qty = self.daily_production
        self.stock_matrix.manage_inventory_item('item', production_qty) # adds chosen qty to inventory 
