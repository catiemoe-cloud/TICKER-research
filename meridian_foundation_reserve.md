# Meridian Foundation Reserve — Requirement Sort and Candidate Check

## Sort before building

| ID | Classification | Reason |
|---|---|---|
| S1 | Hard constraint | Seven-year horizon and annual rebalancing are implementation requirements. |
| S2 | Objective | Seek CPI + 4% net of costs over rolling five-year periods. |
| S3 | Hard constraint | Hold 12 months of payouts in cash or daily-liquid government securities. |
| S4 | Missing | A benchmark is named, but its role in construction is not defined. |
| S5 | Hard constraint | Long-only; no borrowing, short sales, or derivatives. |
| S6 | Hard constraint | No non-exempt issuer may exceed 8%. |
| S7 | Hard constraint | Turnover may not exceed 25% without committee approval. |
| S8 | Hard constraint | At least 90% must be redeemable within five business days. |
| S9 | Unverifiable promise | The loss statement has no measure, monitoring method, or breach rule. |
| S10 | Missing | No pilot optimization criterion is stated. |

## Candidate checks

The reserve is $100 million. Twelve months of payouts equal $3 million ($0.75 million × 4), so S3 requires at least **3%** in reserve-eligible assets.

| Check | A | B | C |
|---|---:|---:|---:|
| Reserve-eligible liquidity | 14% | 1% | 2% |
| S3: at least 3% reserve-eligible | Pass | Fail | Fail |
| Redeemable within five business days | 100% | 85% | 100% |
| S8: at least 90% within five days | Pass | Fail | Pass |
| Largest non-exempt issuer | 0% Acme | 9% Acme | 8% Acme |
| S6 issuer limit | Pass | Fail | Pass |
| S5 long-only/no borrowing, shorts, or derivatives | Pass from listed holdings | Pass from listed holdings | Pass from listed holdings |
| S7 turnover, S2 return objective, S9 loss rule | Unresolved | Unresolved | Unresolved |

Candidate A is the only A–C candidate meeting the observable liquidity and issuer constraints. No candidate is fully approvable from static weights because turnover, expected net return, and the loss rule cannot be verified.

Before optimization, the CIO must specify the pilot’s objective, operationalize S9 (risk measure, monitoring, and breach response), and clarify whether S4 is evaluation only or a relative-risk constraint.

## Investment policy statement

An investment policy statement (IPS) is the governing agreement that converts a client’s purpose, return goal, spending need, risk tolerance, time horizon, and restrictions into construction and monitoring rules. It distinguishes objectives from constraints so the portfolio is managed against written client terms rather than unstated preferences.

| IPS component | Meridian statements | Meaning |
|---|---|---|
| Horizon and review | S1 | Seven-year planning horizon; annual rebalance. |
| Return objective | S2 | CPI + 4% net over rolling five years. |
| Spending and liquidity | S3 | Quarterly distributions and a one-year liquid reserve. |
| Benchmark and evaluation | S4 | 60% global equity/40% U.S. investment-grade bonds; construction role unresolved. |
| Restrictions | S5–S8 | Long-only, issuer cap, turnover cap, and redemption liquidity. |
| Risk governance | S9 | Loss-control intent; rule not operationalized. |
| Preferences/authority | S10 | No stated style preferences; pilot objective missing. |

## Reflection

A portfolio can pass every checkable rule and still be wrong because a checklist cannot establish that it can meet the CPI + 4% objective, suits the seven-year horizon, or matches intended loss tolerance. Candidate D demonstrates this: it passes mechanically but its Treasury concentration may be inconsistent with S2 and exposes S10’s missing optimization choice.

I was least certain about S4: a benchmark is useful for evaluation but is not automatically a construction constraint. Without a tracking-error or relative-return instruction, I classified its construction role as missing instead of silently imposing an allocation rule.
