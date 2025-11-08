# Documentation for `registry.py`

## Class: `Registry`

The `Registry` class is designed to manage the loading and parsing of configuration files for a model run. It centralizes simulation and model configurations, making them easily accessible to other components of the ABM.

### Methods:

#### `__init__(self)`

Initializes the `Registry` object with empty dictionaries for `model_config`, `sim_config`, and `agent_configs`, and sets `sim_folder` to `None`.

#### `load_run_config_from_folder(self, folder_path: str) -> None`

*   **Purpose:** Finds and loads the main simulation configuration (`run_config.yaml`) from a specified model folder. It also loads model parameters and triggers the loading of agent configurations.
*   **Parameters:**
    *   `folder_path` (str): The path to the directory containing the `run_config.yaml` file.
*   **Raises:**
    *   `FileNotFoundError`: If the specified `folder_path` or `run_config.yaml` does not exist.
    *   `ValueError`: If the `simulation` or `model` objects are missing in `run_config.yaml`.
*   **Side Effects:** Populates `self.sim_config`, `self.model_config`, and calls `self._load_agent_configs()`.

#### `_load_agent_configs(self)`

*   **Purpose:** Loads agent-specific configuration details from YAML files referenced within the `model_config`.
*   **Assumptions:** Relies on `self.sim_folder` being set and `self.model_config` containing an 'agents' key with 'config_path' for each agent type.
*   **Raises:**
    *   `ValueError`: If the agent configuration or `config_path` is not found, or if the agent configuration file cannot be loaded or is empty.
*   **Side Effects:** Populates `self.agent_configs` with loaded agent data.
