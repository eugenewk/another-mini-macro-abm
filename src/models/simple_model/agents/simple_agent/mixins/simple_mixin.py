
"""simple mixin"""

class SimpleMixin:
    def __init__(self):
        super().__init__()
        # note: define parameters in the main agent class
    
    def increment_mixin_attribute(self):
        self.mixin_param += 1
