import pytest
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.scoring import ScoringEngine
from app.models.risk_models import ContextData


class TestScoringEngine:
    """Test suite for the ScoringEngine."""
    
    @pytest.fixture
    def engine(self):
        """Create a fresh scoring engine instance."""
        return ScoringEngine()
    
    def test_basic_calculation(self, engine):
        """Test basic risk score calculation."""
        # Equal weights: (0.35 * 80 + 0.35 * 75 + 0.30 * 90) / 100 * 100
        risk_score = engine.calculate_risk_score(80, 75, 90)
        assert 0 <= risk_score <= 100
        assert abs(risk_score - 81.25) < 0.1  # Expected: ~81.25
    
    def test_zero_scores(self, engine):
        """Test with zero scores."""
        risk_score = engine.calculate_risk_score(0, 0, 0)
        assert risk_score == 0
    
    def test_max_scores(self, engine):
        """Test with maximum scores."""
        risk_score = engine.calculate_risk_score(100, 100, 100)
        assert risk_score == 100
    
    def test_clamp_above_100(self, engine):
        """Test that values above 100 are clamped."""
        risk_score = engine.calculate_risk_score(150, 120, 110)
        assert 0 <= risk_score <= 100
    
    def test_clamp_below_0(self, engine):
        """Test that negative values are clamped to 0."""
        risk_score = engine.calculate_risk_score(-10, -20, -50)
        assert risk_score == 0
    
    def test_risk_level_low(self, engine):
        """Test LOW risk level (0-30)."""
        level = engine.get_risk_level(15)
        assert level == "LOW"
    
    def test_risk_level_medium(self, engine):
        """Test MEDIUM risk level (31-60)."""
        level = engine.get_risk_level(45)
        assert level == "MEDIUM"
    
    def test_risk_level_high(self, engine):
        """Test HIGH risk level (61-80)."""
        level = engine.get_risk_level(75)
        assert level == "HIGH"
    
    def test_risk_level_critical(self, engine):
        """Test CRITICAL risk level (81-100)."""
        level = engine.get_risk_level(90)
        assert level == "CRITICAL"
    
    def test_risk_level_boundaries(self, engine):
        """Test risk level boundaries."""
        assert engine.get_risk_level(0) == "LOW"
        assert engine.get_risk_level(30) == "LOW"
        assert engine.get_risk_level(31) == "MEDIUM"
        assert engine.get_risk_level(60) == "MEDIUM"
        assert engine.get_risk_level(61) == "HIGH"
        assert engine.get_risk_level(80) == "HIGH"
        assert engine.get_risk_level(81) == "CRITICAL"
        assert engine.get_risk_level(100) == "CRITICAL"
    
    def test_weighted_calculation(self, engine):
        """Test that weights are properly applied."""
        # Severity should have 0.35 weight, same as confidence
        # Frequency has 0.30 weight
        score1 = engine.calculate_risk_score(100, 0, 0)  # Only severity
        score2 = engine.calculate_risk_score(0, 100, 0)  # Only confidence
        score3 = engine.calculate_risk_score(0, 0, 100)  # Only frequency
        
        # severity and confidence should be equal
        assert abs(score1 - score2) < 0.1
        # Frequency should be slightly less due to lower weight
        assert score3 < score1
    
    def test_deterministic_output(self, engine):
        """Test that the same input produces the same output."""
        score1 = engine.calculate_risk_score(75.5, 82.3, 91.2)
        score2 = engine.calculate_risk_score(75.5, 82.3, 91.2)
        assert score1 == score2
    
    def test_floating_point_precision(self, engine):
        """Test floating point calculation accuracy."""
        score = engine.calculate_risk_score(50, 50, 50)
        assert 49 < score < 51  # Should be very close to 50
