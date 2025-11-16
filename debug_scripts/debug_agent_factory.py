"""Debug script to test and view agent factory output."""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.mini_macro_abm.core.registry import Registry
from mini_macro_abm.core.factory.component_factory import AgentFactory

def debug_agent_factory():
    """Test the agent factory and display composed agent classes."""
    print("=== AGENT FACTORY DEBUG OUTPUT ===")
    
    # Create registry instance
    registry = Registry()
    print("✅ Registry created successfully")
    
    # Load configuration from simple_model folder
    try:
        registry.load_run_config_from_folder("../src/models/simple_model")
        print("✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return None
    
    # Create agent factory
    try:
        factory = AgentFactory(registry)
        print("✅ Agent factory initialized successfully")
    except Exception as e:
        print(f"❌ Error creating agent factory: {e}")
        return None
    
    # Compose all agents
    print("\n🤖 COMPOSING AGENT CLASSES...")
    try:
        composed_agents = factory.compose_all_agent_classes()
        print(f"✅ Successfully composed {len(composed_agents)} agent classes")
    except Exception as e:
        print(f"❌ Error composing agents: {e}")
        return None
    
    # Display composed agent classes
    print("\n--- COMPOSED AGENT CLASSES ---")
    for agent_name, agent_class in composed_agents.items():
        print(f"\n🔧 {agent_name}:")
        print(f"   Class: {agent_class}")
        print(f"   Class Name: {agent_class.__name__}")
        
        # Show inheritance chain
        print(f"   Inheritance (MRO):")
        for i, base_class in enumerate(agent_class.__mro__):
            print(f"     {i}. {base_class.__name__}")
        
        # Show available methods (excluding dunder methods)
        methods = [method for method in dir(agent_class) 
                  if not method.startswith('_') and callable(getattr(agent_class, method))]
        print(f"   Available Methods: {methods}")
        
        # Show parameters from config (for reference only)
        agent_config = registry.agent_configs.get(agent_name, {})
        params = agent_config.get('params', {})
        print(f"   Config Parameters: {params} (for reference)")
        
        # Test creating an instance without parameters
        try:
            agent_instance = agent_class()
            print(f"   ✅ Instance created successfully")
            
            # Test calling methods if they exist
            if hasattr(agent_instance, 'increment_agent_param'):
                agent_instance.increment_agent_param()
                print(f"   ✅ increment_agent_param() called successfully")
            
            if hasattr(agent_instance, 'increment_attribute'):
                agent_instance.increment_attribute()
                print(f"   ✅ increment_attribute() called successfully")
                
            if hasattr(agent_instance, 'provide_data'):
                data = agent_instance.provide_data()
                print(f"   ✅ provide_data() returned: {data}")
                
        except Exception as e:
            print(f"   ❌ Error creating instance: {e}")
    
    print("\n=== DEBUG COMPLETE ===")
    return composed_agents

if __name__ == "__main__":
    debug_agent_factory()
