import logging
from typing import Dict, Any
from mini_macro_abm.core.data_collector import AgentDataObject

logger = logging.getLogger(__name__)

class BaseAgent:
    """
    Base Agent class used by all agents in the simulation.
    Will contain the StockMatrix.
    """

    def __init__(self, id):
        super().__init__()
        self.id = id
        self.agent_data = AgentDataObject(id)
        # will add stock matrix here
        pass

