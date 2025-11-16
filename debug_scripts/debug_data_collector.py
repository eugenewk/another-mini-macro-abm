#!/usr/bin/env python3
"""
Debug script for @data decorator and DataCollector functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.mini_macro_abm.core.data_collector import data, DataCollector
from src.mini_macro_abm.core.registry import Registry
from mini_macro_abm.core.factory.component_factory import AgentFactory

def debug_data_decorator():
    """Test the @data decorator directly"""
    print("=== DEBUG: Testing @data decorator ===")
    
    # Test the decorator on a simple class
    class TestClass:
        def __init__(self):
            self._test_value = 42
        
        @data
        def test_property(self):
            return self._test_value
    
    # Create instance and test
    obj = TestClass()
    print(f"Test property value: {obj.test_property}")
    print(f"Test property type: {type(TestClass.test_property)}")
    print(f"Has _is_data_attribute: {hasattr(TestClass.test_property, '_is_data_attribute')}")
    print()

def debug_agent_composition():
    """Test if agents are being composed correctly with @data properties"""
    print("=== DEBUG: Testing agent composition ===")
    
    try:
        # Load a simple model
        registry = Registry()
        registry.load_run_config_from_folder('src/models/simple_model')
        
        # Create agent factory and compose classes
        factory = AgentFactory(registry)
        agent_classes = factory.compose_all_agent_classes()
        
        print(f"Composed agent classes: {list(agent_classes.keys())}")
        
        for agent_name, agent_class in agent_classes.items():
            print(f"\n--- Agent Class: {agent_name} ---")
            print(f"Class: {agent_class}")
            print(f"MRO: {agent_class.__mro__}")
            
            # Check class attributes
            print("Class attributes:")
            for attr_name, attr_obj in agent_class.__dict__.items():
                if not attr_name.startswith('_'):
                    print(f"  {attr_name}: {type(attr_obj)}")
                    if hasattr(attr_obj, '_is_data_attribute'):
                        print(f"    -> HAS @data marker!")
            
            # Create an instance and test
            agent_instance = agent_class()
            print(f"Instance attributes (non-private): {[x for x in dir(agent_instance) if not x.startswith('_')]}")
            
            # Test if properties work
            if hasattr(agent_instance, 'agent_param'):
                print(f"agent_param value: {agent_instance.agent_param}")
            if hasattr(agent_instance, 'mixin_attribute'):
                print(f"mixin_attribute value: {agent_instance.mixin_attribute}")
        
    except Exception as e:
        print(f"Error during agent composition: {e}")
        import traceback
        traceback.print_exc()
    print()

def debug_data_collector_detection():
    """Test DataCollector's ability to detect @data properties"""
    print("=== DEBUG: Testing DataCollector detection ===")
    
    try:
        # Load model and create agents
        registry = Registry()
        registry.load_run_config_from_folder('src/models/simple_model')
        
        factory = AgentFactory(registry)
        agent_classes = factory.compose_all_agent_classes()
        agent_roster = factory.instantiate_agents(agent_classes)
        
        print(f"Agent roster: {list(agent_roster.keys())}")
        
        # Test DataCollector
        collector = DataCollector(agent_roster)
        
        # Manually test the detection logic
        for agent_type, agents in agent_roster.items():
            print(f"\n--- Testing agents of type: {agent_type} ---")
            
            for i, agent in enumerate(agents[:1]):  # Just test first agent
                print(f"Agent {i}:")
                print(f"  Class: {agent.__class__}")
                print(f"  MRO: {agent.__class__.__mro__}")
                
                # Test the detection logic manually
                data_dict = {}
                for cls in agent.__class__.__mro__:
                    print(f"  Checking class: {cls.__name__}")
                    for attr_name, attr_obj in cls.__dict__.items():
                        if not attr_name.startswith('_'):
                            print(f"    Attribute: {attr_name} -> {type(attr_obj)}")
                            if isinstance(attr_obj, property):
                                print(f"      Is property: True")
                                print(f"      Has _is_data_attribute: {hasattr(attr_obj, '_is_data_attribute')}")
                                if hasattr(attr_obj, '_is_data_attribute'):
                                    try:
                                        value = getattr(agent, attr_name)
                                        data_dict[attr_name] = value
                                        print(f"      -> COLLECTED: {attr_name} = {value}")
                                    except Exception as e:
                                        print(f"      -> ERROR: {e}")
                
                print(f"  Collected data: {data_dict}")
        
    except Exception as e:
        print(f"Error during DataCollector test: {e}")
        import traceback
        traceback.print_exc()
    print()

def debug_property_setters():
    """Test if properties have setters (related to the earlier error)"""
    print("=== DEBUG: Testing property setters ===")
    
    try:
        # Load model and create agents
        registry = Registry()
        registry.load_run_config_from_folder('src/models/simple_model')
        
        factory = AgentFactory(registry)
        agent_classes = factory.compose_all_agent_classes()
        agent_roster = factory.instantiate_agents(agent_classes)
        
        for agent_type, agents in agent_roster.items():
            print(f"\n--- Agent type: {agent_type} ---")
            agent = agents[0]  # Test first agent
            
            # Check if properties have setters
            for attr_name in ['agent_param', 'mixin_attribute']:
                if hasattr(agent.__class__, attr_name):
                    prop = getattr(agent.__class__, attr_name)
                    print(f"{attr_name}:")
                    print(f"  Has getter: {prop.fget is not None}")
                    print(f"  Has setter: {prop.fset is not None}")
                    print(f"  Has deleter: {prop.fdel is not None}")
                    
                    # Try to get the value
                    try:
                        value = getattr(agent, attr_name)
                        print(f"  Current value: {value}")
                    except Exception as e:
                        print(f"  Error getting value: {e}")
        
    except Exception as e:
        print(f"Error during setter test: {e}")
        import traceback
        traceback.print_exc()
    print()

if __name__ == "__main__":
    print("Data Collector Debug Script")
    print("=" * 50)
    
    debug_data_decorator()
    debug_agent_composition()
    debug_data_collector_detection()
    debug_property_setters()
    
    print("Debug script completed.")
