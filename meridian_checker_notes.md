# Meridian Foundation Reserve — Checker Notes

Run the checker with:

```bash
python3 mandate.py
```

## Known-answer validation

The checker calculates a 3.0% reserve minimum from four quarterly $0.75 million distributions divided by the $100 million reserve. It reproduces the known checks: A passes, B fails the reserve, redemption, and Acme issuer checks, and C fails only the reserve check; Acme bonds and stock are aggregated for the issuer rule.

## Negative-weight test

For the temporary test, Candidate A was changed to Cash = -2% and Global equity index fund = 64%. The checker then showed a -2.0% lowest weight and failed only the long-only rule; the reserve-eligible weight remained 10.0% and passed. The original Candidate A inputs were restored afterward.

## Candidate D — a passing portfolio the CIO could reject

Candidate D holds 3% Cash and 97% Treasury 10-year notes. It passes every checkable rule: it meets the 3% reserve minimum, is fully redeemable within five business days, and Treasury securities are issuer-limit exempt.

The objection holds because Candidate D exposes S2: a 97% long-duration Treasury portfolio may not be a feasible way to achieve CPI + 4% net of costs over rolling five-year periods. S2, together with the missing pilot-optimization instruction in S10, decides whether that otherwise compliant portfolio is acceptable.

## Question for the CIO

**Question:** What should the pilot optimize—probability of achieving CPI + 4% net of costs, expected return relative to the 60/40 benchmark, downside-risk control, or another explicit metric?

**Portfolio-changing answer:** If the CIO prioritizes a credible probability of CPI + 4% over five-year periods, I would move away from Candidate D’s Treasury concentration toward a diversified growth allocation while preserving the required reserve and redemption liquidity. If the CIO instead prioritizes capital stability under a formal loss limit, I would retain more government securities and accept that the return objective may be harder to meet.
