from fastapi import APIRouter, HTTPException
from typing import Optional
from ..models.risk_models import RiskInput, RiskOutput, BreakdownData
from ..scoring import ScoringEngine
from ..rules import RuleEngine
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize engines
scoring_engine = ScoringEngine()
rule_engine = RuleEngine()


@router.post("/calculate-risk", response_model=RiskOutput)
def calculate_risk(risk_input: RiskInput) -> RiskOutput:
    """
    Calculate risk score from structured input.
    
    This endpoint computes a risk score (0-100) using a weighted formula
    that combines severity, confidence, and frequency. It also evaluates
    security rules to provide explainability.
    
    Args:
        risk_input: RiskInput containing severity, confidence, frequency, and optional context
    
    Returns:
        RiskOutput with calculated risk score, risk level, and triggered rules
    
    Raises:
        HTTPException: If input validation fails
    """
    try:
        # Validate input
        severity = risk_input.severity
        confidence = risk_input.confidence
        frequency = risk_input.frequency
        context = risk_input.context or {}
        
        # Calculate risk score
        risk_score = scoring_engine.calculate_risk_score(severity, confidence, frequency)
        
        # Determine risk level
        risk_level = scoring_engine.get_risk_level(risk_score)
        
        # Evaluate rules for explainability
        triggered_rules = rule_engine.evaluate_rules(
            severity=severity,
            confidence=confidence,
            frequency=frequency,
            context=context,
        )
        
        # Create response
        response = RiskOutput(
            risk_score=round(risk_score, 2),
            risk_level=risk_level,
            breakdown=BreakdownData(
                severity=severity,
                confidence=confidence,
                frequency=frequency,
            ),
            triggered_rules=triggered_rules,
        )
        
        logger.info(f"Risk calculated: {risk_score:.2f} ({risk_level}), triggered {len(triggered_rules)} rules")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during risk calculation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "RiskRadar",
        "version": "1.0.0",
    }
