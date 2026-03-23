"""
Unit tests for TSSI Calculator.
Pure Python - NO NUMPY
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from treomor.core.tssi import TSSICalculator


class TestTSSICalculator(unittest.TestCase):
    """Test cases for TSSICalculator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = TSSICalculator()
    
    def test_normalize_f0(self):
        """Test normalization of resonance frequency."""
        norm = self.calc.normalize('f0', 0.3)
        self.assertEqual(norm, 0.0)
        
        norm = self.calc.normalize('f0', 2.5)
        self.assertEqual(norm, 1.0)
        
        norm = self.calc.normalize('f0', 1.4)
        expected = (1.4 - 0.3) / (2.5 - 0.3)
        self.assertAlmostEqual(norm, expected, places=3)
    
    def test_normalize_xi(self):
        """Test normalization of coupling coefficient."""
        norm = self.calc.normalize('xi', 0)
        self.assertEqual(norm, 0.0)
        
        norm = self.calc.normalize('xi', 1)
        self.assertEqual(norm, 1.0)
        
        norm = self.calc.normalize('xi', 0.5)
        self.assertEqual(norm, 0.5)
    
    def test_normalize_invalid_parameter(self):
        """Test normalization with invalid parameter name."""
        norm = self.calc.normalize('invalid', 10)
        self.assertEqual(norm, 0.0)
    
    def test_calculate_tssi_good_sensor(self):
        """Test TSSI for a good sensor."""
        params = {
            'f0': 0.48,
            'xi': 0.85,
            'zeta': 0.08,
            'sigma_inf': 80,
            'delta_p_sap': 500,
            'EI': 1e10,
            'Z_RS': 6.0,
            'ADI': 10.0,
            'tau_lead': 12.0
        }
        
        tssi = self.calc.calculate_tssi(params)
        
        # Good sensor should have TSSI > 0.35
        self.assertGreater(tssi, 0.35)
    
    def test_calculate_tssi_poor_sensor(self):
        """Test TSSI for a poor sensor."""
        params = {
            'f0': 0.2,
            'xi': 0.3,
            'zeta': 0.25,
            'sigma_inf': 10,
            'delta_p_sap': 50,
            'EI': 1e8,
            'Z_RS': 1.0,
            'ADI': 0.5,
            'tau_lead': 2.0
        }
        
        tssi = self.calc.calculate_tssi(params)
        
        self.assertLess(tssi, 0.3)
    
    def test_calculate_tssi_empty_params(self):
        """Test TSSI with empty parameters."""
        tssi = self.calc.calculate_tssi({})
        self.assertEqual(tssi, 0.0)
    
    def test_classify_sensitivity_exceptional(self):
        """Test sensitivity classification for exceptional sensor."""
        category, desc = self.calc.classify_sensitivity(0.85)
        self.assertEqual(category, "EXCEPTIONAL")
        self.assertIn("bedrock", desc.lower())
    
    def test_classify_sensitivity_good(self):
        """Test sensitivity classification for good sensor."""
        category, desc = self.calc.classify_sensitivity(0.70)
        self.assertEqual(category, "GOOD")
    
    def test_classify_sensitivity_moderate(self):
        """Test sensitivity classification for moderate sensor."""
        category, desc = self.calc.classify_sensitivity(0.45)
        self.assertEqual(category, "MODERATE")
    
    def test_classify_sensitivity_poor(self):
        """Test sensitivity classification for poor sensor."""
        category, desc = self.calc.classify_sensitivity(0.20)
        self.assertEqual(category, "POOR")
    
    def test_get_improvement_recommendations(self):
        """Test improvement recommendations."""
        params = {
            'xi': 0.4,
            'ADI': 1.0,
            'Z_RS': 1.5
        }
        
        recs = self.calc.get_improvement_recommendations(params)
        
        self.assertGreater(len(recs), 0)
    
    def test_compare_sites(self):
        """Test site comparison functionality."""
        sites = {
            'Site_A': {'f0': 0.48, 'xi': 0.85, 'zeta': 0.08},
            'Site_B': {'f0': 0.35, 'xi': 0.65, 'zeta': 0.12},
            'Site_C': {'f0': 0.55, 'xi': 0.92, 'zeta': 0.06}
        }
        
        results = self.calc.compare_sites(sites)
        
        self.assertEqual(len(results), 3)


if __name__ == '__main__':
    unittest.main()
