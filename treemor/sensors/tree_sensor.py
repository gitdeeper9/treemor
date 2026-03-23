"""
Tree Sensor Model - Individual tree instrumentation and monitoring.
Pure Python implementation - NO NUMPY
"""

import math
import json
from datetime import datetime
from typing import Dict, Optional, List, Tuple


class TreeSensor:
    """
    Individual tree sensor model.
    
    Each tree acts as a natural seismometer with specific biomechanical properties.
    """
    
    # Species database (E in GPa, density in kg/m³)
    SPECIES_DB = {
        "douglas_fir": {"E": 13.0, "density": 450, "typical_height": (40, 80)},
        "coast_live_oak": {"E": 11.0, "density": 750, "typical_height": (15, 25)},
        "japanese_cedar": {"E": 9.5, "density": 380, "typical_height": (20, 40)},
        "ponderosa_pine": {"E": 10.5, "density": 420, "typical_height": (30, 60)},
        "redwood": {"E": 12.5, "density": 410, "typical_height": (50, 100)},
        "maple": {"E": 12.0, "density": 620, "typical_height": (15, 30)},
        "oak": {"E": 11.5, "density": 720, "typical_height": (15, 35)},
    }
    
    def __init__(
        self,
        tree_id: str,
        species: str,
        height: float,
        dbh: float,
        latitude: float,
        longitude: float,
        soil_type: str = "bedrock",
        custom_E: Optional[float] = None,
        custom_density: Optional[float] = None
    ):
        """
        Initialize a tree sensor.
        
        Args:
            tree_id: Unique identifier
            species: Tree species (key in SPECIES_DB)
            height: Tree height in meters
            dbh: Diameter at breast height in meters
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            soil_type: Soil type (sediment, soil, bedrock)
            custom_E: Custom elastic modulus (GPa)
            custom_density: Custom density (kg/m³)
        """
        self.tree_id = tree_id
        self.species = species
        self.height = height
        self.dbh = dbh
        self.latitude = latitude
        self.longitude = longitude
        self.soil_type = soil_type
        
        # Get species properties
        species_data = self.SPECIES_DB.get(species, {"E": 10.0, "density": 500})
        self.elastic_modulus = (custom_E or species_data["E"]) * 1e9  # Pa
        self.density = custom_density or species_data["density"]  # kg/m³
        
        # Calculated properties
        self.mass = self._calculate_mass()
        self.I = self._calculate_moment_of_inertia()
        self.mass_per_length = self.mass / height
        
        # FSIN parameters (to be calculated)
        self.fsin_params = {}
        self.tssi = None
        
        # Installation metadata
        self.installed_at = datetime.now().isoformat()
        self.last_calibration = None
        self.status = "active"
    
    def _calculate_mass(self) -> float:
        """Calculate tree mass (kg)."""
        volume = math.pi * (self.dbh / 2) ** 2 * self.height
        mass = volume * self.density
        return round(mass, 2)
    
    def _calculate_moment_of_inertia(self) -> float:
        """Calculate second moment of area (m⁴)."""
        I = math.pi * (self.dbh ** 4) / 64
        return round(I, 8)
    
    def calculate_resonance_frequency(self) -> float:
        """
        Calculate fundamental resonance frequency f₀ (Hz).
        
        f₀ = (λ₁²/2π) √(EI/mL⁴)
        λ₁ = 1.875
        """
        lambda1 = 1.875
        EI = self.elastic_modulus * self.I
        denominator = self.mass_per_length * (self.height ** 4)
        
        if denominator <= 0:
            return 0.0
        
        sqrt_term = math.sqrt(EI / denominator)
        f0 = (lambda1 ** 2 / (2 * math.pi)) * sqrt_term
        
        return round(f0, 4)
    
    def calculate_coupling_coefficient(self) -> float:
        """
        Calculate seismic coupling coefficient ξ based on soil type.
        
        Impedance values:
        - Sediment: Z_soil = 0.5-1.0 MPa·s/m
        - Soil: Z_soil = 2.0-4.0 MPa·s/m
        - Bedrock: Z_soil = 6.0-10.0 MPa·s/m
        """
        # Root impedance (typical for mature trees)
        Z_root = 3.0  # MPa·s/m
        
        # Soil impedance based on type
        soil_impedance = {
            "sediment": 0.8,
            "soil": 3.0,
            "bedrock": 8.0
        }
        
        Z_soil = soil_impedance.get(self.soil_type, 3.0)
        
        if Z_root + Z_soil == 0:
            return 0.0
        
        numerator = 4 * Z_root * Z_soil
        denominator = (Z_root + Z_soil) ** 2
        
        xi = numerator / denominator
        return max(0.0, min(1.0, round(xi, 4)))
    
    def calculate_damping_ratio(self) -> float:
        """
        Calculate damping ratio ζ based on species.
        
        Living trees: ζ = 0.05-0.15
        """
        # Species-based damping (empirical)
        species_damping = {
            "douglas_fir": 0.08,
            "coast_live_oak": 0.12,
            "japanese_cedar": 0.10,
            "ponderosa_pine": 0.09,
            "redwood": 0.07,
            "maple": 0.13,
            "oak": 0.11
        }
        
        zeta = species_damping.get(self.species, 0.10)
        return round(zeta, 4)
    
    def calculate_bending_stiffness(self) -> float:
        """Calculate bending stiffness EI (N·m²)."""
        EI = self.elastic_modulus * self.I
        return round(EI, 2)
    
    def get_fsin_parameters(self) -> Dict[str, float]:
        """
        Calculate all FSIN parameters for this tree.
        
        Returns:
            Dictionary of 9 FSIN parameters
        """
        self.fsin_params = {
            'f0': self.calculate_resonance_frequency(),
            'xi': self.calculate_coupling_coefficient(),
            'zeta': self.calculate_damping_ratio(),
            'EI': self.calculate_bending_stiffness(),
            # Default values for parameters requiring dynamic input
            'sigma_inf': self._estimate_canopy_cross_section(),
            'delta_p_sap': self._estimate_sap_pressure(),
            'Z_RS': self._estimate_root_soil_impedance(),
            'ADI': 5.0,  # Default - good conditions
            'tau_lead': 10.0  # Default - typical for 100 km
        }
        
        return self.fsin_params
    
    def _estimate_canopy_cross_section(self) -> float:
        """Estimate infrasonic cross-section σ_inf (m²)."""
        # Canopy diameter roughly 0.5-0.7 of height
        canopy_diameter = self.height * 0.5
        Cd = 0.4
        sigma_inf = (math.pi * (canopy_diameter ** 2) * Cd) / 4
        return round(sigma_inf, 4)
    
    def _estimate_sap_pressure(self) -> float:
        """Estimate sap pressure oscillation ΔP_sap (kPa)."""
        rho_sap = 1000  # kg/m³
        a_peak = 0.5  # m/s² (typical for moderate earthquake)
        delta_p = (rho_sap * self.height * a_peak) / 1000  # Convert to kPa
        return round(delta_p, 2)
    
    def _estimate_root_soil_impedance(self) -> float:
        """Estimate root-soil impedance Z_RS (MPa·s/m)."""
        Z_root = 3.0
        soil_impedance = {"sediment": 0.8, "soil": 3.0, "bedrock": 8.0}
        Z_soil = soil_impedance.get(self.soil_type, 3.0)
        
        Z_rs = math.sqrt(Z_root * Z_soil)
        return round(Z_rs, 2)
    
    def to_dict(self) -> Dict:
        """Convert tree sensor to dictionary."""
        return {
            "tree_id": self.tree_id,
            "species": self.species,
            "height": self.height,
            "dbh": self.dbh,
            "location": {"lat": self.latitude, "lon": self.longitude},
            "soil_type": self.soil_type,
            "mass": self.mass,
            "elastic_modulus_gpa": self.elastic_modulus / 1e9,
            "fsin_parameters": self.get_fsin_parameters(),
            "installed_at": self.installed_at,
            "status": self.status
        }
    
    def to_json(self) -> str:
        """Convert tree sensor to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    def calibrate(self, measured_f0: Optional[float] = None, measured_xi: Optional[float] = None):
        """
        Calibrate tree sensor with field measurements.
        
        Args:
            measured_f0: Measured resonance frequency (Hz)
            measured_xi: Measured coupling coefficient
        """
        self.last_calibration = datetime.now().isoformat()
        
        if measured_f0 is not None:
            self.fsin_params['f0'] = measured_f0
        
        if measured_xi is not None:
            self.fsin_params['xi'] = measured_xi
    
    def health_check(self) -> Tuple[bool, str]:
        """
        Check sensor health.
        
        Returns:
            (is_healthy, status_message)
        """
        issues = []
        
        if self.status != "active":
            issues.append(f"Sensor status: {self.status}")
        
        if self.height <= 0:
            issues.append("Invalid height")
        
        if self.dbh <= 0:
            issues.append("Invalid diameter")
        
        if self.mass <= 0:
            issues.append("Invalid mass calculation")
        
        is_healthy = len(issues) == 0
        status_msg = "OK" if is_healthy else "; ".join(issues)
        
        return (is_healthy, status_msg)
