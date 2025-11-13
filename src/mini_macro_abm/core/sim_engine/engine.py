import logging
from typing import List, Dict
from mini_macro_abm.core.registry import Registry
from mini_macro_abm.core.data_collector import DataCollector

logger = logging.getLogger(__name__)

class SimEngine:
    def __init__(self, registry: Registry, agents: Dict[str, List[object]]):
        self.registry: Registry = registry
        self.agents: Dict[str, List[object]] = agents
        self.schedule: object # to be implemented
        self.totalSimSteps: int # total steps for the simulation
    
    def set_simulation_params(self):
        self.totalSimSteps = self.registry.sim_config['steps']

    def set_initial_agent_values(self):
        # iterate through agent configs and set the appropriate starting values in each agent object
        for agent_type, agent_list in self.agents.items():
            agent_config = self.registry.agent_configs.get(agent_type)
            params = agent_config.get('params')

            for agent in agent_list:
                for param_name, param_value in params.items():
                    setattr(agent, param_name, param_value) # excluding check for now, fail fast if not present.
                    
    def run_simulation(self, output_data: bool):

        data = DataCollector(self.agents)

        for step in range(self.totalSimSteps):
            self._step()
            data.collect_data(step)

        data.display_data()
        if output_data:
            data.write_data(self.registry.output_dir)

    def _step(self):  
        for agent_type, agent_list in self.agents.items():
            for agent in agent_list:
                agent.increment_agent_param()
                agent.increment_mixin_attribute()
