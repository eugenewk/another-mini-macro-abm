
"""simple mixin"""

class BudgetMixin:
    def __init__(self, *args, **kwargs):
        # define mixin-specific parameters here
        self.budget_param = 0
        # add those params to data tracking
        self.agent_data.add_data_attributes(['budget_param'])
        super().__init__(*args, **kwargs)
    
    def increment_mixin_attribute(self):
        self.budget_param += 1
