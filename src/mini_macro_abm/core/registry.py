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
        # used for tracking the run config and model 
        self.run_config_file = None
        self.output_dir = None

        # these store the data from the files and form the registry
        self.model_pkg = None
        self.model_config: Dict[str, Any] = {}
        self.sim_config: Dict[str, Any] = {}
        self.agent_configs: Dict[str, Any] = {}
        self.market_configs: Dict[str, Any] = {}


    def clear(self) -> None:
        self.run_config_file = None
        self.output_dir = None
        self.model_pkg = None
        self.model_config.clear()
        self.sim_config.clear()
        self.agent_configs.clear()
        self.market_configs.clear()

    def _display(self) -> None:
        print("Registry displaying...")
        print("model config:")
        print(self.model_config)
        print("sim config:")
        print(self.sim_config)
        print("agent configs:")
        print(self.agent_configs)
        print("market configs:")
        print(self.market_configs)

    def _resolve_path(self, relative_path: str) -> str:
        if not self.model_pkg:
            raise ValueError("no model_pkg set in config")
        return f"{self.model_pkg}.{relative_path}"
    
    def _resolve_agent_paths(self):
        for agent_name, agent_config in self.agent_configs.items():
            agent_dir = f"agents.{agent_config.get('agent_dir')}"
            if not agent_dir:
                raise ValueError(f"agent dir not found for {agent_name}")
            
            if 'agent_class' in agent_config:
                agent_config['agent_class_path'] = self._resolve_path(
                    f"{agent_dir}.{agent_config['agent_class']}"
                )

            if 'mixins' in agent_config:
                agent_config['mixins'] = [
                    self._resolve_path(f"{agent_dir}.mixins.{mixin_path}")
                    for mixin_path in agent_config['mixins']
                ]

    def _resolve_market_paths(self):
        for market_name, market_config in self.market_configs.items():
            if 'market_class_path' in market_config:
                market_config['market_class_path'] = self._resolve_path(
                    market_config['market_class_path']
                )
        

    def load_config(self, run_config: str) -> None:
        self.run_config_file = run_config

        with open(self.run_config_file, 'r') as f:
            run_config_data = yaml.safe_load(f)

        # print('run config:')
        # print(run_config_data)

        # load sim config block
        self.sim_config = run_config_data.get('simulation')
        # get output dir from the sim config block
        self.output_dir = self.sim_config.get('output_dir')

        # load model config
        self.model_config = run_config_data.get('model')

        # print('model config:')
        # print(self.model_config)

        # load agent configs
        self.agent_configs = self.model_config.get('agents')

        # load market configs
        self.market_configs = self.model_config.get('markets')

        # now resolve all agent paths using model_dir
        self.model_pkg = f"models.{self.model_config.get('model_dir')}"
        if not self.model_pkg:
            raise ValueError("no model_pkg specified in config")

        self._resolve_agent_paths()
        self._resolve_market_paths()

        # print("registry loading complete...")
        # self._display()
        
