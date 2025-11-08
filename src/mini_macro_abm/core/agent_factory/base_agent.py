import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BaseAgent:
    """
    Base Agent class used by all agents in the simulation.
    Will contain the StockMatrix.
    """

    def __init__(self):
        super().__init__()
        # will add stock matrix here
        pass

