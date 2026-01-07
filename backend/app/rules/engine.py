from typing import List, Optional
from ..models.risk_models import ContextData, RuleResult
import logging

logger = logging.getLogger(__name__)


class RuleEngine:
    """
    Explainability layer that detects security patterns and reports triggered rules.
    
    Rules implemented:
    - Multiple failed login attempts (>5)
    - High-severity events (severity >= 80)
    - Privileged account activity
    - High event frequency (frequency > 85)
    - Low confidence with high severity (suspicious pattern)
    """
    
    def __init__(self):
        """Initialize the rule engine."""
        self.rules = [
            {
                "name": "Multiple failed login attempts",
                "description": "More than 5 failed login attempts detected",
                "check": self._check_failed_logins,
            },
            {
                "name": "High-severity event detected",
                "description": "Event severity score >= 80",
                "check": self._check_high_severity,
            },
            {
                "name": "Privileged account activity detected",
                "description": "Activity from a privileged account",
                "check": self._check_privileged_account,
            },
            {
                "name": "High event frequency detected",
                "description": "Event frequency score > 85",
                "check": self._check_high_frequency,
            },
            {
                "name": "Low confidence with high severity",
                "description": "Suspicious pattern: high severity but low confidence",
                "check": self._check_confidence_severity_mismatch,
            },
        ]
    
    def evaluate_rules(
        self,
        severity: float,
        confidence: float,
        frequency: float,
        context: Optional[ContextData] = None,
    ) -> List[str]:
        """
        Evaluate all rules against the given inputs.
        
        Args:
            severity: Severity score (0-100)
            confidence: Confidence score (0-100)
            frequency: Frequency score (0-100)
            context: Optional context data
        
        Returns:
            List of triggered rule names
        """
        if context is None:
            context = ContextData()
        
        triggered = []
        for rule in self.rules:
            if rule["check"](severity, confidence, frequency, context):
                triggered.append(rule["name"])
                logger.debug(f"Rule triggered: {rule['name']}")
        
        return triggered
    
    @staticmethod
    def _check_failed_logins(
        severity: float,
        confidence: float,
        frequency: float,
        context: ContextData,
    ) -> bool:
        """Check if there are multiple failed login attempts (>5)."""
        return context.failed_logins > 5
    
    @staticmethod
    def _check_high_severity(
        severity: float,
        confidence: float,
        frequency: float,
        context: ContextData,
    ) -> bool:
        """Check if severity is high (>= 80)."""
        return severity >= 80
    
    @staticmethod
    def _check_privileged_account(
        severity: float,
        confidence: float,
        frequency: float,
        context: ContextData,
    ) -> bool:
        """Check if activity involves a privileged account."""
        return context.is_privileged is True
    
    @staticmethod
    def _check_high_frequency(
        severity: float,
        confidence: float,
        frequency: float,
        context: ContextData,
    ) -> bool:
        """Check if event frequency is high (> 85)."""
        return frequency > 85
    
    @staticmethod
    def _check_confidence_severity_mismatch(
        severity: float,
        confidence: float,
        frequency: float,
        context: ContextData,
    ) -> bool:
        """Check for suspicious pattern: high severity but low confidence."""
        return severity >= 75 and confidence <= 40
