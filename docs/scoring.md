# Scoring Methodology

## Formula

RiskRadar uses a **linear weighted combination** of three security metrics:

```
Risk Score = (Severity × w_severity) + (Confidence × w_confidence) + (Frequency × w_frequency)

where:
  - Severity:   Impact level of the event (0–100)
  - Confidence: How certain we are the threat is real (0–100)
  - Frequency:  How often the event occurs (0–100)
  - w_*:        Configurable weights (default: 0.35, 0.35, 0.30)
```

### Example Calculation

**Input:**
- Severity: 80 (high impact)
- Confidence: 75 (mostly certain)
- Frequency: 90 (very frequent)
- Weights: [0.35, 0.35, 0.30]

**Calculation:**
```
risk_score = (80 × 0.35) + (75 × 0.35) + (90 × 0.30)
           = 28 + 26.25 + 27
           = 81.25
```

**Risk Level:** CRITICAL (81–100)

---

## Risk Levels

| Level | Range | Interpretation | Action |
|-------|-------|-----------------|--------|
| **LOW** | 0–30 | Minimal risk, routine event | Monitor, log |
| **MEDIUM** | 31–60 | Notable risk, elevated monitoring required | Investigate, consider mitigation |
| **HIGH** | 61–80 | Significant risk, immediate action recommended | Escalate, implement controls |
| **CRITICAL** | 81–100 | Severe risk, urgent response required | Immediate escalation, incident response |

---

## Input Metrics

### Severity (Default Weight: 0.35)

The potential **impact** of the security event if it succeeds.

**Examples:**
- **0–20:** Informational, no impact (service health check)
- **20–50:** Low impact (failed non-admin authentication)
- **50–75:** Medium impact (unauthorized data access)
- **75–95:** High impact (admin account compromise)
- **95–100:** Critical (production data exfiltration, ransomware)

### Confidence (Default Weight: 0.35)

How **certain** we are that the detected event is a real threat (not a false positive).

**Examples:**
- **0–30:** Low confidence, likely benign (test activity, known false positive)
- **30–60:** Moderate confidence, possible threat
- **60–85:** High confidence, likely real threat
- **85–100:** Very high confidence, definitely a threat

### Frequency (Default Weight: 0.30)

How **often** the event occurs or how many times it has been observed.

**Examples:**
- **0–25:** Rare, isolated incident
- **25–50:** Occasional, sporadic activity
- **50–75:** Regular, recurring pattern
- **75–100:** Very frequent, sustained or epidemic activity

---

## Customizing Weights

Weights are loaded from `backend/config/scoring_weights.yaml`:

```yaml
weights:
  severity: 0.35
  confidence: 0.35
  frequency: 0.30
```

### Weight Customization Scenarios

**Scenario 1: Maximize Severity**
```yaml
weights:
  severity: 0.50
  confidence: 0.30
  frequency: 0.20
```
*Use when: You want impact assessment to dominate (e.g., financial theft is worse than repeated low-impact attempts)*

**Scenario 2: Maximize Confidence**
```yaml
weights:
  severity: 0.25
  confidence: 0.50
  frequency: 0.25
```
*Use when: False positives are expensive (e.g., alerts sent to law enforcement)*

**Scenario 3: Maximize Frequency**
```yaml
weights:
  severity: 0.30
  confidence: 0.30
  frequency: 0.40
```
*Use when: Volume and patterns matter most (e.g., detecting distributed attacks)*

### Important Notes

1. **Weights must sum to 1.0** (RiskRadar auto-normalizes if they don't)
2. **Changes apply globally** to all risk calculations
3. **No restart required** (configuration reloaded per request)
4. **Changes are transparent** (weights are logged and can be audited)

---

## Rule Engine

Beyond the numeric score, RiskRadar evaluates **5 security detection rules**:

### Rule 1: Multiple Failed Login Attempts
- **Trigger Condition:** `failed_logins > 5`
- **Severity:** Indicates brute force or credential stuffing
- **Action:** Requires investigation and potentially account lockout

### Rule 2: High-Severity Event
- **Trigger Condition:** `severity >= 80`
- **Severity:** High-impact event detected
- **Action:** Escalate immediately

### Rule 3: Privileged Account Activity
- **Trigger Condition:** `is_privileged == true`
- **Severity:** Admin/root-level accounts are high-value targets
- **Action:** Log and monitor all privileged activity

### Rule 4: High Event Frequency
- **Trigger Condition:** `frequency > 85`
- **Severity:** Sustained or mass activity pattern
- **Action:** Indicates potential epidemic/campaign

### Rule 5: Confidence-Severity Mismatch
- **Trigger Condition:** `severity >= 75 AND confidence <= 40`
- **Severity:** Suspicious pattern—we think it's bad, but we're not sure
- **Action:** Requires urgent investigation to resolve uncertainty

---

## Scoring Philosophy

### Why Linear Weighting?

1. **Explainability:** Every point in the score is traceable to an input
2. **Simplicity:** No black-box models, easy to audit
3. **Determinism:** Same input always produces same output
4. **Operability:** SOC analysts can reason about scores manually
5. **Customization:** Organizations can adjust weights to match policy

### Why These Weights?

The default weights (0.35, 0.35, 0.30) reflect a balanced approach:

- **Severity + Confidence (70%):** Impact and certainty are equally important
- **Frequency (30%):** Volume matters, but is secondary to severity/confidence

This can be customized per organization based on:
- Industry (finance vs. tech vs. healthcare)
- Risk appetite
- Incident response capabilities
- Regulatory requirements

### Why No Machine Learning?

RiskRadar intentionally avoids ML models because:

1. **Transparency:** ML is a "black box"; RiskRadar is fully explainable
2. **Auditability:** No training data bias, no model drift
3. **Reliability:** Deterministic output is critical for security
4. **Deployability:** Works offline, no API dependencies
5. **Control:** Security team, not data scientists, controls risk assessment

---

## Integration Guidance

### Input Mapping from Other Tools

**From SIEM/IDS:**
- Severity → Alert priority or confidence score
- Confidence → Detection accuracy or signature match confidence
- Frequency → Event count or occurrence pattern

**From Vulnerability Scanners:**
- Severity → CVSS base score
- Confidence → Exploit reliability (0 = unproven, 100 = proven RCE)
- Frequency → Number of instances found

**From Behavioral Analytics:**
- Severity → Anomaly deviation from baseline
- Confidence → Statistical significance of deviation
- Frequency → Number of observed instances

---

## Edge Cases

### What if all inputs are 0?
```
risk_score = 0
risk_level = "LOW"
```
→ No risk detected.

### What if all inputs are 100?
```
risk_score = 100
risk_level = "CRITICAL"
```
→ Maximum risk detected.

### What if inputs exceed 100 or go negative?
RiskRadar **clamps** values to [0, 100]:
```python
severity = max(0, min(100, severity))
```
→ Prevents calculation errors and maintains determinism.

### What about floating-point precision?
RiskRadar rounds final scores to 2 decimal places:
```python
risk_score = round(risk_score, 2)
```
→ Ensures consistent output and prevents false precision claims.

---

## Performance

- **Calculation time:** <1ms per request
- **Memory usage:** <10MB for the entire application
- **Concurrent requests:** Handles thousands per second (stateless)
- **Configuration reload:** <1ms, no request blocking

---

## Future Enhancements (v2.0+)

- **Dynamic weight adjustment:** Weights that change based on threat landscape
- **Historical baselines:** Compare current score to historical context
- **Multi-stage scoring:** Different weights for initial vs. refined assessment
- **Custom rules:** Allow organizations to define their own detection rules
- **Score evolution:** Track how risk changes over time
- **Integration plugins:** Direct connectors to popular SIEM/monitoring tools

For full roadmap, see [docs/roadmap.md](roadmap.md).
