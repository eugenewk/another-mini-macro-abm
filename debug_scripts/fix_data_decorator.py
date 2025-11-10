#!/usr/bin/env python3
"""
Fix for @data decorator and property setters
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def data(func):
    """Fixed @data decorator that properly marks properties and adds setters"""
    print(f"DEBUG: Applying @data to {func.__name__}")
    
    # Store the original function name for the setter
    private_name = f"_{func.__name__}"
    
    def getter(self):
        return getattr(self, private_name, 0)
    
    def setter(self, value):
        setattr(self, private_name, value)
    
    # Mark the property
    prop = property(getter, setter)
    prop._is_data_attribute = True
    
    print(f"DEBUG: Created property with _is_data_attribute: {hasattr(prop, '_is_data_attribute')}")
    return prop

def test_fixed_decorator():
    """Test the fixed @data decorator"""
    print("=== Testing Fixed @data Decorator ===")
    
    class TestClass:
        def __init__(self):
            self._test_value = 42
        
        @data
        def test_property(self):
            return self._test_value
    
    # Test the fixed decorator
    obj = TestClass()
    print(f"Test property value: {obj.test_property}")
    print(f"Test property type: {type(TestClass.test_property)}")
    print(f"Has _is_data_attribute: {hasattr(TestClass.test_property, '_is_data_attribute')}")
    
    # Test setter
    obj.test_property = 100
    print(f"After setting: {obj.test_property}")
    print()

def create_fixed_agent_and_mixin():
    """Create fixed versions of agent and mixin with working @data properties"""
    print("=== Creating Fixed Agent and Mixin ===")
    
    class FixedSimpleAgent:
        def __init__(self):
            self._agent_param = 0

        def __repr__(self):
            return f"fixed simple agent, param: {self._agent_param}"

        def increment_agent_param(self):
            self.agent_param += 1

        @data
        def agent_param(self):
            return self._agent_param

    class FixedSimpleMixin:
        def __init__(self):
            self._mixin_attribute = 0
        
        def increment_mixin_attribute(self):
            self.mixin_attribute += 1

        @data
        def mixin_attribute(self):
            return self._mixin_attribute

    # Test the fixed classes
    agent = FixedSimpleAgent()
    print(f"Agent agent_param: {agent.agent_param}")
    print(f"Has setter: {FixedSimpleAgent.agent_param.fset is not None}")
    
    # Test setter
    agent.agent_param = 10
    print(f"After setting: {agent.agent_param}")
    
    mixin = FixedSimpleMixin()
    print(f"Mixin mixin_attribute: {mixin.mixin_attribute}")
    print(f"Has setter: {FixedSimpleMixin.mixin_attribute.fset is not None}")
    
    # Test setter
    mixin.mixin_attribute = 5
