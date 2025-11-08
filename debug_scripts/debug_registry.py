"""Debug script to test and view registry output."""

from mini_macro_abm.core.registry import Registry

def debug_registry():
    """Test the registry and display loaded configuration."""
    print("=== REGISTRY DEBUG OUTPUT ===")
    
    # Create registry instance
    registry = Registry()
    print("✅ Registry created successfully")
    
    # Load configuration from simple_model folder
    try:
        registry.load_run_config_from_folder("src/models/simple_model")
        print("✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return None
    
    print("\n--- LOADED CONFIGURATION ---")
    
    # Display simulation configuration
    print("📊 SIMULATION CONFIG:")
    print(f"  sim_config: {registry.sim_config}")
    if registry.sim_config:
        for key, value in registry.sim_config.items():
            print(f"    {key}: {value}")
    
    # Display model configuration  
    print("\n🏗️  MODEL CONFIG:")
    print(f"  model_config: {registry.model_config}")
    if registry.model_config:
        for key, value in registry.model_config.items():
            print(f"    {key}: {value}")
    
    # Display specific values
    print("\n🔍 SPECIFIC VALUES:")
    print(f"  Steps: {registry.sim_config.get('steps', 'Not found')}")
    
    agents = registry.model_config.get('agents', {})
    print(f"  Agents: {agents}")
    
    if 'simple' in agents:
        simple_agent = agents['simple']
        print(f"  Simple agent config: {simple_agent}")
        print(f"  Simple agent count: {simple_agent.get('count', 'Not found')}")
    
    # Display loaded agent configurations
    print("\n🤖 LOADED AGENT CONFIGS:")
    print(f"  agent_configs: {registry.agent_configs}")
    if registry.agent_configs:
        for agent_type, agent_config in registry.agent_configs.items():
            print(f"    {agent_type}: {agent_config}")
            if 'params' in agent_config:
                print(f"      Parameters: {agent_config['params']}")
            if 'mixins' in agent_config:
                print(f"      Mixins: {agent_config['mixins']}")
    
    print("\n=== DEBUG COMPLETE ===")
    return registry

if __name__ == "__main__":
    debug_registry()
