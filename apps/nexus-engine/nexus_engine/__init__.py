"""Nexus Engine package for Terminal-V"""

from .main import NexusEngine, get_engine
from .services.aggregator import DataAggregatorService
from .models.aggregated_data import AggregatedData

__version__ = "0.1.0"

__all__ = [
    "NexusEngine",
    "get_engine",
    "DataAggregatorService",
    "AggregatedData",
]
