"""simple mixin"""

class SimpleMixin:
    def __init__(self):
        super().__init__()
        self.mixin_attribute = 0
    
    def increment_attribute(self):
        self.mixin_attribute += 1