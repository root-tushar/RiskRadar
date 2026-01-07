from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List


class ContextData(BaseModel):
    """Optional context about the event being scored."""
    model_config = ConfigDict(json_schema_extra={})
    
    failed_logins: Optional[int] = Field(0, ge=0, description="Number of failed login attempts")
    is_privileged: Optional[bool] = Field(False, description="Whether the account is privileged")
    user_id: Optional[str] = Field(None, description="User identifier")
    source_ip: Optional[str] = Field(None, description="Source IP address")
    event_count: Optional[int] = Field(0, ge=0, description="Total event count")


class RiskInput(BaseModel):
    """Input model for risk calculation."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "severity": 80,
                "confidence": 75,
                "frequency": 90,
                "context": {
                    "failed_logins": 6,
                    "is_privileged": True
                }
            }
        }
    )
    
    severity: float = Field(..., ge=0, le=100, description="Severity score (0-100)")
    confidence: float = Field(..., ge=0, le=100, description="Confidence score (0-100)")
    frequency: float = Field(..., ge=0, le=100, description="Frequency score (0-100)")
    context: Optional[ContextData] = Field(default_factory=ContextData, description="Optional context data")

    @field_validator("severity", "confidence", "frequency", mode="before")
    @classmethod
    def validate_scores(cls, v):
        if v is None:
            raise ValueError("Score cannot be None")
        return float(v)

class BreakdownData(BaseModel):
    """Detailed breakdown of the risk score components."""
    model_config = ConfigDict(json_schema_extra={})
    
    severity: float = Field(..., description="Severity component")
    confidence: float = Field(..., description="Confidence component")
    frequency: float = Field(..., description="Frequency component")


class RiskOutput(BaseModel):
    """Output model for risk calculation."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "risk_score": 82,
                "risk_level": "CRITICAL",
                "breakdown": {
                    "severity": 80,
                    "confidence": 75,
                    "frequency": 90
                },
                "triggered_rules": [
                    "Multiple failed login attempts",
                    "Privileged account activity detected"
                ]
            }
        }
    )
    
    risk_score: float = Field(..., ge=0, le=100, description="Calculated risk score (0-100)")
    risk_level: str = Field(..., description="Risk level (LOW, MEDIUM, HIGH, CRITICAL)")
    breakdown: BreakdownData = Field(..., description="Component breakdown")
    triggered_rules: List[str] = Field(default_factory=list, description="List of triggered rules")


class RuleResult(BaseModel):
    """Result of a single rule evaluation."""
    rule_name: str = Field(..., description="Name of the rule")
    triggered: bool = Field(..., description="Whether the rule was triggered")
    description: Optional[str] = Field(None, description="Description of the rule")
