from typing import List, Dict
import pandas as pd
from pathlib import Path
from mini_macro_abm.core.agent_utils.stock_matrix import StockMatrix
import copy

# helper functions

class AgentDataObject:
    def __init__(self, id, stock_matrix):
        self.agent_id: int = id
        self.stock_matrix: StockMatrix = stock_matrix
        self.data: Dict[str, List] = {
            'step' : [],
            'stock_matrix_snapshots' : []
        }

    def add_data_attributes(self, attrs: List[str]):
        # handle case where single string is added
        if isinstance(attrs, str):
            attrs = [attrs]

        for attr in attrs:
            self.data[attr] = []

    def record_step(self, step, agent_object: object):    
        # append step data
        self.data['step'].append(step)

        # record stock matrix
        snapshot = copy.deepcopy(self.stock_matrix) 
        self.data['stock_matrix_snapshots'].append(snapshot)

        # record other params
        for attr in self.data.keys():
            if attr != 'step' and attr != 'stock_matrix_snapshots':
                data = getattr(agent_object, attr)
                self.data[attr].append(copy.deepcopy(data))
    
    def return_data(self) -> pd.DataFrame:
        df = pd.DataFrame(self.data)
        df['agent_id'] = self.agent_id
        return df

class MarketDataObject: # noting this is mostly a duplicate of the above for now, will change later if it's an issue.
    def __init__(self, name):
        self.market_name: str = name
        self.data: Dict[str, List] = {'step' : [],}

    def add_data_attributes(self, attrs: List[str]):
        if isinstance(attrs, str):
            attrs = [attrs]
            
        for attr in attrs:
            self.data[attr] = []

    def record_step(self, step, market_object: object):    
        # append step data
        self.data['step'].append(step)

        # print(self.data.keys())

        # record params
        for attr in self.data.keys():
            if attr != 'step' and attr != 'stock_matrix_snapshots':
                data = getattr(market_object, attr)
                self.data[attr].append(copy.deepcopy(data))
    
    def return_data(self) -> pd.DataFrame:
        df = pd.DataFrame(self.data)
        df['market_id'] = self.market_name
        return df

class DataCollector:
    def __init__(self, agent_list: Dict[str, List[object]], market_list: Dict[str, object]):
        self.agent_list = agent_list
        self.agent_data_by_type: Dict[str, List[Dict]] = {}

        self.market_list = market_list
        self.market_data_by_type: Dict[str, List[Dict]] = {}

        for agent_type in agent_list.keys():
            self.agent_data_by_type[agent_type] = []

        for market_type in market_list.keys():
            self.market_data_by_type[market_type] = []

    def collect_data(self, step):
        for agent_type, agents in self.agent_list.items():
            for agent in agents:
                agent.agent_data.record_step(step, agent)

        for market_name, market in self.market_list.items():
            market.market_data.record_step(step, market)
            
    def display_data(self):
        for agent_type, agents in self.agent_list.items():
            print(f'Agent type: {agent_type}')
            for agent in agents:
                agent_data = agent.agent_data.return_data()
                print(agent_data)
        for market_name, market_obj in self.market_list.items():
            print(f'Market step data:')
            market_data = market_obj.market_data.return_data()
            print(market_data)

    def write_data(self, output_dir: str):

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # combine all agent dfs into one df and then output to csv
        output_dfs: Dict[str, List[pd.DataFrame]] = {}

        # create output dfs for each agent type
        for agent_type, agents in self.agent_list.items():
            agent_type_dfs = []
            for agent in agents:
                agent_df = agent.agent_data.return_data()
                agent_type_dfs.append(agent_df)
            output_dfs[agent_type] = agent_type_dfs

        # TODO: need to add market outputs to csv as well
        for market_type, market in self.market_list.items():
            market_df = market.market_data.return_data()
            output_dfs[market_type] = [market_df]
        
        # for each entry in output_dfs, create one file per agent type and combine into one df
        for agent_type, dfs in output_dfs.items():
            combined_df = pd.concat(dfs, ignore_index=True)
            output_file = output_path / f'{agent_type}_data.csv'
            combined_df.to_csv(output_file, index=False)





                
