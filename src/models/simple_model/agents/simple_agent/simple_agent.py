"""simple agent file"""
from models.simple_model.agents.simple_agent.mixins import simple_mixin
from mini_macro_abm.core.agent_factory.base_agent import BaseAgent

class SimpleAgent:

    def __init__(self):
        super().__init__()
        self.agent_param = 0
        self.mixin_param = 0

    def __repr__(self):
        return f"simple agent, param: {self.agent_param}"

    def increment_agent_param(self):
        self.agent_param += 1

    # define data outputs here
    def get_agent_data(self):
        self.agent_data.data = {
            'agent_param': self.agent_param,
            'mixin_param': self.mixin_param   
        }
       


    
