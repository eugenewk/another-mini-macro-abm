"""simple agent file"""
from models.simple_model.agents.simple_agent.mixins import simple_mixin
from mini_macro_abm.core.agent_factory.base_agent import BaseAgent
from mini_macro_abm.core.data_collector import AgentDataObject

class SimpleAgent:

    def __init__(self, id):
        # core setup params, requires id given by sim engine
        super().__init__()
        self.id = id
        self.agent_data = AgentDataObject(id) # creates data tracking object

        # define all custom agent params here
        self.agent_param = 0
        self.mixin_param = 0 # note that this is used by a mixin function
        self.test_param = 'nothing'

        # add the desired data fields to tracking
        self.agent_data.add_data_attributes(['agent_param', 'mixin_param', 'test_param'])

    def __repr__(self):
        return f"{self.id}"

    def increment_agent_param(self):
        self.agent_param += 2
       


    
