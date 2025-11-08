import logging
import importlib
from typing import Dict, Any, List, Type

from mini_macro_abm.core.agent_factory.base_agent import BaseAgent
from mini_macro_abm.core.registry import Registry

logger = logging.getLogger(__name__)

class AgentFactory:
    
    def __init__(self, registry: Registry):
        """
        Initializes the agent factory with a pre-loaded registry.
        """
        self.registry = registry

    def _import_class_from_path(self, class_path: str) -> Type:
        """
        Imports classes from a path. Used to compose agents from mixins.
        Gets the import path from the config file, splits in and imports.
        """

        try:
            module_name, class_name = class_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            return cls
        except (ImportError, AttributeError, ValueError) as e:
            logger.error(f"could not import class '{class_path}'")
            raise

    def _compose_agent_class(self, agent_name: str, agent_config_data: Dict[str, Any]) -> Type:
        mixin_paths = agent_config_data.get('mixins', [])

        try:
            agent_class_path = agent_config_data.get('agent_class_path')
            AgentClass = self._import_class_from_path(agent_class_path)
        except ValueError as e:
            logger.warning(f"could not load from {agent_class_path}")
            raise

        base_classes = [BaseAgent, AgentClass]
        agent_mixins = []

        for mixin_path in mixin_paths:
            try:
                MixinClass = self._import_class_from_path(mixin_path)
                agent_mixins.append(MixinClass)
                logger.debug(f"added mixin class '{MixinClass.__name__} from '{agent_class_path}")
            except ValueError as e:
                logger.warning(f"could not load mixin '{mixin_path}' for '{agent_name}: {e}")
                raise

        
        composed_class = type(
            f"{agent_name}_sim",
            tuple(base_classes + agent_mixins),
            {}
        )

        return composed_class
    
    def compose_all_agent_classes(self) -> Dict[str, Type]:
        """
        Composes all agent classes from the registry and returns a dictionary
        mapping agent names to their composed classes.
        """
        composed_agent_classes = {}
        
        # Use the actual agent_configs from registry
        for agent_name, agent_config in self.registry.agent_configs.items():
            try:
                composed_class = self._compose_agent_class(agent_name, agent_config)
                composed_agent_classes[agent_name] = composed_class
                logger.info(f"Composed agent class for '{agent_name}'")
            except Exception as e:
                logger.error(f"Failed to compose agent '{agent_name}': {e}")
                continue
        
        return composed_agent_classes
    
    def instantiate_agents(self, agent_classes: Dict[str, Type]) -> Dict[str, List[object]]:
        # for each agent class, look at the registry and create the appropriate number of agents
        agent_roster = {}

        # go through each agent class in the list, get the count from the registry
        for agent_name, agent_class in agent_classes.items():
            agent_count = self.registry.model_config['agents'][agent_name]['count']

            # instantiate individual agent objects
            agents = []
            for i in range(agent_count):
                agent = agent_class()
                agents.append(agent)

            agent_roster[agent_name] = agents

        return agent_roster
    


