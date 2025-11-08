import pytest
from mini_macro_abm.core.registry import Registry

class TestRegistry:
    """Registry test cases for now"""

    def test_registry_initialization(self):
        registry = Registry()
        assert registry.sim_config == {}
        assert registry.model_config == {}

    def test_load_run_config_from_folder(self):
        test_sim_config = "src/models/simple_model"
        registry = Registry()

        registry.load_run_config_from_folder(test_sim_config)
        assert registry.sim_config is not None
        assert registry.model_config is not None

