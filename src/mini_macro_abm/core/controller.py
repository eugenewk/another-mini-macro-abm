import logging
from typing import List
from mini_macro_abm.core.registry import Registry
from mini_macro_abm.core.agent_factory.factory import AgentFactory
from mini_macro_abm.core.sim_engine.engine import SimEngine

logger = logging.getLogger(__name__)

class Controller:
    def __init__(self):
        self.registry = Registry()
        self.factory = AgentFactory(self.registry)
        self.simEngine = None # set at runtime


    def run_simulation(self, model_folder: str):
        '''
            Order of operations here:
            1. Load the model and the component registry
            2. Send to the agent factory to create all the agents
            3. Pass all agents and markets to the simulation engine
            4. Trigger simulation and data collection
            5. Trigger data analysis and output visualization
        '''
        # first, clear and populate the registry with the model components
        self.registry.clear()
        self.registry.load_run_config_from_folder(model_folder) 
        # print(self.registry)

        # pass the registry to the agent factory to get back the composed classes
        agentClasses = self.factory.compose_all_agent_classes()
        # print(agentClasses)

        # pass those classes back to get the agents
        agentRoster = self.factory.instantiate_agents(agentClasses)
        print(agentRoster)

        # assign roster to sim engine
        self.simEngine = SimEngine(self.registry, agentRoster)

        # pass registry and agent objects to the sim engine
        self.simEngine.set_initial_agent_values()
        print(agentRoster)

        # load simulation parameters into engine
        self.simEngine.set_simulation_params()
        print(self.simEngine.totalSimSteps)

        # run sim!
        self.simEngine.run_simulation()
        print(agentRoster)

        


# test script to run simulation
controller = Controller()
controller.run_simulation('src/models/simple_model')






        
            