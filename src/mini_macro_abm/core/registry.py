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
        self.model_config: Dict[str, Any] = {}
        self.sim_config: Dict[str, Any] = {}
        self.agent_configs: Dict[str, Any] = {}
        self.sim_folder = None # to delete
        
        self.run_config_file = None
        self.model_folder = None

    def clear(self) -> None:
        self.model_config = {}
        self.sim_config = {}
        self.agent_configs = {}
        self.sim_folder = None

    def load_run_config(self, run_config_file:str) -> None:
        
        self.run_config_file = run_config_file
        
        with open(run_config_file, 'r') as f:
            run_config_data = yaml.safe_load(f)

        # set simulation config from run config folder (sim steps)
        self.sim_config = run_config_data.get('simulation')

        model_ref = run_config_data.get('model')
        model_config_path = model_ref.get('model_config')
        if not model_config_path:
            raise ValueError("Run config must point to a model_config.yaml file")

        self.model_folder = Path(model_config_path).parent # returns the parent folder of the model config file
        
        with open(model_config_path, 'r') as f:
            model_config = yaml.safe_load(f)

        self.model_config = model_config.get('model')

        if self.sim_config is None:
            raise ValueError(f"missing simulation object in run_config.yaml in {self.sim_folder}")
        
        if self.model_config is None:
            raise ValueError(f"missing model object in run_config.yaml in {self.sim_folder}")

        logger.info(f"loaded config from {run_config_file}")

        self._load_agent_configs()
        
    def _load_agent_configs(self):
        """Load agent configurations from relative file paths"""
        agents_config = self.model_config.get('agents')

        if agents_config is None:
            raise ValueError(f"agent config not found in {self.sim_folder}")
        
        for agent_type, agent_config in agents_config.items():
            if 'config_path' in agent_config:
                agent_file = self.model_folder / agent_config['config_path']

                if agent_file.exists():
                    with open(agent_file, 'r') as f:
                        agent_data=yaml.safe_load(f)
                        if agent_type not in self.agent_configs:
                            self.agent_configs[agent_type] = {}
                        self.agent_configs[agent_type].update(agent_data)
                        if self.agent_configs[agent_type] == {}:
                            raise ValueError(f"agent config not loaded from {agent_file}")
                else:
                    raise ValueError(f"agent config file not found at {agent_file}")
            else:
                raise ValueError(f"agent config_path not found for {agent_type} in {self.sim_folder}")


