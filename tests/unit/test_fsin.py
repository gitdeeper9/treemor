"""
Unit tests for FSIN Calculator.
Pure Python - NO NUMPY
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from treomor.core.fsin import FSINCalculator


class TestFSINCalculator(unittest.TestCase):
    """Test cases for FSINCalculator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = FSINCalculator()
    
    def test_resonance_frequency_douglas_fir(self):
        """Test resonance frequency for typical Douglas fir."""
        E = 13e9
        D = 1.2
        I = 3.14159 * (D ** 4) / 64
        m = 450
        L = 50
        
        f0 = self.calc.calculate_resonance_frequency(E, I, m, L)
        
        self.assertGreater(f0, 0.3)
        self.assertLess(f0, 0.5)
    
    def test_resonance_frequency_small_tree(self):
        """Test resonance frequency for small tree (higher frequency)."""
        E = 10e9
        D = 0.3
        I = 3.14159 * (D ** 4) / 64
        m = 500
        L = 10
        
        f0 = self.calc.calculate_resonance_frequency(E, I, m, L)
        
        self.assertGreater(f0, 0.4)
        self.assertLess(f0, 1.5)
    
    def test_coupling_coefficient_bedrock(self):
        """Test coupling coefficient for bedrock (high coupling)."""
        Z_root = 3.0
        Z_soil = 8.0
        
        xi = self.calc.calculate_coupling_coefficient(Z_root, Z_soil)
        
        self.assertGreater(xi, 0.75)
        self.assertLessEqual(xi, 1.0)
    
    def test_coupling_coefficient_sediment(self):
        """Test coupling coefficient for sediment (low coupling)."""
        Z_root = 3.0
        Z_soil = 0.8
        
        xi = self.calc.calculate_coupling_coefficient(Z_root, Z_soil)
        
        self.assertLess(xi, 0.7)
        self.assertGreaterEqual(xi, 0.0)
    
    def test_damping_ratio_typical(self):
        """Test damping ratio for typical tree."""
        c = 10000
        k = 1e7
        m = 25000
        
        zeta = self.calc.calculate_damping_ratio(c, k, m)
        
        # Damping ratio should be >= 0.01
        self.assertGreaterEqual(zeta, 0.01)
        self.assertLess(zeta, 0.2)
    
    def test_infrasonic_cross_section(self):
        """Test infrasonic cross-section calculation."""
        D = 20.0
        Cd = 0.4
        
        sigma = self.calc.calculate_infrasonic_cross_section(D, Cd)
        
        self.assertAlmostEqual(sigma, 125.66, places=1)
    
    def test_sap_pressure(self):
        """Test sap pressure oscillation."""
        rho_sap = 1000
        h = 40
        a_peak = 0.5
        
        delta_p = self.calc.calculate_sap_pressure(rho_sap, h, a_peak)
        
        self.assertEqual(delta_p, 20000.0)
    
    def test_bending_stiffness(self):
        """Test bending stiffness calculation."""
        E = 13e9
        D = 1.2
        
        EI = self.calc.calculate_bending_stiffness(E, D)
        
        expected = E * (3.14159 * (1.2 ** 4) / 64)
        self.assertAlmostEqual(EI, expected, delta=1e6)
    
    def test_root_soil_impedance(self):
        """Test root-soil impedance calculation."""
        Z_root = 3.0
        Z_soil = 8.0
        
        Z_rs = self.calc.calculate_root_soil_impedance(Z_root, Z_soil)
        
        self.assertAlmostEqual(Z_rs, 4.90, places=1)
    
    def test_adi_seismic(self):
        """Test ADI for seismic signal."""
        P_seismic = 10.0
        P_wind = 1.0
        
        adi = self.calc.calculate_adi(P_seismic, P_wind)
        
        self.assertEqual(adi, 100.0)
    
    def test_adi_wind(self):
        """Test ADI for wind noise."""
        P_seismic = 1.0
        P_wind = 10.0
        
        adi = self.calc.calculate_adi(P_seismic, P_wind)
        
        self.assertEqual(adi, 0.01)
    
    def test_lead_time(self):
        """Test lead time calculation."""
        delta = 100
        Vp = 6.0
        Vs = 3.5
        
        tau = self.calc.calculate_lead_time(delta, Vp, Vs)
        
        self.assertAlmostEqual(tau, 11.9, places=1)
    
    def test_lead_time_near_field(self):
        """Test lead time for near-field earthquake."""
        delta = 20
        
        tau = self.calc.calculate_lead_time(delta)
        
        self.assertAlmostEqual(tau, 2.38, places=1)
    
    def test_edge_cases(self):
        """Test edge cases and invalid inputs."""
        self.assertEqual(self.calc.calculate_resonance_frequency(1, 1, 0, 1), 0.0)
        self.assertEqual(self.calc.calculate_coupling_coefficient(-1, 1), 0.0)
        self.assertEqual(self.calc.calculate_adi(10, 0), 0.0)
        self.assertEqual(self.calc.calculate_lead_time(100, 0, 3.5), 0.0)


if __name__ == '__main__':
    unittest.main()
