from typing import List, Dict
import pandas as pd
from pathlib import Path


class AgentDataObject:
    def __init__(self, id):
        self.agent_id: int = id
        self.data: Dict[str, List] = {
            'step' : []
        }

    def add_data_attributes(self, attrs: List[str]):
        for attr in attrs:
            self.data[attr] = []

    def record_step(self, step, agent_object: object):
        self.data['step'].append(step)
        for attr in self.data.keys():
            if attr != 'step':
                data = getattr(agent_object, attr)
                self.data[attr].append(data)
    
    def return_data(self) -> pd.DataFrame:
        df = pd.DataFrame(self.data)
        df['agent_id'] = self.agent_id
        return df
    


class DataCollector:
    def __init__(self, agent_list: Dict[str, List[object]]):
        self.agent_list = agent_list
        self.agent_data_by_type: Dict[str, List[Dict]] = {}

        for agent_type in agent_list.keys():
            self.agent_data_by_type[agent_type] = []

    def collect_data(self, step):
        for agent_type, agents in self.agent_list.items():
            for agent in agents:
                agent.agent_data.record_step(step, agent)
            
    def display_data(self):
        for agent_type, agents in self.agent_list.items():
            print(f'Agent type: {agent_type}')
            for agent in agents:
                agent_data = agent.agent_data.return_data()
                print(agent_data)

    def write_data(self, output_dir: str):

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # combine all agent dfs into one df and then output to csv
        output_dfs: Dict[str, List[pd.DataFrame]] = {}
        for agent_type, agents in self.agent_list.items():
            agent_type_dfs = []
            for agent in agents:
                agent_df = agent.agent_data.return_data()
                agent_type_dfs.append(agent_df)
            output_dfs[agent_type] = agent_type_dfs

        # for each entry in output_dfs, create one file per agent type and combine into one df
        for agent_type, dfs in output_dfs.items():
            combined_df = pd.concat(dfs, ignore_index=True)
            output_file = output_path / f'{agent_type}_data.csv'
            combined_df.to_csv(output_file, index=False)

                
