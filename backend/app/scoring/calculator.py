import yaml
from pathlib import Path
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class ScoringEngine:
    """
    Risk scoring engine that calculates a deterministic risk score (0-100)
    using weighted combination of severity, confidence, and frequency.
    
    Formula: risk_score = (severity * w_severity) + (confidence * w_confidence) + (frequency * w_frequency)
    """
    
    def __init__(self, config_path: Path = None):
        """
        Initialize the scoring engine with configuration.
        
        Args:
            config_path: Path to scoring_weights.yaml. Defaults to backend/config/scoring_weights.yaml
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "scoring_weights.yaml"
        
        self.config_path = config_path
        self.config = self._load_config()
        self.weights = self.config.get("weights", {})
        self.risk_levels = self.config.get("risk_levels", {})
        
        # Validate weights sum to 1.0
        weights_sum = sum(self.weights.values())
        if abs(weights_sum - 1.0) > 0.001:  # Allow small floating point errors
            logger.warning(f"Weights sum to {weights_sum}, not 1.0. Normalizing.")
            self._normalize_weights()
    
    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        with open(self.config_path, "r") as f:
            return yaml.safe_load(f)
    
    def _normalize_weights(self) -> None:
        """Normalize weights to sum to 1.0."""
        total = sum(self.weights.values())
        for key in self.weights:
            self.weights[key] = self.weights[key] / total
    
    def calculate_risk_score(self, severity: float, confidence: float, frequency: float) -> float:
        """
        Calculate the risk score using the weighted formula.
        
        Formula:
            risk_score = (severity * w_severity) + (confidence * w_confidence) + (frequency * w_frequency)
        
        Args:
            severity: Severity score (0-100)
            confidence: Confidence score (0-100)
            frequency: Frequency score (0-100)
        
        Returns:
            Risk score (0-100)
        """
        # Clamp inputs to 0-100 range
        severity = max(0, min(100, severity))
        confidence = max(0, min(100, confidence))
        frequency = max(0, min(100, frequency))
        
        # Calculate weighted sum
        risk_score = (
            (severity / 100.0) * self.weights["severity"] * 100 +
            (confidence / 100.0) * self.weights["confidence"] * 100 +
            (frequency / 100.0) * self.weights["frequency"] * 100
        )
        
        # Clamp result to 0-100
        return max(0, min(100, risk_score))
    
    def get_risk_level(self, risk_score: float) -> str:
        """
        Determine risk level based on score.
        
        Args:
            risk_score: Risk score (0-100)
        
        Returns:
            Risk level string (LOW, MEDIUM, HIGH, CRITICAL)
        """
        for level, bounds in self.risk_levels.items():
            if bounds["min"] <= risk_score <= bounds["max"]:
                return level.upper()
        return "CRITICAL"
