
"""simple mixin"""

class ProductionMixin:
    def __init__(self):
        # note: define parameters in the main agent class

        required_attrs = ['mixin_param']

        for attr in required_attrs:
            if not hasattr(self, attr):
                raise ValueError(f'{attr} not found in agent class')
    
    def increment_mixin_attribute(self):
        self.mixin_param += 1
