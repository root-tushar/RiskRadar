import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test suite for FastAPI endpoints."""
    
    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "RiskRadar"
        assert data["version"] == "1.0.0"
        assert "endpoints" in data
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "RiskRadar"
    
    def test_calculate_risk_basic(self):
        """Test basic risk calculation endpoint."""
        payload = {
            "severity": 80,
            "confidence": 75,
            "frequency": 90,
        }
        response = client.post("/calculate-risk", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "risk_score" in data
        assert "risk_level" in data
        assert "breakdown" in data
        assert "triggered_rules" in data
        assert 0 <= data["risk_score"] <= 100
        assert data["risk_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    
    def test_calculate_risk_with_context(self):
        """Test risk calculation with context data."""
        payload = {
            "severity": 80,
            "confidence": 75,
            "frequency": 90,
            "context": {
                "failed_logins": 6,
                "is_privileged": True,
            },
        }
        response = client.post("/calculate-risk", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert len(data["triggered_rules"]) > 0
        assert "Multiple failed login attempts" in data["triggered_rules"]
    
    def test_calculate_risk_zero_values(self):
        """Test with all zero values."""
        payload = {
            "severity": 0,
            "confidence": 0,
            "frequency": 0,
        }
        response = client.post("/calculate-risk", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["risk_score"] == 0
        assert data["risk_level"] == "LOW"
    
    def test_calculate_risk_max_values(self):
        """Test with maximum values."""
        payload = {
            "severity": 100,
            "confidence": 100,
            "frequency": 100,
        }
        response = client.post("/calculate-risk", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["risk_score"] == 100
        assert data["risk_level"] == "CRITICAL"
    
    def test_calculate_risk_breakdown(self):
        """Test that breakdown contains correct component values."""
        payload = {
            "severity": 60,
            "confidence": 70,
            "frequency": 80,
        }
        response = client.post("/calculate-risk", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["breakdown"]["severity"] == 60
        assert data["breakdown"]["confidence"] == 70
        assert data["breakdown"]["frequency"] == 80
    
    def test_calculate_risk_missing_field(self):
        """Test validation error with missing required field."""
        payload = {
            "severity": 80,
            "confidence": 75,
            # missing frequency
        }
        response = client.post("/calculate-risk", json=payload)
        assert response.status_code == 422
    
    def test_calculate_risk_invalid_type(self):
        """Test validation error with invalid data type."""
        payload = {
            "severity": "invalid",
            "confidence": 75,
            "frequency": 90,
        }
        response = client.post("/calculate-risk", json=payload)
        assert response.status_code == 422
    
    def test_calculate_risk_out_of_range_high(self):
        """Test validation error with value above 100."""
        payload = {
            "severity": 150,
            "confidence": 75,
            "frequency": 90,
        }
        response = client.post("/calculate-risk", json=payload)
        assert response.status_code == 422
    
    def test_calculate_risk_out_of_range_low(self):
        """Test validation error with negative value."""
        payload = {
            "severity": -10,
            "confidence": 75,
            "frequency": 90,
        }
        response = client.post("/calculate-risk", json=payload)
        assert response.status_code == 422
    
    def test_calculate_risk_deterministic(self):
        """Test that same input produces same output."""
        payload = {
            "severity": 75.5,
            "confidence": 82.3,
            "frequency": 91.2,
        }
        response1 = client.post("/calculate-risk", json=payload)
        response2 = client.post("/calculate-risk", json=payload)
        assert response1.json()["risk_score"] == response2.json()["risk_score"]
    
    def test_calculate_risk_response_structure(self):
        """Test that response has correct structure."""
        payload = {
            "severity": 50,
            "confidence": 50,
            "frequency": 50,
        }
        response = client.post("/calculate-risk", json=payload)
        data = response.json()
        
        # Check all required fields
        assert "risk_score" in data
        assert "risk_level" in data
        assert "breakdown" in data
        assert "triggered_rules" in data
        
        # Check breakdown structure
        assert "severity" in data["breakdown"]
        assert "confidence" in data["breakdown"]
        assert "frequency" in data["breakdown"]
        
        # Check types
        assert isinstance(data["risk_score"], (int, float))
        assert isinstance(data["risk_level"], str)
        assert isinstance(data["breakdown"], dict)
        assert isinstance(data["triggered_rules"], list)
    
    def test_calculate_risk_edge_case_float_precision(self):
        """Test edge case with float precision."""
        payload = {
            "severity": 33.333333,
            "confidence": 33.333333,
            "frequency": 33.333333,
        }
        response = client.post("/calculate-risk", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert 0 <= data["risk_score"] <= 100
