from typing import List, Dict


class AgentDataObject:
    def __init__(self, id):
        self.agent_id: int = id
        self.data: Dict = {}

    def get_agent_state_data(self, step):
        data_dict = {
            'step': step,
            'id': self.agent_id,
            'data': self.data
        }
        return data_dict

class DataCollector:
    def __init__(self, agent_list: Dict[str, List[object]]):
        self.agent_list = agent_list
        self.agent_data_by_type: Dict[str, List[Dict]] = {}

        for agent_type in agent_list.keys():
            self.agent_data_by_type[agent_type] = []

    def collect_data(self, step):
        for agent_type, agents in self.agent_list.items():
            for agent in agents:
                data = agent.agent_data.get_agent_state_data(step)
                self.agent_data_by_type[agent_type].append(data)
            

    def display_data(self):
        for data in self.agent_data_by_type.items():
            for item in data:
                print(item)

