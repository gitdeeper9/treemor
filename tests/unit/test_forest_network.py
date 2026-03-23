"""
Unit tests for ForestNetwork class.
Pure Python - NO NUMPY
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from treomor.network.forest_network import ForestNetwork
from treomor.sensors.tree_sensor import TreeSensor


class TestForestNetwork(unittest.TestCase):
    """Test cases for ForestNetwork class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.network = ForestNetwork("Test Network")
        
        # Create test trees
        self.tree1 = TreeSensor(
            tree_id='T01',
            species='douglas_fir',
            height=52.0,
            dbh=1.2,
            latitude=47.6,
            longitude=-122.3,
            soil_type='bedrock'
        )
        
        self.tree2 = TreeSensor(
            tree_id='T02',
            species='ponderosa_pine',
            height=45.0,
            dbh=1.0,
            latitude=47.7,
            longitude=-122.4,
            soil_type='soil'
        )
        
        self.tree3 = TreeSensor(
            tree_id='T03',
            species='redwood',
            height=65.0,
            dbh=1.5,
            latitude=47.5,
            longitude=-122.2,
            soil_type='bedrock'
        )
    
    def test_add_sensor(self):
        """Test adding sensors to network."""
        self.network.add_sensor(self.tree1)
        self.network.add_sensor(self.tree2)
        
        self.assertEqual(len(self.network.sensors), 2)
        self.assertIn('T01', self.network.sensors)
        self.assertIn('T02', self.network.sensors)
    
    def test_add_duplicate_sensor(self):
        """Test adding duplicate sensor returns False."""
        self.network.add_sensor(self.tree1)
        result = self.network.add_sensor(self.tree1)
        
        self.assertFalse(result)
        self.assertEqual(len(self.network.sensors), 1)
    
    def test_remove_sensor(self):
        """Test removing sensor."""
        self.network.add_sensor(self.tree1)
        self.network.add_sensor(self.tree2)
        
        result = self.network.remove_sensor('T01')
        
        self.assertTrue(result)
        self.assertEqual(len(self.network.sensors), 1)
        self.assertNotIn('T01', self.network.sensors)
    
    def test_remove_nonexistent_sensor(self):
        """Test removing nonexistent sensor."""
        result = self.network.remove_sensor('NONEXISTENT')
        self.assertFalse(result)
    
    def test_get_sensor(self):
        """Test retrieving sensor by ID."""
        self.network.add_sensor(self.tree1)
        
        sensor = self.network.get_sensor('T01')
        self.assertIsNotNone(sensor)
        self.assertEqual(sensor.tree_id, 'T01')
        
        sensor = self.network.get_sensor('NONEXISTENT')
        self.assertIsNone(sensor)
    
    def test_get_active_sensors(self):
        """Test getting active sensors."""
        self.tree2.status = "offline"
        self.network.add_sensor(self.tree1)
        self.network.add_sensor(self.tree2)
        self.network.add_sensor(self.tree3)
        
        active = self.network.get_active_sensors()
        
        self.assertEqual(len(active), 2)
        self.assertIn(self.tree1, active)
        self.assertIn(self.tree3, active)
        self.assertNotIn(self.tree2, active)
    
    def test_network_tssi(self):
        """Test network average TSSI calculation."""
        self.network.add_sensor(self.tree1)
        self.network.add_sensor(self.tree2)
        self.network.add_sensor(self.tree3)
        
        avg_tssi = self.network.network_tssi()
        
        # Should be between 0 and 1
        self.assertGreaterEqual(avg_tssi, 0)
        self.assertLessEqual(avg_tssi, 1)
    
    def test_detect_event_consensus(self):
        """Test event detection with consensus."""
        self.network.add_sensor(self.tree1)
        self.network.add_sensor(self.tree2)
        self.network.add_sensor(self.tree3)
        
        # Epicenter near sensors
        event = self.network.detect_event(1000000, (47.6, -122.3))
        
        if event and event['detected']:
            self.assertIn('event_id', event)
            self.assertIn('epicenter', event)
            self.assertGreater(event['triggered_sensors'], 0)
    
    def test_haversine_distance(self):
        """Test haversine distance calculation."""
        # Distance between same point should be 0
        dist = self.network._haversine_distance(47.6, -122.3, 47.6, -122.3)
        self.assertEqual(dist, 0.0)
        
        # Approximate distance between Seattle and Portland (~230 km)
        dist = self.network._haversine_distance(47.6062, -122.3321, 45.5152, -122.6784)
        self.assertGreater(dist, 200)
        self.assertLess(dist, 250)
    
    def test_get_network_statistics(self):
        """Test network statistics."""
        self.network.add_sensor(self.tree1)
        self.network.add_sensor(self.tree2)
        self.network.add_sensor(self.tree3)
        
        stats = self.network.get_network_statistics()
        
        self.assertEqual(stats['name'], 'Test Network')
        self.assertEqual(stats['total_sensors'], 3)
        self.assertIn('soil_type_distribution', stats)
        self.assertIn('average_tssi', stats)
    
    def test_get_best_sensors(self):
        """Test getting best sensors by TSSI."""
        self.network.add_sensor(self.tree1)
        self.network.add_sensor(self.tree2)
        self.network.add_sensor(self.tree3)
        
        best = self.network.get_best_sensors(2)
        
        self.assertEqual(len(best), 2)
        # Best sensors should be sorted by TSSI descending
        self.assertGreaterEqual(best[0]['tssi'], best[1]['tssi'])
    
    def test_to_dict(self):
        """Test dictionary conversion."""
        self.network.add_sensor(self.tree1)
        
        data = self.network.to_dict()
        
        self.assertEqual(data['name'], 'Test Network')
        self.assertIn('statistics', data)
        self.assertIn('sensors', data)
    
    def test_empty_network_tssi(self):
        """Test TSSI for empty network."""
        avg_tssi = self.network.network_tssi()
        self.assertEqual(avg_tssi, 0.0)


if __name__ == '__main__':
    unittest.main()
