# 🤝 Contributing to RiskRadar

First of all, **thank you for considering contributing to RiskRadar** ❤️

RiskRadar is an open-source, community-driven project dedicated to making security risk scoring transparent, explainable, and accessible to everyone. Your contributions make it better for the entire security community.

---

## 📋 Table of Contents

- [🎯 Project Philosophy](#-project-philosophy)
- [🛠 How You Can Contribute](#-how-you-can-contribute)
- [🚀 Getting Started](#-getting-started)
- [📝 Development Workflow](#-development-workflow)
- [💻 Code Standards](#-code-standards)
- [🧪 Testing Guidelines](#-testing-guidelines)
- [📚 Documentation](#-documentation)
- [🔀 Creating Pull Requests](#-creating-pull-requests)
- [🐛 Reporting Bugs](#-reporting-bugs)
- [💡 Proposing Features](#-proposing-features)
- [📖 Commit Message Guidelines](#-commit-message-guidelines)
- [❓ Questions & Support](#-questions--support)

---

## 🎯 Project Philosophy

RiskRadar is built on these core principles. **Please keep them in mind when contributing:**

| Principle | Meaning | Example |
|-----------|---------|---------|
| 🔍 **Explainability First** | Every calculation must be understandable to humans | Use linear formulas, not neural networks |
| ⚡ **Deterministic** | Same input always produces same output | No randomization, no learning |
| 🎚️ **Customizable** | Analysts can tune the engine without coding | YAML config for weights, custom rules |
| 🔓 **Open & Transparent** | No vendor lock-in, no proprietary logic | MIT licensed, all source visible |
| 🛡️ **Security-First** | Designed for SOC/IR teams, not attackers | Fail-safe defaults, audit trails |

---

## 🛠 How You Can Contribute

### 🎯 Priority Contribution Areas

| Contribution Type | Impact | Difficulty | Time |
|-------------------|--------|-----------|------|
| 🐛 **Bug Reports** | High | Low | 5 min |
| 📖 **Documentation** | High | Low | 15-30 min |
| ✅ **Tests** | High | Medium | 30-60 min |
| 📏 **Code Quality** | Medium | Medium | 30-90 min |
| 🆕 **Features** | Medium-High | Medium-High | 1-4 hours |
| 🔌 **Integrations** | High | High | 2-8 hours |

### 🌟 You Can Help By:

#### 🐛 **Reporting Bugs**
- Found a crash? Unexpected behavior? Please report it!
- [Open a Bug Report](https://github.com/yourusername/RiskRadar/issues/new?template=bug_report.md)

#### 💡 **Proposing Features**
- Got an idea for a new rule? Scoring metric? Integration?
- [Suggest a Feature](https://github.com/yourusername/RiskRadar/issues/new?template=feature_request.md)

#### 📖 **Writing Documentation**
- Typos in README? Need better examples? Improve clarity?
- Documentation is just as important as code!

#### 🧪 **Adding Tests**
- Improve test coverage
- Add edge case tests
- Write integration tests

#### 💻 **Improving Code Quality**
- Refactor existing code
- Improve performance
- Add type hints
- Fix linting issues

#### ✨ **Adding New Features**
- New scoring rules
- Enhanced explainability
- Better error handling
- New API endpoints

#### 🔌 **Creating Integrations**
- SIEM connectors (Splunk, ELK, Wazuh)
- Incident management (PagerDuty, Opsgenie, Jira)
- Data formats (CSV, Parquet, Protocol Buffers)
- Webhooks and alerts

---

## 🚀 Getting Started

### Step 1: Fork the Repository 🍴

```bash
# Go to https://github.com/yourusername/RiskRadar
# Click "Fork" button in top-right corner
# This creates YOUR copy of the repository
```

### Step 2: Clone Your Fork

```bash
git clone https://github.com/YOUR-USERNAME/RiskRadar.git
cd RiskRadar
git remote add upstream https://github.com/yourusername/RiskRadar.git
```

### Step 3: Create Virtual Environment 🐍

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Development Dependencies

```bash
pip install -r requirements.txt
pip install -e .  # Install RiskRadar in editable mode
```

### Step 5: Create a Feature Branch

```bash
git checkout -b feature/my-awesome-feature
# OR
git checkout -b fix/bug-description
# OR
git checkout -b docs/improve-readme
```

**Branch Naming Conventions:**
- `feature/` — New features
- `fix/` — Bug fixes
- `docs/` — Documentation updates
- `test/` — Test additions
- `refactor/` — Code quality improvements
- `perf/` — Performance improvements

---

## 📝 Development Workflow

### 📂 Project Structure

```
RiskRadar/
├── backend/
│   ├── app/
│   │   ├── api/          # HTTP endpoints
│   │   ├── models/       # Pydantic data models
│   │   ├── scoring/      # Scoring formula
│   │   └── rules/        # Rule engine
│   ├── config/           # Configuration files
│   ├── tests/            # Test suite
│   └── main.py           # FastAPI app
├── docs/                 # Documentation
├── frontend/             # Optional web UI
└── samples/              # Example inputs/outputs
```

### 🔄 Development Cycle

**1️⃣ Make Your Changes**
```bash
# Edit files, add new features, fix bugs
nano backend/app/scoring/calculator.py
```

**2️⃣ Run Tests Locally**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend

# Run specific test file
pytest backend/tests/test_scoring.py -v

# Run with output
pytest -v -s
```

**3️⃣ Check Code Quality**
```bash
# Format code (if you have black installed)
black backend/

# Check style
python -m pylint backend/ --disable=all --enable=E,F

# Type checking (if you have mypy)
mypy backend/
```

**4️⃣ Commit Your Changes**
```bash
git add backend/
git commit -m "feat: add new risk rule for privilege escalation"
```

**5️⃣ Push to Your Fork**
```bash
git push origin feature/my-awesome-feature
```

**6️⃣ Create a Pull Request**
- Go to https://github.com/yourusername/RiskRadar
- You'll see a button to create a PR from your branch
- Click it and fill in the PR template

---

## 💻 Code Standards

### ✅ Code Style

RiskRadar follows **PEP 8** — Python's official style guide.

```python
# ✅ Good
def calculate_risk_score(severity: int, confidence: int, frequency: int) -> float:
    """Calculate risk score using weighted formula.
    
    Args:
        severity: Impact level (0-100)
        confidence: Threat certainty (0-100)
        frequency: Event frequency (0-100)
    
    Returns:
        Risk score (0-100)
    """
    weights = self.load_weights()
    score = (severity * weights['severity'] + 
             confidence * weights['confidence'] + 
             frequency * weights['frequency'])
    return min(100, max(0, score))


# ❌ Bad
def calc_risk(s, c, f):
    w = self.weights
    return s*w['s']+c*w['c']+f*w['f']
```

### 📝 Docstrings

All functions, classes, and modules should have docstrings:

```python
"""Module for calculating security risk scores."""

class ScoringEngine:
    """Calculate risk scores from severity, confidence, and frequency.
    
    Attributes:
        weights (dict): Scoring weights from YAML config
        config_path (str): Path to configuration file
    """
    
    def calculate_risk_score(self, severity: int, confidence: int, 
                            frequency: int) -> float:
        """Calculate risk score using weighted formula.
        
        The formula combines three metrics with configurable weights:
        risk_score = (severity × w_s) + (confidence × w_c) + (freq × w_f)
        
        Args:
            severity: Impact level if threat succeeds (0-100)
            confidence: Certainty threat is real (0-100)
            frequency: How often threat occurs (0-100)
        
        Returns:
            Risk score normalized to 0-100 range
        
        Raises:
            ValueError: If any parameter is outside 0-100 range
        """
        # Implementation here
        pass
```

### 🔤 Naming Conventions

```python
# Constants: UPPER_SNAKE_CASE
MAX_RISK_SCORE = 100
MIN_RISK_SCORE = 0
DEFAULT_WEIGHTS = {"severity": 0.35}

# Variables/Functions: lower_snake_case
risk_score = 75
triggered_rules = []
def calculate_risk_score():
    pass

# Classes: PascalCase
class ScoringEngine:
    pass

# Private methods: _leading_underscore
def _load_weights():
    pass
```

### 🏷️ Type Hints

Always use type hints:

```python
# ✅ Good
from typing import Dict, List, Optional

def evaluate_rules(self, severity: int, context: Optional[Dict] = None) -> List[str]:
    """Evaluate security rules."""
    pass

# ❌ Bad
def evaluate_rules(self, severity, context=None):
    """Evaluate security rules."""
    pass
```

### ❌ What NOT to Do

- ❌ Don't change the core scoring formula without discussion
- ❌ Don't add dependencies without approval (keep it lightweight)
- ❌ Don't commit `__pycache__` or `.pyc` files
- ❌ Don't hardcode API keys or secrets
- ❌ Don't write untested code
- ❌ Don't mix multiple features in one PR

---

## 🧪 Testing Guidelines

### ✅ Writing Tests

Tests are **required** for all new features. Write tests BEFORE implementing features (TDD-style):

```python
# backend/tests/test_scoring.py
import pytest
from backend.app.scoring import ScoringEngine

class TestScoringEngine:
    """Tests for scoring formula."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = ScoringEngine()
    
    def test_basic_calculation(self):
        """Test basic weighted scoring calculation."""
        score = self.engine.calculate_risk_score(
            severity=80,
            confidence=90,
            frequency=70
        )
        assert score == pytest.approx(81.5, rel=0.01)
    
    def test_zero_scores(self):
        """Test calculation with all zero inputs."""
        score = self.engine.calculate_risk_score(0, 0, 0)
        assert score == 0
    
    def test_max_scores(self):
        """Test calculation with all max inputs."""
        score = self.engine.calculate_risk_score(100, 100, 100)
        assert score == 100
    
    def test_invalid_severity(self):
        """Test that invalid severity raises ValueError."""
        with pytest.raises(ValueError):
            self.engine.calculate_risk_score(
                severity=-1,  # Invalid!
                confidence=50,
                frequency=50
            )
```

### 📊 Test Coverage

Aim for **>80% code coverage**:

```bash
# Run tests with coverage
pytest --cov=backend --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS/Linux
start htmlcov\index.html # Windows
```

### 🧪 Test Organization

```
backend/tests/
├── test_api.py          # API endpoint tests
├── test_rules.py        # Rule engine tests
├── test_scoring.py      # Scoring formula tests
└── test_models.py       # Data model validation tests
```

### ✅ Testing Checklist

- [ ] Tests pass locally (`pytest`)
- [ ] Code coverage > 80% (`pytest --cov`)
- [ ] Edge cases covered (0, 100, -1, None)
- [ ] Error cases tested (invalid input, missing config)
- [ ] Tests have descriptive names
- [ ] Tests have docstrings explaining what they test
- [ ] No hardcoded data (use fixtures)

---

## 📚 Documentation

### 📖 Documentation Types

**1. Code Documentation (Docstrings)**
```python
def calculate_risk_score(self, severity: int) -> float:
    """Calculate risk component from severity.
    
    Args:
        severity: Event impact level (0-100)
    
    Returns:
        Risk contribution (0-35)
    """
```

**2. Inline Comments (For Why, Not What)**
```python
# ✅ Good - explains WHY
# We cap frequency at 100 because higher values are meaningless
frequency = min(100, event_count)

# ❌ Bad - explains WHAT (obvious from code)
# Set frequency to minimum of 100 and event_count
frequency = min(100, event_count)
```

**3. File Documentation**
```python
"""
Scoring Engine Module

Calculates security risk scores using a weighted formula that combines
severity, confidence, and frequency metrics. Weights are loaded from YAML
configuration and can be customized per organization.

Example:
    >>> engine = ScoringEngine()
    >>> score = engine.calculate_risk_score(80, 90, 70)
    >>> print(score)
    81.5
"""
```

**4. Project Documentation**
- Update [README.md](README.md) for user-facing features
- Update [docs/](docs/) for design decisions
- Update examples in [samples/](samples/)

### 📝 Documentation Checklist

- [ ] Added docstrings to all new functions/classes
- [ ] Added inline comments for complex logic
- [ ] Updated README if feature is user-facing
- [ ] Updated docs/ if feature changes design
- [ ] Added example code if applicable
- [ ] Updated API documentation

---

## 🔀 Creating Pull Requests

### 📋 PR Checklist

Before submitting a pull request, ensure:

- [ ] **Tests pass**: `pytest` runs successfully
- [ ] **Code style**: Follows PEP 8
- [ ] **Coverage**: New code has tests (>80% coverage)
- [ ] **Documentation**: Docstrings and comments added
- [ ] **No dependencies added**: Or approved by maintainers
- [ ] **Branch is up-to-date**: `git pull upstream main`
- [ ] **Descriptive commits**: Clear commit messages
- [ ] **PR description filled out**: Following template

### 📝 PR Template

Use this template for PR descriptions:

```markdown
## 🎯 Description
Brief description of what this PR does

## 🐛 Related Issue
Fixes #123 (if applicable)

## 🔍 Type of Change
- [ ] Bug fix (non-breaking)
- [ ] New feature (non-breaking)
- [ ] Breaking change
- [ ] Documentation update

## ✅ Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Coverage maintained (>80%)

## 📚 Documentation
- [ ] README updated
- [ ] Docstrings added
- [ ] Comments added for complex logic
- [ ] Examples updated

## 🔄 Checklist
- [ ] Code follows style guidelines
- [ ] No new warnings generated
- [ ] Reviewed own code before submitting
```

### 🚀 Example PR Title Formats

```
✨ feat: add rule for detecting privilege escalation
🐛 fix: resolve risk score off-by-one error
📖 docs: improve installation instructions
🧪 test: add edge case tests for rule engine
♻️ refactor: simplify scoring calculation
⚡ perf: optimize rule evaluation
```

---

## 🐛 Reporting Bugs

### 🐛 Bug Report Checklist

When reporting a bug, please include:

1. **Description**: What's the problem?
2. **Reproduction Steps**: How to reproduce it?
3. **Expected Behavior**: What should happen?
4. **Actual Behavior**: What actually happens?
5. **Environment**: Python version, OS, etc.
6. **Error Message**: Full stack trace
7. **Screenshots**: If UI-related

### 📋 Example Bug Report

```markdown
## 🐛 Bug: Risk Score Exceeds 100

### Description
Risk score calculation is returning values > 100 in some cases.

### Reproduction Steps
1. Start the server
2. POST to /calculate-risk with:
   - severity: 100
   - confidence: 100
   - frequency: 100
3. Observe response

### Expected Behavior
Risk score should be capped at 100

### Actual Behavior
Risk score is 100.0 (OK) — need actual failing case

### Environment
- Python: 3.10.2
- OS: Windows 11
- RiskRadar: v1.0

### Error Message
```
POST /calculate-risk HTTP/1.1
Response: {"risk_score": 101.5}
```
```

---

## 💡 Proposing Features

### ✨ Feature Request Checklist

1. **Check existing issues**: Is it already suggested?
2. **Use feature template**: [Feature Template](https://github.com/yourusername/RiskRadar/issues/new?template=feature_request.md)
3. **Describe motivation**: Why is this needed?
4. **Provide examples**: Show use cases
5. **Discuss constraints**: What's NOT in scope?

### 📋 Example Feature Request

```markdown
## 💡 Feature: Add Support for Custom Rule Functions

### Motivation
Currently, rules are hardcoded in engine.py. Organizations need to add
custom rules without modifying source code.

### Proposed Solution
Allow users to define rules in YAML:

```yaml
custom_rules:
  - name: "Contractor Access"
    condition: "context.user_type == 'contractor' AND severity >= 50"
    message: "Contractor account with elevated risk activity"
```

### Use Cases
- SOCs want org-specific rules
- MSPs need per-client rules
- Testing custom logic without rebuilding

### Acceptance Criteria
- [ ] Rules loaded from YAML
- [ ] Support boolean conditions
- [ ] Test coverage > 80%
- [ ] Documentation added
```

---

## 📖 Commit Message Guidelines

Write clear, descriptive commit messages:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Examples

```
✨ feat(rules): add privilege escalation detection rule

Add new rule that detects when privileged accounts (admin, root) are
used in unusual ways. This helps identify potential account compromise
or privilege abuse attacks.

Fixes #42
```

```
🐛 fix(scoring): prevent risk score from exceeding 100

Risk score normalization was not capping values at 100 in edge cases
where all weights sum > 1.0. Added explicit min(100, score) check.

Fixes #35
```

```
📖 docs: add custom rule examples to README

Include YAML examples showing how to customize scoring weights and
define custom rules for different organizational needs.
```

### Type Prefixes

- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation
- `style:` — Code style (formatting, semicolons, etc)
- `refactor:` — Code refactoring
- `perf:` — Performance improvement
- `test:` — Adding/updating tests
- `chore:` — Build, dependencies, etc

### Scope Examples

- `scoring` — Scoring formula
- `rules` — Rule engine
- `api` — HTTP endpoints
- `models` — Data models
- `config` — Configuration
- `tests` — Test suite
- `docs` — Documentation

---

## ❓ Questions & Support

### 🤔 Not Sure Where to Start?

1. **Look for ["good first issue"](https://github.com/yourusername/RiskRadar/issues?q=label%3A%22good+first+issue%22)** — These are beginner-friendly
2. **Check [documentation](docs/)** — Design philosophy, architecture
3. **Review [existing code](backend/)** — See how things work
4. **Ask in [discussions](https://github.com/yourusername/RiskRadar/discussions)** — Community is friendly!

### 📞 Communication Channels

| Channel | Best For | Response Time |
|---------|----------|---|
| **Issues** | Bug reports, feature requests | 24-48 hours |
| **Discussions** | Questions, ideas, brainstorming | 24 hours |
| **Pull Requests** | Code review, feedback | 48 hours |
| **Email** | Sensitive topics | 72 hours |

### 🙏 Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

**Be respectful, inclusive, and professional.** ✨

---

## 🎉 Contributing is Awesome!

Whether you're fixing typos, adding tests, or implementing major features:

✅ **Your contribution matters!**
✅ **We appreciate the effort!**
✅ **Together, we make security better!**

### 🏆 Recognition

Contributors are recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md)
- GitHub's "Contributors" page
- Release notes

---

## 📚 Additional Resources

- [Project README](README.md)
- [Design Methodology](docs/methodology.md)
- [Scoring Formula](docs/scoring.md)
- [Roadmap](docs/roadmap.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Git Cheatsheet](https://github.github.com/training-kit/downloads/github-git-cheat-sheet.pdf)

---

<div align="center">

### 🎉 **Happy Contributing!**

Questions? Open an issue or start a discussion. The community is here to help! 🙌

**Made with ❤️ by the RiskRadar Community**

</div>
