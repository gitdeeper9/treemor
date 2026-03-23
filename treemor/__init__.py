"""
TREEMOR - Tree-Based Earth Motion Resonance
Bio-Seismic Sensing & Planetary Infrasound Resonance

A nine-parameter biomechanical seismology framework that transforms
forests into a planetary-scale distributed seismic monitoring network.

Author: Samir Baladi
DOI: 10.5281/zenodo.19183878
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Samir Baladi"
__email__ = "gitdeeper@gmail.com"
__doi__ = "10.5281/zenodo.19183878"
__license__ = "MIT"
__url__ = "https://treomor.netlify.app"

from .core.fsin import FSINCalculator
from .core.tssi import TSSICalculator
from .sensors.tree_sensor import TreeSensor
from .network.forest_network import ForestNetwork

__all__ = [
    "FSINCalculator",
    "TSSICalculator", 
    "TreeSensor",
    "ForestNetwork",
    "__version__",
    "__doi__"
]
