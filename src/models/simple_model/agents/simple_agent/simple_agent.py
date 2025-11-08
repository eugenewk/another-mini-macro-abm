"""simple agent file"""

class SimpleAgent:

    def __init__(self):
        super().__init__()
        self.agent_param = 0

    def __repr__(self):
        return f"simple agent, param: {self.agent_param}"

    def increment_agent_param(self):
        self.agent_param += 1

    def provide_data(self):
        return self.agent_param
    
