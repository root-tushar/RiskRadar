import pytest
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.rules import RuleEngine
from app.models.risk_models import ContextData


class TestRuleEngine:
    """Test suite for the RuleEngine."""
    
    @pytest.fixture
    def engine(self):
        """Create a fresh rule engine instance."""
        return RuleEngine()
    
    def test_failed_logins_rule(self, engine):
        """Test multiple failed login attempts rule."""
        context = ContextData(failed_logins=6)
        rules = engine.evaluate_rules(50, 50, 50, context)
        assert "Multiple failed login attempts" in rules
    
    def test_failed_logins_threshold(self, engine):
        """Test that rule doesn't trigger at threshold boundary."""
        context = ContextData(failed_logins=5)
        rules = engine.evaluate_rules(50, 50, 50, context)
        assert "Multiple failed login attempts" not in rules
        
        context = ContextData(failed_logins=6)
        rules = engine.evaluate_rules(50, 50, 50, context)
        assert "Multiple failed login attempts" in rules
    
    def test_high_severity_rule(self, engine):
        """Test high-severity event rule."""
        rules = engine.evaluate_rules(80, 50, 50, ContextData())
        assert "High-severity event detected" in rules
    
    def test_high_severity_boundary(self, engine):
        """Test high-severity rule boundary."""
        rules = engine.evaluate_rules(79, 50, 50, ContextData())
        assert "High-severity event detected" not in rules
        
        rules = engine.evaluate_rules(80, 50, 50, ContextData())
        assert "High-severity event detected" in rules
    
    def test_privileged_account_rule(self, engine):
        """Test privileged account activity rule."""
        context = ContextData(is_privileged=True)
        rules = engine.evaluate_rules(50, 50, 50, context)
        assert "Privileged account activity detected" in rules
    
    def test_privileged_account_false(self, engine):
        """Test that rule doesn't trigger for non-privileged accounts."""
        context = ContextData(is_privileged=False)
        rules = engine.evaluate_rules(50, 50, 50, context)
        assert "Privileged account activity detected" not in rules
    
    def test_high_frequency_rule(self, engine):
        """Test high event frequency rule."""
        rules = engine.evaluate_rules(50, 50, 86, ContextData())
        assert "High event frequency detected" in rules
    
    def test_high_frequency_boundary(self, engine):
        """Test high frequency rule boundary."""
        rules = engine.evaluate_rules(50, 50, 85, ContextData())
        assert "High event frequency detected" not in rules
        
        rules = engine.evaluate_rules(50, 50, 85.1, ContextData())
        assert "High event frequency detected" in rules
    
    def test_confidence_severity_mismatch_rule(self, engine):
        """Test low confidence with high severity rule."""
        rules = engine.evaluate_rules(75, 40, 50, ContextData())
        assert "Low confidence with high severity" in rules
    
    def test_confidence_severity_boundaries(self, engine):
        """Test confidence-severity mismatch rule boundaries."""
        # Severity too low
        rules = engine.evaluate_rules(74, 40, 50, ContextData())
        assert "Low confidence with high severity" not in rules
        
        # Confidence too high
        rules = engine.evaluate_rules(75, 41, 50, ContextData())
        assert "Low confidence with high severity" not in rules
        
        # Both conditions met
        rules = engine.evaluate_rules(75, 40, 50, ContextData())
        assert "Low confidence with high severity" in rules
    
    def test_multiple_rules_triggered(self, engine):
        """Test that multiple rules can be triggered simultaneously."""
        context = ContextData(
            failed_logins=6,
            is_privileged=True,
        )
        rules = engine.evaluate_rules(80, 50, 90, context)
        assert "Multiple failed login attempts" in rules
        assert "High-severity event detected" in rules
        assert "Privileged account activity detected" in rules
        assert "High event frequency detected" in rules
        assert len(rules) >= 4
    
    def test_no_rules_triggered(self, engine):
        """Test scenario where no rules are triggered."""
        context = ContextData(
            failed_logins=2,
            is_privileged=False,
        )
        rules = engine.evaluate_rules(50, 60, 70, context)
        assert len(rules) == 0
    
    def test_context_default_values(self, engine):
        """Test that default context values work correctly."""
        rules = engine.evaluate_rules(50, 50, 50)  # No context provided
        assert isinstance(rules, list)
        assert len(rules) == 0
    
    def test_all_rules_exist(self, engine):
        """Test that all expected rules are defined."""
        assert len(engine.rules) >= 5
        rule_names = [r["name"] for r in engine.rules]
        assert "Multiple failed login attempts" in rule_names
        assert "High-severity event detected" in rule_names
        assert "Privileged account activity detected" in rule_names
        assert "High event frequency detected" in rule_names
        assert "Low confidence with high severity" in rule_names
