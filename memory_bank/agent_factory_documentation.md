# Agent Factory Module Documentation

## Introduction

The agent factory module is designed to dynamically create and compose agent classes based on configuration. This approach provides flexibility, modularity, and extensibility in defining agent behaviors within the simulation.

## Core Components

### `AgentFactory` Class

The `AgentFactory` class is responsible for orchestrating the creation of agent classes.

#### `__init__(self, registry: Registry)`

*   **Description**: Initializes the `AgentFactory` with a pre-loaded `Registry` object.
*   **Parameters**:
    *   `registry` (`Registry`): An instance of the `Registry` class containing agent configurations.

#### `_import_class_from_path(self, class_path: str) -> Type`

*   **Description**: A private helper method to dynamically import Python classes from a given string path. This is crucial for composing agents from mixins and specifying the base agent class.
*   **Parameters**:
    *   `class_path` (`str`): The fully qualified path to the class (e.g., 'module.submodule.ClassName').
*   **Returns**: The imported class object (`Type`).
*   **Raises**:
    *   `ImportError`: If the module cannot be found.
    *   `AttributeError`: If the class cannot be found within the module.
    *   `ValueError`: If the `class_path` is not in the expected format.

#### `_compose_agent_class(self, agent_name: str, agent_config_data: Dict[str, Any]) -> Type`

*   **Description**: The core method for creating a new agent class. It combines a specified base agent class with a list of mixin classes, all defined in the agent's configuration.
*   **Parameters**:
    *   `agent_name` (`str`): The name of the agent being composed.
    *   `agent_config_data` (`Dict[str, Any]`): A dictionary containing the configuration for the agent. Expected keys include:
        *   `agent_class_path` (`str`): The path to the primary agent class.
        *   `mixins` (`List[str]`, optional): A list of paths to mixin classes to be applied.
*   **Process**:
    1.  Imports the base agent class specified by `agent_class_path`.
    2.  Iterates through the `mixins` list, importing each mixin class.
    3.  Uses Python's `type()` function to dynamically create a new class that inherits from `BaseAgent`, the imported base agent class, and all imported mixin classes. The new class is named using the `agent_name` (e.g., `f"{agent_name}_sim"`).
*   **Returns**: The dynamically composed agent class (`Type`).
*   **Raises**:
    *   `ValueError`: If `agent_class_path` or any mixin path cannot be loaded.

#### `compose_all_agents(self) -> Dict[str, Type]`

*   **Description**: Iterates through all agent configurations stored in the `Registry` and composes the corresponding agent classes using `_compose_agent_class`.
*   **Returns**: A dictionary mapping agent names (`str`) to their newly composed class types (`Type`).

### `BaseAgent` Class

*   **Description**: This class serves as the foundational building block for all agents within the simulation. It is intended to contain common attributes and methods shared across all agents.
*   **Attributes**:
    *   `super().__init__()`: Calls the parent constructor.
    *   `# will add stock matrix here`: A comment indicating a future implementation detail where a `StockMatrix` will be added.

## Configuration

Agent configurations are expected to be stored within the `Registry` object. Each agent's configuration should be a dictionary with the following structure:

*   `agent_class_path` (`str`): The fully qualified Python path to the primary class that defines the agent's core behavior.
*   `mixins` (`List[str]`, optional): A list of fully qualified Python paths to mixin classes. These classes will be inherited by the composed agent, adding their functionality.

## Usage Example

```python
from src.mini_macro_abm.core.registry import Registry
from src.mini_macro_abm.core.agent_factory.agent_factory import AgentFactory

# Assume registry is already populated with agent configurations
# registry = Registry(...) 

# Example: Manually creating a registry for demonstration
class MockRegistry:
    def __init__(self):
        self.agent_configs = {
            "trader": {
                "agent_class_path": "src.models.simple_model.agents.simple_agent.simple_agent.SimpleAgent",
                "mixins": [
                    "src.models.simple_model.agents.simple_agent.mixins.simple_mixin.SimpleMixin"
                ]
            }
        }

registry = MockRegistry()

# Initialize the agent factory
factory = AgentFactory(registry)

# Compose all agent classes
composed_agents = factory.compose_all_agents()

# Now you can instantiate agents from the composed classes
# For example:
# trader_class = composed_agents.get("trader")
# if trader_class:
#     trader_instance = trader_class() 
#     print(f"Successfully composed and instantiated: {trader_instance}")

print(f"Composed agents: {composed_agents}")
