"""
TREEMOR Engine - Core detection engine.
Pure Python implementation - NO NUMPY
"""

import math
from typing import Dict, Optional, Tuple, List
from datetime import datetime


class TREEMOREngine:
    """
    Core detection engine for seismic events.
    
    Processes tree sensor data and detects earthquakes/infrasonic events.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize detection engine."""
        self.config = config or {}
        self.detection_threshold = self.config.get('detection_threshold', 0.6)
        self.p_wave_velocity = self.config.get('p_wave_velocity', 6.0)
        self.s_wave_velocity = self.config.get('s_wave_velocity', 3.5)
    
    def calculate_lead_time(self, distance_km: float) -> float:
        """Calculate P-wave lead time before S-wave arrival."""
        if self.p_wave_velocity <= 0 or self.s_wave_velocity <= 0:
            return 0.0
        lead_time = (distance_km / self.s_wave_velocity) - (distance_km / self.p_wave_velocity)
        return max(0.0, round(lead_time, 2))
    
    def estimate_magnitude(self, amplitude: float, distance_km: float) -> float:
        """Estimate earthquake magnitude from tree displacement."""
        if amplitude <= 0 or distance_km <= 0:
            return 0.0
        magnitude = math.log10(amplitude * distance_km) + 2.5
        return round(magnitude, 1)
    
    def get_status(self) -> Dict:
        """Get engine status."""
        return {
            "status": "active",
            "detection_threshold": self.detection_threshold,
            "p_wave_velocity_kms": self.p_wave_velocity,
            "s_wave_velocity_kms": self.s_wave_velocity
        }
