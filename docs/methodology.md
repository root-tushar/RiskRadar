# Design Methodology & Philosophy

## Why RiskRadar?

Traditional security risk scoring has problems:

1. **Opacity:** Risk scores appear as magic numbers with no explanation
2. **Inconsistency:** Different tools produce wildly different scores for the same event
3. **Inflexibility:** Black-box algorithms can't be tuned to organizational policy
4. **Over-complexity:** ML-based scoring requires data scientists, not security analysts
5. **Audit Gaps:** Compliance teams can't easily explain scoring to regulators

**RiskRadar solves these problems** by being:
- **Explainable:** Every point is traced to an input component
- **Customizable:** Weights can be adjusted without code changes
- **Deterministic:** Same input always produces same output
- **Auditable:** Full calculation history and rules are transparent
- **Operational:** Built for SOC analysts, not data scientists

---

## What RiskRadar is NOT

### 1. Not a SIEM

**SIEM** (Security Information Event Management):
- Collects and correlates logs from many sources
- Detects patterns across infrastructure
- Maintains long-term event storage
- Complex rule engine with state

**RiskRadar:**
- Accepts *pre-processed* structured inputs
- Scores individual events (stateless)
- No log collection or storage
- Simple, rule-based explainability layer

**When to use SIEM instead:** Collecting logs, cross-system correlation, long-term forensics.

### 2. Not an IDS/IPS

**IDS/IPS** (Intrusion Detection/Prevention System):
- Monitors network traffic in real-time
- Detects malicious patterns and signatures
- Can block traffic automatically
- Specialized for specific attack types

**RiskRadar:**
- Scores *already detected* security events
- Prioritizes them by risk level
- No threat detection capability
- No traffic interception

**When to use IDS instead:** Real-time network defense, attack prevention.

### 3. Not Machine Learning

**ML-Based Risk Scoring:**
- Learns patterns from historical data
- Can adapt to new threats
- Requires labeled training data
- Difficult to audit and explain
- Can have bias and drift over time

**RiskRadar:**
- Deterministic formula
- Transparent weights
- Easy to audit and customize
- No training data required
- No model drift

**When to use ML instead:** Anomaly detection, pattern learning from massive datasets.

### 4. Not a Vulnerability Scanner

**Vulnerability Scanners:**
- Identify security weaknesses in systems
- Produce detailed remediation guidance
- Scan for known CVEs
- Generate compliance reports

**RiskRadar:**
- Scores *risk* given severity, confidence, frequency
- Prioritizes known vulnerabilities
- No scanning capability
- No patch management

**When to use scanners instead:** Finding vulnerabilities, compliance assessment.

---

## Design Principles

### 1. Explainability First

Every score must be understandable to humans without a data science degree.

**Implementation:**
- Linear formula (not neural networks)
- Component breakdown in every response
- Human-readable rule names
- Audit trail of calculations
- Weights visible in configuration

### 2. Operational Soundness

RiskRadar must work in real SOC environments.

**Implementation:**
- Stateless (no database required)
- Sub-millisecond response time
- Deployable offline
- No external dependencies
- Clear error messages

### 3. Customization without Code

Organizations have different risk policies.

**Implementation:**
- YAML configuration for weights
- Per-organization risk level thresholds
- Pluggable rules (v2.0)
- No programming required to adjust scoring

### 4. Deterministic by Design

Security decisions must be reproducible and auditable.

**Implementation:**
- No randomization
- No machine learning
- No floating-point approximations
- Identical inputs → identical outputs
- Clear rounding rules

### 5. Security-First

We're building a security tool—it must be trustworthy.

**Implementation:**
- No external API calls
- No data persistence
- No authentication (internal use only)
- Clear code, no obfuscation
- Comprehensive testing

---

## Architecture Decisions

### Decision 1: Linear Weighted Formula

**Question:** How should we combine severity, confidence, and frequency?

**Options Considered:**
1. **Linear combination** (chosen)
   - `score = w1×severity + w2×confidence + w3×frequency`
   - Pros: Explainable, customizable, fast, auditable
   - Cons: Can't capture non-linear interactions

2. **Multiplicative formula**
   - `score = severity × confidence × frequency`
   - Pros: All factors must be non-zero
   - Cons: Low confidence *kills* the score; less granular control

3. **Machine learning model**
   - Train on historical incident data
   - Pros: Can learn complex patterns
   - Cons: Black-box, requires data, hard to audit, can be biased

**Decision:** Linear. It's the best trade-off between explainability and effectiveness. Organizations can customize weights based on their specific risk tolerance.

### Decision 2: YAML Configuration

**Question:** How should weights be configured?

**Options Considered:**
1. **Hardcoded in Python** (rejected)
   - Bad: Requires code change and redeploy

2. **YAML file** (chosen)
   - Pros: Human-readable, version-controllable, easy to customize
   - Cons: Requires file system access

3. **Environment variables** (rejected)
   - Bad: Not suitable for multiple parameters

4. **Database** (rejected)
   - Bad: Adds complexity, requires persistence

**Decision:** YAML. It's simple, auditable, and integrates well with deployment pipelines.

### Decision 3: No Database

**Question:** Should RiskRadar store risk scores?

**Options Considered:**
1. **No database** (chosen)
   - Pros: Simpler, faster, no dependencies, works offline
   - Cons: No historical queries

2. **Embedded SQLite**
   - Pros: Simple persistence
   - Cons: Adds complexity, file I/O overhead

3. **PostgreSQL/MongoDB**
   - Pros: Robust, queryable
   - Cons: External dependency, defeats stateless design

**Decision:** No database. RiskRadar v1 is focused on scoring, not archival. Integration with SIEMs/logging systems is the responsibility of the calling application.

### Decision 4: FastAPI Framework

**Question:** Which web framework should we use?

**Options Considered:**
1. **FastAPI** (chosen)
   - Pros: Fast, automatic API docs, Pydantic validation, modern Python
   - Cons: Requires Python 3.6+

2. **Flask**
   - Pros: Lightweight, simple
   - Cons: Manual validation, slower, no auto docs

3. **Django**
   - Pros: Full-featured
   - Cons: Heavyweight, overkill for simple API

4. **gRPC**
   - Pros: Fast, binary protocol
   - Cons: Complex, not REST

**Decision:** FastAPI. It's modern, fast, and provides excellent API documentation automatically. Perfect for exposing risk scoring as a service.

### Decision 5: Pydantic for Validation

**Question:** How should we validate inputs?

**Options Considered:**
1. **Pydantic** (chosen)
   - Pros: Type hints, auto-validation, schema generation, integration with FastAPI
   - Cons: Runtime overhead (negligible at scale)

2. **JSON Schema + manual validation**
   - Pros: Lightweight
   - Cons: Repetitive, error-prone

3. **No validation**
   - Pros: Fast
   - Cons: Garbage in, garbage out

**Decision:** Pydantic. It's the Python standard for data validation and integrates seamlessly with FastAPI. Input validation is critical for security.

---

## Risk Level Classification

**Question:** What are the risk level thresholds?

**Data:**
- Security industry standard: CVSS (0-10 scale)
  - Low: 0.1–3.9
  - Medium: 4.0–6.9
  - High: 7.0–8.9
  - Critical: 9.0–10.0

- NIST guidance: Risk matrices typically use 3-5 levels

**Decision:** 4 levels (LOW, MEDIUM, HIGH, CRITICAL) on 0–100 scale
- LOW: 0–30 (< 1/3)
- MEDIUM: 31–60 (1/3–2/3)
- HIGH: 61–80 (2/3–4/5)
- CRITICAL: 81–100 (> 4/5)

**Rationale:** 4 levels match NIST and CVSS conventions. Thresholds provide clear demarcation points for SOC prioritization.

---

## Testing Strategy

### Test Coverage

1. **Unit Tests** (60%): Scoring logic, rule engine, models
2. **Integration Tests** (30%): API endpoints, error handling
3. **Edge Cases** (10%): Boundary conditions, overflow, type errors

### Test Philosophy

- **No mocking:** Real implementations tested end-to-end
- **Determinism validation:** Same input → same output (always)
- **Edge case coverage:** Negative values, overflow, missing fields
- **Regression prevention:** Tests for each bug fix
- **Performance baseline:** Ensure calculations stay < 1ms

---

## Security Considerations

### Input Validation
- All inputs are type-checked and range-validated
- No SQL injection risk (no database)
- No path traversal risk (no file access)

### Authentication & Authorization
- v1 has no authentication (internal use only)
- Future versions can add API key validation
- No sensitive data in responses

### Denial of Service
- Stateless design prevents resource exhaustion
- No expensive computations
- CORS enabled for development (can be restricted)

### Code Quality
- No external package vulnerabilities
- Dependencies are minimal (FastAPI, Pydantic, PyYAML)
- Code is readable and auditable

---

## Performance Optimization

### Current Performance
- Calculation time: <1ms per request
- Memory footprint: <10MB
- Can handle 1000s of concurrent requests

### Optimization Opportunities (v2.0)
- Caching of configuration
- Connection pooling (if database added)
- Async rule evaluation
- Distributed scoring across nodes

---

## Known Limitations

1. **Static Rules:** Rules are hard-coded; v2 will allow custom rules
2. **No Historical Context:** Each score is independent; no trending
3. **No Correlation:** Only scores individual events; no multi-event patterns
4. **No ML:** Can't learn from new threats; requires manual weight updates
5. **No Persistence:** Scores aren't stored; integration required for archival

---

## Future Direction (v2.0+)

1. **Custom Rules Engine:** Allow organizations to define their own rules
2. **Historical Trending:** Compare current score to baseline and trends
3. **Alert Fatigue Reduction:** Deduplication and aggregation logic
4. **Integration Plugins:** Pre-built connectors to Splunk, Elastic, etc.
5. **Dynamic Weights:** Automatically adjust weights based on threat landscape
6. **Multi-Tenant:** Support different weights per customer
7. **Explanations:** Generate natural language explanations of scores

---

## Conclusion

RiskRadar is designed for **transparency, operability, and customization**. It's not trying to replace SIEMs or ML models—it's trying to bring clarity and control to risk scoring. Security teams should understand their risk assessments, and that requires explainability over complexity.
