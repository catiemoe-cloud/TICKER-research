# Project 2 — Visible Executed Output

Built with AI help for coding, research organization, and debugging; the analysis and decision are mine.  
Education, not investment advice.

## Base decision

**Tentative action:** Pilot.  
**Pilot range:** 55–65% BIL and 35–45% ACWI.  
**Price-data boundary:** 59 monthly returns from November 2021 through September 2026.  
**As-of rule:** The live app uses the selected ALFRED vintage for the `BAMLC0A0CM` credit monitor.

## Constrained portfolio

| ETF | Weight |
|---|---:|
| BIL | 60.00% |
| IEF | 0.00% |
| LQD | 0.00% |
| ACWI | 40.00% |

| Measure | Result |
|---|---:|
| Historical net return estimate | 6.69% |
| Annualized volatility | 6.03% |
| BIL minimum | pass: 60.00% is at least 10.00% |
| Maximum ETF weight | pass: 60.00% is below 70.00% |
| Long-only and full allocation | pass |

## Stress results

| Scenario | BIL | IEF | LQD | ACWI | Net return estimate | Volatility |
|---|---:|---:|---:|---:|---:|---:|
| Base case | 60.00% | 0.00% | 0.00% | 40.00% | 6.69% | 6.03% |
| ACWI return estimate −1 point | 55.00% | 0.00% | 0.00% | 45.00% | 6.62% | 6.77% |
| Latest 36 monthly returns | 70.00% | 15.00% | 0.00% | 15.00% | 6.59% | 2.44% |
| 50-basis-point annual cost drag | 55.00% | 0.00% | 0.00% | 45.00% | 6.57% | 6.77% |
| BIL minimum raised to 20% | 60.00% | 0.00% | 0.00% | 40.00% | 6.69% | 6.03% |

## Committee condition

The latest-36-month window moves ACWI from 40.00% to 15.00%, a 25-point change. This reaches
the review trigger. The committee should keep the recommendation as a monitored pilot, not treat
the base allocation as permanently stable.
