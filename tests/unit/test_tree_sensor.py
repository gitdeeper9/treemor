"""
Unit tests for TreeSensor class.
Pure Python - NO NUMPY
"""

import unittest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from treomor.sensors.tree_sensor import TreeSensor


class TestTreeSensor(unittest.TestCase):
    """Test cases for TreeSensor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tree = TreeSensor(
            tree_id='TEST_001',
            species='douglas_fir',
            height=50.0,
            dbh=1.2,
            latitude=47.6,
            longitude=-122.3,
            soil_type='bedrock'
        )
    
    def test_initialization(self):
        """Test tree sensor initialization."""
        self.assertEqual(self.tree.tree_id, 'TEST_001')
        self.assertEqual(self.tree.species, 'douglas_fir')
        self.assertEqual(self.tree.height, 50.0)
        self.assertEqual(self.tree.dbh, 1.2)
        self.assertEqual(self.tree.latitude, 47.6)
        self.assertEqual(self.tree.longitude, -122.3)
        self.assertEqual(self.tree.soil_type, 'bedrock')
        self.assertEqual(self.tree.status, 'active')
    
    def test_mass_calculation(self):
        """Test tree mass calculation."""
        self.assertAlmostEqual(self.tree.mass, 25446.9, places=0)
    
    def test_moment_of_inertia(self):
        """Test moment of inertia calculation."""
        self.assertAlmostEqual(self.tree.I, 0.1018, places=4)
    
    def test_resonance_frequency(self):
        """Test resonance frequency calculation."""
        f0 = self.tree.calculate_resonance_frequency()
        self.assertGreater(f0, 0.3)
        self.assertLess(f0, 0.5)
    
    def test_coupling_coefficient_bedrock(self):
        """Test coupling coefficient for bedrock."""
        xi = self.tree.calculate_coupling_coefficient()
        self.assertGreater(xi, 0.75)
        self.assertLessEqual(xi, 1.0)
    
    def test_coupling_coefficient_sediment(self):
        """Test coupling coefficient for sediment."""
        tree_sediment = TreeSensor(
            tree_id='TEST_002',
            species='douglas_fir',
            height=50.0,
            dbh=1.2,
            latitude=47.6,
            longitude=-122.3,
            soil_type='sediment'
        )
        xi = tree_sediment.calculate_coupling_coefficient()
        self.assertLess(xi, 0.7)
    
    def test_damping_ratio(self):
        """Test damping ratio calculation."""
        zeta = self.tree.calculate_damping_ratio()
        self.assertGreater(zeta, 0.05)
        self.assertLess(zeta, 0.15)
    
    def test_bending_stiffness(self):
        """Test bending stiffness calculation."""
        EI = self.tree.calculate_bending_stiffness()
        self.assertGreater(EI, 1e9)
        self.assertLess(EI, 1.5e9)
    
    def test_fsin_parameters(self):
        """Test FSIN parameters generation."""
        params = self.tree.get_fsin_parameters()
        
        expected_keys = ['f0', 'xi', 'zeta', 'EI', 'sigma_inf', 
                         'delta_p_sap', 'Z_RS', 'ADI', 'tau_lead']
        
        for key in expected_keys:
            self.assertIn(key, params)
            self.assertIsNotNone(params[key])
    
    def test_to_dict(self):
        """Test dictionary conversion."""
        data = self.tree.to_dict()
        
        self.assertEqual(data['tree_id'], 'TEST_001')
        self.assertEqual(data['species'], 'douglas_fir')
        self.assertEqual(data['height'], 50.0)
        self.assertIn('location', data)
        self.assertIn('fsin_parameters', data)
    
    def test_to_json(self):
        """Test JSON conversion."""
        json_str = self.tree.to_json()
        data = json.loads(json_str)
        
        self.assertEqual(data['tree_id'], 'TEST_001')
        self.assertIsInstance(data, dict)
    
    def test_calibrate(self):
        """Test calibration functionality."""
        self.assertIsNone(self.tree.last_calibration)
        
        self.tree.calibrate(measured_f0=0.45, measured_xi=0.82)
        
        self.assertIsNotNone(self.tree.last_calibration)
    
    def test_health_check_healthy(self):
        """Test health check for healthy tree."""
        is_healthy, msg = self.tree.health_check()
        self.assertTrue(is_healthy)
        self.assertEqual(msg, "OK")
    
    def test_health_check_unhealthy(self):
        """Test health check for unhealthy tree."""
        self.tree.status = "offline"
        is_healthy, msg = self.tree.health_check()
        self.assertFalse(is_healthy)
        self.assertIn("offline", msg)


if __name__ == '__main__':
    unittest.main()
