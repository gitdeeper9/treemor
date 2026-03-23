"""
TSSI (Tree Seismic Sensitivity Index) - Composite Metric
Combines all 9 FSIN parameters into a single sensitivity score.
Pure Python implementation - NO NUMPY
"""

from typing import Dict, List, Tuple


class TSSICalculator:
    """
    Tree Seismic Sensitivity Index Calculator.
    
    TSSI = Σ w_i * FSIN_i*
    where FSIN_i* are normalized (0-1) parameter values.
    """
    
    # Default weights derived from validation (847 events)
    DEFAULT_WEIGHTS = {
        'f0': 0.21,          # Resonance frequency
        'xi': 0.19,          # Seismic coupling
        'EI': 0.16,          # Bending stiffness
        'Z_RS': 0.14,        # Root-soil impedance
        'ADI': 0.12,         # Atmospheric decoupling
        'zeta': 0.08,        # Damping ratio
        'sigma_inf': 0.05,   # Infrasonic cross-section
        'delta_p_sap': 0.03, # Sap pressure
        'tau_lead': 0.02     # Lead time
    }
    
    # Typical ranges for normalization (min, max)
    PARAMETER_RANGES = {
        'f0': (0.3, 2.5),           # Hz
        'xi': (0.0, 1.0),           # dimensionless
        'zeta': (0.0, 0.2),         # dimensionless
        'sigma_inf': (0, 100),      # m²
        'delta_p_sap': (0, 1000),   # kPa
        'EI': (1e8, 1e11),          # N·m²
        'Z_RS': (0.5, 10.0),        # MPa·s/m
        'ADI': (0, 100),            # dimensionless
        'tau_lead': (0, 30)         # seconds
    }
    
    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize TSSI calculator.
        
        Args:
            weights: Custom weights for each parameter (optional)
        """
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()
    
    def normalize(self, param_name: str, value: float) -> float:
        """
        Normalize parameter to 0-1 scale.
        
        Args:
            param_name: Parameter name
            value: Raw parameter value
        
        Returns:
            Normalized value (0-1)
        """
        if param_name not in self.PARAMETER_RANGES:
            return 0.0
        
        min_val, max_val = self.PARAMETER_RANGES[param_name]
        
        if max_val <= min_val:
            return 0.0
        
        # Clamp value to range
        clamped = max(min_val, min(max_val, value))
        
        # Normalize
        normalized = (clamped - min_val) / (max_val - min_val)
        
        return round(normalized, 4)
    
    def calculate_tssi(self, parameters: Dict[str, float]) -> float:
        """
        Calculate TSSI from FSIN parameters.
        
        Args:
            parameters: Dictionary of FSIN parameter values
        
        Returns:
            TSSI score (0-1)
        """
        if not parameters:
            return 0.0
        
        total_weight = 0.0
        weighted_sum = 0.0
        
        for param_name, value in parameters.items():
            if param_name in self.weights:
                weight = self.weights[param_name]
                normalized = self.normalize(param_name, value)
                weighted_sum += weight * normalized
                total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        tssi = weighted_sum / total_weight
        return round(tssi, 4)
    
    def classify_sensitivity(self, tssi: float) -> Tuple[str, str]:
        """
        Classify sensor sensitivity based on TSSI score.
        
        Args:
            tssi: TSSI score (0-1)
        
        Returns:
            (category, description)
        """
        if tssi >= 0.8:
            return ("EXCEPTIONAL", "Bedrock anchoring, optimal resonance")
        elif tssi >= 0.6:
            return ("GOOD", "Competent soil, favorable geometry")
        elif tssi >= 0.3:
            return ("MODERATE", "Mixed conditions, acceptable performance")
        else:
            return ("POOR", "Soft soil, low coupling, high wind exposure")
    
    def get_improvement_recommendations(self, parameters: Dict[str, float]) -> List[str]:
        """
        Get recommendations to improve TSSI.
        
        Args:
            parameters: Dictionary of FSIN parameter values
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        for param_name, value in parameters.items():
            if param_name == 'xi' and value < 0.6:
                recommendations.append(
                    "Improve seismic coupling: Consider trees rooted in bedrock or compacted soil"
                )
            elif param_name == 'f0':
                if value < 0.3:
                    recommendations.append(
                        "Low resonance frequency: Tree may be too tall, consider shorter trees"
                    )
                elif value > 2.5:
                    recommendations.append(
                        "High resonance frequency: Tree may be too short, consider taller trees"
                    )
            elif param_name == 'ADI' and value < 2.0:
                recommendations.append(
                    "High wind noise: Install wind shields or relocate to sheltered area"
                )
            elif param_name == 'Z_RS' and value < 2.0:
                recommendations.append(
                    "Poor root-soil coupling: Consider soil compaction or different tree species"
                )
        
        return recommendations
    
    def compare_sites(self, sites_data: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Compare multiple sites by TSSI.
        
        Args:
            sites_data: {site_name: {parameter: value}}
        
        Returns:
            {site_name: tssi_score}
        """
        results = {}
        for site_name, parameters in sites_data.items():
            results[site_name] = self.calculate_tssi(parameters)
        
        # Sort by TSSI descending
        return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
