"""
Forest Network - Distributed seismic monitoring network.
Pure Python implementation - NO NUMPY
"""

import math
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class ForestNetwork:
    """
    Distributed forest seismic monitoring network.
    Manages multiple tree sensors as a unified detection array.
    """
    
    def __init__(self, name: str = "TREEMOR Network"):
        """
        Initialize forest network.
        
        Args:
            name: Network name
        """
        self.name = name
        self.sensors: Dict[str, object] = {}  # tree_id -> TreeSensor
        self.events: List[Dict] = []
        self.detection_threshold = 0.6  # Minimum TSSI for detection
        self.consensus_threshold = 3  # Minimum trees for event confirmation
        
    def add_sensor(self, sensor) -> bool:
        """
        Add a tree sensor to the network.
        
        Args:
            sensor: TreeSensor instance
        
        Returns:
            True if added successfully
        """
        if sensor.tree_id in self.sensors:
            return False
        
        self.sensors[sensor.tree_id] = sensor
        return True
    
    def remove_sensor(self, tree_id: str) -> bool:
        """
        Remove a sensor from the network.
        
        Args:
            tree_id: Sensor identifier
        
        Returns:
            True if removed
        """
        if tree_id in self.sensors:
            del self.sensors[tree_id]
            return True
        return False
    
    def get_sensor(self, tree_id: str):
        """Get sensor by ID."""
        return self.sensors.get(tree_id)
    
    def get_active_sensors(self) -> List:
        """Get all active sensors."""
        return [s for s in self.sensors.values() if s.status == "active"]
    
    def network_tssi(self) -> float:
        """
        Calculate average network TSSI.
        
        Returns:
            Average TSSI across all sensors
        """
        from ..core.tssi import TSSICalculator
        
        tssi_calc = TSSICalculator()
        tssi_scores = []
        
        for sensor in self.sensors.values():
            params = sensor.get_fsin_parameters()
            tssi = tssi_calc.calculate_tssi(params)
            tssi_scores.append(tssi)
        
        if not tssi_scores:
            return 0.0
        
        return sum(tssi_scores) / len(tssi_scores)
    
    def detect_event(self, p_wave_arrival: float, epicenter: Tuple[float, float]) -> Optional[Dict]:
        """
        Detect seismic event from network response.
        
        Args:
            p_wave_arrival: P-wave arrival time (seconds since epoch)
            epicenter: (lat, lon) estimated epicenter
        
        Returns:
            Event dictionary or None if no detection
        """
        # Get all sensors that would detect this event
        triggered_sensors = []
        
        for sensor in self.sensors.values():
            # Calculate distance to epicenter
            dist = self._haversine_distance(
                sensor.latitude, sensor.longitude,
                epicenter[0], epicenter[1]
            )
            
            # Check if sensor can detect at this distance
            if dist <= 200:  # Detection range for M≥3.5
                triggered_sensors.append({
                    "tree_id": sensor.tree_id,
                    "distance_km": dist,
                    "tssi": self._get_sensor_tssi(sensor)
                })
        
        # Check consensus threshold
        if len(triggered_sensors) >= self.consensus_threshold:
            event = {
                "event_id": f"TREEMOR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": p_wave_arrival,
                "epicenter": epicenter,
                "triggered_sensors": len(triggered_sensors),
                "sensors": triggered_sensors,
                "detected": True
            }
            self.events.append(event)
            return event
        
        return None
    
    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate great-circle distance between two points.
        
        Args:
            lat1, lon1: First point coordinates
            lat2, lon2: Second point coordinates
        
        Returns:
            Distance in kilometers
        """
        R = 6371  # Earth's radius in km
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = math.sin(delta_phi / 2) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * \
            math.sin(delta_lambda / 2) ** 2
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        
        return round(distance, 2)
    
    def _get_sensor_tssi(self, sensor) -> float:
        """Calculate TSSI for a sensor."""
        from ..core.tssi import TSSICalculator
        
        tssi_calc = TSSICalculator()
        params = sensor.get_fsin_parameters()
        return tssi_calc.calculate_tssi(params)
    
    def get_network_statistics(self) -> Dict:
        """
        Get network statistics.
        
        Returns:
            Dictionary with network metrics
        """
        active = self.get_active_sensors()
        
        if not active:
            return {"total_sensors": len(self.sensors), "active": 0}
        
        # Calculate average TSSI
        avg_tssi = self.network_tssi()
        
        # Count by soil type
        soil_counts = {}
        for sensor in active:
            st = sensor.soil_type
            soil_counts[st] = soil_counts.get(st, 0) + 1
        
        return {
            "name": self.name,
            "total_sensors": len(self.sensors),
            "active_sensors": len(active),
            "average_tssi": avg_tssi,
            "soil_type_distribution": soil_counts,
            "events_detected": len(self.events),
            "network_health": "GOOD" if avg_tssi >= 0.6 else "MODERATE"
        }
    
    def get_best_sensors(self, top_n: int = 10) -> List[Dict]:
        """
        Get top sensors by TSSI.
        
        Args:
            top_n: Number of sensors to return
        
        Returns:
            List of top sensors
        """
        sensor_scores = []
        
        for sensor in self.sensors.values():
            tssi = self._get_sensor_tssi(sensor)
            sensor_scores.append({
                "tree_id": sensor.tree_id,
                "species": sensor.species,
                "location": (sensor.latitude, sensor.longitude),
                "tssi": tssi
            })
        
        # Sort by TSSI descending
        sensor_scores.sort(key=lambda x: x["tssi"], reverse=True)
        
        return sensor_scores[:top_n]
    
    def to_dict(self) -> Dict:
        """Convert network to dictionary."""
        return {
            "name": self.name,
            "statistics": self.get_network_statistics(),
            "sensors": [s.to_dict() for s in self.sensors.values()],
            "events": self.events[-10:]  # Last 10 events
        }
    
    def to_json(self) -> str:
        """Convert network to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)
