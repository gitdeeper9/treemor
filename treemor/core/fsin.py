"""
FSIN (Forest Seismic Intelligence Nonet) - Nine Parameters Calculator
Pure Python implementation - NO NUMPY
"""

import math
from typing import Dict, Any, Optional


class FSINCalculator:
    """
    Forest Seismic Intelligence Nonet - 9 parameters for bio-seismic sensing.
    
    Parameters:
        f0: Fundamental resonance frequency (Hz)
        xi: Seismic coupling coefficient (0-1)
        zeta: Damping ratio (0-1)
        sigma_inf: Infrasonic cross-section (m²)
        delta_p_sap: Sap pressure oscillation (Pa)
        EI: Bending stiffness (N·m²)
        Z_RS: Root-soil impedance (kg/(m²·s))
        ADI: Atmospheric decoupling index
        tau_lead: Bio-seismic lead time (seconds)
    """
    
    def __init__(self):
        self.parameters = {
            'f0': None,
            'xi': None,
            'zeta': None,
            'sigma_inf': None,
            'delta_p_sap': None,
            'EI': None,
            'Z_RS': None,
            'ADI': None,
            'tau_lead': None
        }
    
    def calculate_resonance_frequency(self, E: float, I: float, m: float, L: float) -> float:
        """
        Calculate fundamental resonance frequency f₀.
        
        Equation: f₀ = (λ₁²/2π) √(EI/mL⁴)
        λ₁ = 1.875 (first eigenvalue for cantilever beam)
        
        Args:
            E: Elastic modulus (Pa)
            I: Second moment of area (m⁴)
            m: Mass per unit length (kg/m)
            L: Tree height (m)
        
        Returns:
            f₀: Fundamental resonance frequency (Hz)
        """
        lambda1 = 1.875
        EI = E * I
        denominator = m * (L ** 4)
        
        if denominator <= 0:
            return 0.0
        
        sqrt_term = math.sqrt(EI / denominator)
        f0 = (lambda1 ** 2 / (2 * math.pi)) * sqrt_term
        
        return round(f0, 4)
    
    def calculate_coupling_coefficient(self, Z_root: float, Z_soil: float) -> float:
        """
        Calculate seismic coupling coefficient ξ.
        
        Equation: ξ = 4Z_root Z_soil / (Z_root + Z_soil)²
        
        Args:
            Z_root: Root acoustic impedance (kg/(m²·s))
            Z_soil: Soil acoustic impedance (kg/(m²·s))
        
        Returns:
            ξ: Coupling coefficient (0-1)
        """
        if Z_root + Z_soil == 0:
            return 0.0
        
        numerator = 4 * Z_root * Z_soil
        denominator = (Z_root + Z_soil) ** 2
        
        xi = numerator / denominator
        return max(0.0, min(1.0, round(xi, 4)))
    
    def calculate_damping_ratio(self, c: float, k: float, m: float) -> float:
        """
        Calculate damping ratio ζ.
        
        Equation: ζ = c / (2√(km))
        
        Args:
            c: Damping coefficient
            k: Effective stiffness
            m: Effective mass
        
        Returns:
            ζ: Damping ratio (0-1)
        """
        if k <= 0 or m <= 0:
            return 0.0
        
        critical_damping = 2 * math.sqrt(k * m)
        if critical_damping == 0:
            return 0.0
        
        zeta = c / critical_damping
        return max(0.0, min(1.0, round(zeta, 4)))
    
    def calculate_infrasonic_cross_section(self, D: float, Cd: float = 0.4) -> float:
        """
        Calculate infrasonic cross-section σ_inf.
        
        Equation: σ_inf = π D² C_d / 4
        
        Args:
            D: Canopy diameter (m)
            Cd: Drag coefficient (typically 0.3-0.5)
        
        Returns:
            σ_inf: Infrasonic cross-section (m²)
        """
        sigma_inf = (math.pi * (D ** 2) * Cd) / 4
        return round(sigma_inf, 4)
    
    def calculate_sap_pressure(self, rho_sap: float, h: float, a_peak: float) -> float:
        """
        Calculate sap pressure oscillation ΔP_sap.
        
        Equation: ΔP_sap = ρ_sap * h * a_peak
        
        Args:
            rho_sap: Sap density (kg/m³, typically ~1000)
            h: Xylem column height (m)
            a_peak: Peak acceleration (m/s²)
        
        Returns:
            ΔP_sap: Sap pressure oscillation (Pa)
        """
        delta_p = rho_sap * h * a_peak
        return round(delta_p, 2)
    
    def calculate_bending_stiffness(self, E: float, D: float) -> float:
        """
        Calculate bending stiffness EI.
        
        Equation: EI = E * (πD⁴/64)
        
        Args:
            E: Elastic modulus (Pa)
            D: Trunk diameter (m)
        
        Returns:
            EI: Bending stiffness (N·m²)
        """
        I = math.pi * (D ** 4) / 64
        EI = E * I
        return round(EI, 2)
    
    def calculate_root_soil_impedance(self, Z_root: float, Z_soil: float) -> float:
        """
        Calculate root-soil impedance Z_RS.
        
        Equation: Z_RS = √(Z_root * Z_soil)
        
        Args:
            Z_root: Root acoustic impedance (kg/(m²·s))
            Z_soil: Soil acoustic impedance (kg/(m²·s))
        
        Returns:
            Z_RS: Root-soil impedance (kg/(m²·s))
        """
        if Z_root <= 0 or Z_soil <= 0:
            return 0.0
        
        Z_rs = math.sqrt(Z_root * Z_soil)
        return round(Z_rs, 2)
    
    def calculate_adi(self, P_seismic: float, P_wind: float) -> float:
        """
        Calculate Atmospheric Decoupling Index ADI.
        
        Equation: ADI = (P_seismic / P_wind)²
        
        Args:
            P_seismic: Power in seismic band (0.5-5 Hz)
            P_wind: Power in wind band (0.05-0.3 Hz)
        
        Returns:
            ADI: Atmospheric decoupling index
        """
        if P_wind <= 0:
            return 0.0
        
        adi = (P_seismic / P_wind) ** 2
        return round(adi, 4)
    
    def calculate_lead_time(self, delta: float, Vp: float = 6.0, Vs: float = 3.5) -> float:
        """
        Calculate bio-seismic lead time τ_lead.
        
        Equation: τ_lead = Δ/V_s - Δ/V_p
        
        Args:
            delta: Epicentral distance (km)
            Vp: P-wave velocity (km/s, default 6.0)
            Vs: S-wave velocity (km/s, default 3.5)
        
        Returns:
            τ_lead: Lead time (seconds)
        """
        if Vp <= 0 or Vs <= 0:
            return 0.0
        
        tau = (delta / Vs) - (delta / Vp)
        return round(tau, 2)
    
    def get_all_parameters(self) -> Dict[str, float]:
        """Return all calculated parameters."""
        return {k: v for k, v in self.parameters.items() if v is not None}
    
    def reset(self):
        """Reset all parameters to None."""
        for key in self.parameters:
            self.parameters[key] = None
