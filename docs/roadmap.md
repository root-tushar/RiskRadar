# RiskRadar Roadmap

## Vision

RiskRadar v1.0 is a **foundation**—a trusted, transparent risk scoring engine that security teams can build upon. The roadmap outlines how RiskRadar will evolve to address emerging needs while maintaining explainability and operability.

---

## v1.0 (Current - January 2026)

### ✅ Completed

- [x] Risk scoring engine with weighted formula
- [x] Rule-based explainability layer
- [x] FastAPI HTTP server
- [x] Pydantic data validation
- [x] Comprehensive unit tests
- [x] API documentation
- [x] YAML configuration
- [x] Full project documentation
- [x] Sample inputs/outputs
- [x] GitHub-ready structure

### Status: Production Ready

---

## v1.1 (Q2 2026)

### Bug Fixes & Stability

- [ ] Address any production issues reported
- [ ] Performance profiling and optimization
- [ ] Additional edge case tests
- [ ] Docker containerization
- [ ] Kubernetes deployment guide

### Minor Enhancements

- [ ] Support for custom context fields
- [ ] Rate limiting guidelines
- [ ] Monitoring/observability guide
- [ ] Deployment automation (GitHub Actions)

**Target:** Stable, widely deployed, battle-tested.

---

## v2.0 (Q4 2026)

### Major Features

#### 1. Custom Rules Engine

**Problem:** Current rules are hard-coded; organizations want their own.

**Solution:** DSL (Domain Specific Language) for defining rules

```yaml
custom_rules:
  - name: "SQL Injection Detected"
    conditions:
      - field: context.payload
        pattern: "SQL.*OR.*1=1"
        weight: 1.2  # 20% score boost if triggered
      - field: severity
        min: 70
    action: "flag"
```

**Benefits:**
- No code changes required
- YAML-based rule definition
- Backwards compatible
- Audit trail of rule changes

#### 2. Historical Trending

**Problem:** Single scores don't show if risk is increasing or decreasing.

**Solution:** Optional SQLite backend with trend analysis

```json
{
  "risk_score": 75,
  "risk_level": "HIGH",
  "trend": {
    "1h_change": "+5",
    "24h_change": "+15",
    "trajectory": "increasing"
  }
}
```

**Benefits:**
- Detect emerging patterns
- Compare to organization baseline
- Early warning system

#### 3. Alert Aggregation

**Problem:** High-frequency events cause alert fatigue.

**Solution:** Grouping and deduplication logic

```json
{
  "events": 42,
  "first_seen": "2026-01-07T10:00:00Z",
  "last_seen": "2026-01-07T10:15:00Z",
  "aggregated_risk_score": 68
}
```

**Benefits:**
- Reduce noise
- Focus on campaigns vs. isolated incidents
- Configurable aggregation windows

#### 4. Multi-Tenant Support

**Problem:** Enterprises want different weights per department/customer.

**Solution:** Tenant-aware configuration and scoring

```yaml
tenants:
  finance:
    weights:
      severity: 0.50    # Money is critical
      confidence: 0.30
      frequency: 0.20
  engineering:
    weights:
      severity: 0.30
      confidence: 0.40  # False positives expensive
      frequency: 0.30
```

**Benefits:**
- Single deployment for multiple teams
- Per-tenant customization
- Consistent audit trails

#### 5. Integration Plugins

**Problem:** Every organization has a different tech stack.

**Solution:** Pre-built connectors to popular tools

```python
# Example: Splunk integration
@riskradar.plugin("splunk")
def splunk_query(query: str) -> List[RiskInput]:
    """Convert Splunk events to RiskRadar inputs."""
    ...

# Example: AWS SecurityHub integration
@riskradar.plugin("securityhub")
def parse_securityhub_findings(finding: dict) -> RiskInput:
    """Map SecurityHub findings to risk inputs."""
    ...
```

**Planned Connectors:**
- Splunk
- Elastic Stack
- AWS SecurityHub
- Azure Sentinel
- Datadog
- New Relic

**Benefits:**
- Plug-and-play integration
- No custom code required
- Reduced time-to-value

---

## v2.5 (Q2 2027)

### Machine Learning Foundation (Opt-In)

**Important:** ML is optional and never replaces explainable scoring.

#### 1. Anomaly Detection

```python
# Optional ML layer for context-based anomalies
@riskradar.detect_anomalies(model="isolation_forest")
def detect_user_anomalies(user_id: str, event: RiskInput) -> bool:
    """Is this user's behavior anomalous today?"""
    ...
```

**Use Case:** Detect "impossible travel" or unusual privilege escalation patterns

**Constraints:**
- Fully explainable (SHAP/LIME)
- No black-box predictions
- All anomalies have interpretable explanations

#### 2. Dynamic Weight Optimization

```python
# Optional: Learn weights from security outcomes
@riskradar.optimize_weights(feedback="incident_outcome")
def retrain_weights(historical_scores, actual_outcomes):
    """Optimize weights based on how well scores predicted incidents."""
    ...
```

**Use Case:** Self-tune weights based on SOC effectiveness

**Constraints:**
- Human approval required before changes
- Weights never change by >10% per iteration
- Full audit trail of changes
- Rollback capability

---

## v3.0 (2027+)

### Enterprise Features

#### 1. GraphQL API

Support for complex, nested queries alongside REST.

#### 2. Explanation Generation

Natural language explanations of scores:

```json
{
  "risk_score": 82,
  "explanation": "This event has a CRITICAL risk score because of high severity (80/100) combined with privileged account access (admin@company.com). The system detected 6 failed login attempts and high-frequency events (90/100), suggesting a potential compromise attempt. Immediate investigation recommended."
}
```

#### 3. Multi-Stage Scoring

Different scoring logic for different stages:
- **Triage:** Quick initial assessment
- **Investigation:** Refined scoring with more context
- **Remediation:** Post-incident analysis

#### 4. Federated Scoring

Combine scores from multiple RiskRadar instances:

```
Local Score + (Remote Score × locality_weight) = Federated Score
```

#### 5. Compliance & Audit Reports

Automated generation of risk reports for compliance teams:
- PCI-DSS
- HIPAA
- SOC 2
- NIST

---

## Long-Term Vision (2028+)

### Ecosystem

**RiskRadar as a Standard**

1. **Vendor Integration:** SIEM/IDS vendors implement RiskRadar scoring
2. **Community Rules:** Open repository of community-contributed rules
3. **Academic Research:** Support for security research partnerships
4. **Industry Standards:** Become reference implementation for explainable risk scoring

### Research Opportunities

1. **Fairness in Security:** Ensure scores don't discriminate by user/geography
2. **Adversarial Robustness:** Study how attackers might game the scoring
3. **Game Theory:** Optimal weight allocation given attacker strategies
4. **Human Factors:** How scores should be presented to different audiences

---

## Non-Goals (What RiskRadar Won't Do)

1. **Become a SIEM:** Log storage and correlation belong in specialized tools
2. **Replace Expert Review:** RiskRadar assists humans, doesn't replace them
3. **Predict Future Attacks:** That's machine learning's job, and RiskRadar is intentionally not ML-based
4. **Handle Real-Time Detection:** IDS/IPS systems are better suited
5. **Patch Management:** Vulnerability management is a separate discipline

---

## Contributing to the Roadmap

Community input shapes the roadmap. To propose features:

1. **Open a GitHub issue** with the tag `rfc` (Request for Comment)
2. **Discuss the use case** and how it benefits RiskRadar users
3. **Provide feedback** on prioritization and implementation approach
4. **Join the conversation** with the core team

---

## Metrics for Success

As RiskRadar evolves, we'll measure success by:

- **Adoption:** Number of organizations using RiskRadar
- **Integration:** Number of pre-built connectors
- **Community:** Contributions, custom rules, plugins
- **Reliability:** Uptime, performance, test coverage
- **Transparency:** How well users understand their scores
- **Impact:** Stories of how RiskRadar improved security outcomes

---

## Timeline Summary

| Version | Target | Focus |
|---------|--------|-------|
| **v1.0** | Q1 2026 | Foundation, explainability, core scoring |
| **v1.1** | Q2 2026 | Stability, deployment, observability |
| **v2.0** | Q4 2026 | Custom rules, trends, plugins, multi-tenant |
| **v2.5** | Q2 2027 | Optional ML, dynamic weights |
| **v3.0** | 2027+ | Enterprise features, ecosystem |

---

## Getting Involved

Want to help shape RiskRadar's future?

- **Test v2.0 features** when they're in beta
- **Contribute custom rules** for your industry
- **Report bugs** with detailed reproduction steps
- **Suggest features** based on real SOC challenges
- **Help with documentation** and examples
- **Build plugins** for your organization's tools

See [CONTRIBUTING.md](contributing.md) for details.

---

**Last Updated:** January 7, 2026  
**Status:** Community-driven, transparent roadmap
