# Meridian Foundation Reserve — Requirement Sort and Candidate Check

## Sort before building

| ID | Classification | Reason |
|---|---|---|
| S1 | Hard constraint | The seven-year horizon and annual-rebalancing schedule are implementation requirements. |
| S2 | Objective | The reserve seeks CPI + 4% net of costs over rolling five-year periods. |
| S3 | Hard constraint | Twelve months of quarterly payouts must be held in cash or daily-liquid government securities. |
| S4 | Missing | A benchmark is named, but the CIO has not said whether it is only for evaluation or whether the portfolio must control active risk or optimize relative to it. |
| S5 | Hard constraint | Long-only and no borrowing, short sales, or derivatives are explicit prohibitions. |
| S6 | Hard constraint | A single issuer may not exceed 8%, with the listed exemptions. |
| S7 | Hard constraint | Annual turnover may not exceed 25% without committee approval. |
| S8 | Hard constraint | At least 90% of the reserve must be redeemable within five business days. |
| S9 | Unverifiable promise | The 10% calendar-year-loss statement lacks a risk measure, measurement method, and breach rule. |
| S10 | Missing | There is no stated optimization criterion for the pilot, and no sector, ESG, tax, or home-bias preference. |

## Candidate checks

The reserve is $100 million. Twelve months of payouts equal $3 million ($0.75 million × 4), so S3 requires at least **3%** in reserve-eligible cash or daily-liquid government securities.

| Check | A | B | C |
|---|---:|---:|---:|
| Reserve-eligible liquidity for S3 | 14% | 1% | 2% |
| S3: at least 3% reserve-eligible | Pass | Fail | Fail |
| Redeemable within five business days for S8 | 100% | 85% | 100% |
| S8: at least 90% within five days | Pass | Fail | Pass |
| Largest non-exempt single-issuer exposure for S6 | 0% Acme | 5% Acme | 8% Acme |
| S6: no issuer above 8% | Pass | Pass | Pass |
| S5 long-only/no borrowing, shorts, or derivatives | Pass from listed holdings | Pass from listed holdings | Pass from listed holdings |
| S7 turnover at most 25% | Unresolved | Unresolved | Unresolved |
| S2 CPI + 4% net of costs | Unresolved | Unresolved | Unresolved |
| S9 calendar-year-loss limit | Unresolved | Unresolved | Unresolved |

## Conclusion before optimization

Candidate A is the only candidate that meets the two observable liquidity requirements and the issuer limit using the supplied holdings data. No candidate is fully approvable yet: turnover, expected net return versus CPI + 4%, and the undefined calendar-year-loss rule cannot be verified from static portfolio weights.

Before anyone optimizes, the CIO must specify the pilot’s optimization objective and operationalize S9—for example, the risk measure, confidence level or scenario rule, monitoring frequency, and what happens after a breach. The CIO must also say whether S4 is only an evaluation benchmark or creates a tracking-error/relative-risk constraint.

## Investment policy statement

An investment policy statement (IPS) is the governing agreement that translates a client’s purpose, spending needs, return goal, risk tolerance, time horizon, and restrictions into rules for managing and evaluating a portfolio. It works by separating what the portfolio is trying to achieve from the constraints it must obey; the portfolio is then constructed, monitored, and rebalanced against those written terms rather than against a manager’s unstated preferences.

| IPS component | Meridian statements | Meaning for the reserve |
|---|---|---|
| Time horizon and review process | S1 | Seven-year horizon and annual rebalancing set the planning and implementation cycle. |
| Return objective | S2 | Seek CPI + 4% net of costs over rolling five-year periods. |
| Spending and liquidity need | S3 | Fund $0.75 million quarterly and maintain one year of payouts in specified liquid reserve assets. |
| Benchmark and evaluation | S4 | Use the 60% global-equity/40% U.S. investment-grade-bond mix as a reference, but its role in construction is not yet defined. |
| Legal and implementation restrictions | S5, S6, S7, S8 | Long-only; no borrowing, shorts, or derivatives; issuer cap; turnover limit; and redemption-liquidity requirement. |
| Risk tolerance and risk governance | S9 | Intent is to limit annual losses, but the measurement method and breach response are missing. |
| Preferences and decision authority | S10 | No sector, ESG, tax, or home-bias preference is imposed, but the CIO has not identified the pilot’s optimization objective. |

## Reflection

A portfolio can pass every checkable rule and still be wrong for this client because a checklist only tests rules that have been made measurable; it cannot establish that the portfolio can meet the CPI + 4% net objective, is appropriate for the seven-year horizon, or matches the intended loss tolerance. Candidate D demonstrates this: it mechanically passes, but its 97% Treasury-note concentration may be inconsistent with the return objective and exposes the unresolved choice in S10.

The classification I was least certain about was S4. A benchmark is clearly useful for evaluation, but it is not automatically a construction constraint; without an instruction to control tracking error or optimize relative return, I classified its role as missing rather than silently treating it as a hard allocation rule.
