"""
    The registry is responsible for parsing the YAML input files for each model run. It stores everything in a single object to allow for easy access for other core model components. 
"""

import yaml
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Registry:
    def __init__(self):
        # used for tracking the run config and model folders
        self.run_config_file = None
        self.model_folder = None
        self.output_dir = None

        # these store the data from the files and form the registry
        self.model_config: Dict[str, Any] = {}
        self.sim_config: Dict[str, Any] = {}
        self.agent_configs: Dict[str, Any] = {}
        self.market_configs: Dict[str, Any] = {}


    def clear(self) -> None:
        self.run_config_file = None
        self.model_folder = None
        self.output_dir = None
        self.model_config.clear()
        self.sim_config.clear()
        self.agent_configs.clear()
        self.market_configs.clear()
        

    def load_config(self, run_config: str) -> None:
        self.run_config_file = run_config

        with open(self.run_config_file, 'r') as f:
            run_config_data = yaml.safe_load(f)

        print('run config:')
        print(run_config_data)

        # load sim config block
        self.sim_config = run_config_data.get('simulation')
        # get output dir from the sim config block
        self.output_dir = self.sim_config.get('output_dir')

        # load model config
        self.model_config = run_config_data.get('model')

        print('model config:')
        print(self.model_config)

        # load agent configs
        self.agent_configs = self.model_config.get('agents')

        # load market configs
        self.market_configs = self.model_config.get('markets')