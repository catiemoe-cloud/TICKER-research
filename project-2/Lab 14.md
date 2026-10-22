# Lab 14 — Meridian Portfolio Return, Risk, and Mandate Check

**Date:** October 20, 2026  
**Files:** [mandate.py](mandate.py) and [portfolio.py](portfolio.py)

## 1. Rerun the Meridian mandate checker

Command used:

```bash
python3 mandate.py
```

The checker reproduced the known result: the reserve minimum is **3.0%** of the portfolio. Candidate A passes every checkable rule; B fails three rules (reserve, five-day liquidity, and Acme issuer exposure); C fails the reserve rule; and D passes every checkable rule. The calendar-year-loss statement remains **“requires CIO clarification”** because S9 does not define a measurement method or breach rule.

## 2. Question and boundary

**Question:** What return and risk do the three simple portfolios have, and can any meet the Meridian mandate?

The analysis uses only the course-authored training inputs below, not market estimates. Expected return and risk are calculated for four sleeves; the result does not establish that a portfolio satisfies every Meridian requirement because S9 and the CIO's optimization instruction in S10 remain unresolved.

## 3. Inputs and calculation method

The return objective is **6.5%**, calculated as CPI estimated at 2.5% plus 4.0%. Bills and the Treasury 10-year note are reserve-eligible.

| Sleeve | Expected return | Volatility |
|---|---:|---:|
| Treasury bills | 3.5% | 0.5% |
| Treasury 10-year note | 4.3% | 7.0% |
| Investment-grade bond fund | 5.0% | 6.0% |
| Global equity index fund | 8.0% | 16.0% |

The covariance for each pair is calculated as:

```text
covariance(i, j) = correlation(i, j) × volatility(i) × volatility(j)
```

Portfolio expected return is the weighted average of sleeve expected returns. Portfolio volatility is the square root of the weighted covariance matrix, `sqrt(w'Σw)`. The program refuses to calculate if a correlation is outside −1 to 1 or if the correlation table is not symmetric.

The three portfolios are:

- **Benchmark:** 40% investment-grade bonds and 60% global equity, matching S4.
- **Equal weight:** 25% in each sleeve.
- **Inverse volatility:** each sleeve weight is proportional to `1 ÷ volatility`, scaled to 100%.

## 4. Known-answer results

Command used:

```bash
python3 portfolio.py
```

| Portfolio | Weights: bills / 10-year / IG / equity | Expected return | Volatility | Reserve-eligible | Meets 6.5%? |
|---|---|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | No |

Every value matched the known answer. Including the correlation term matters: omitting it would incorrectly produce a 9.90% benchmark volatility rather than 10.46%.

## 5. Correlation stress test

For a temporary test, the investment-grade-bond/equity correlation was changed from **0.25 to 0.50** in both symmetric cells. The benchmark volatility rose to **11.00%**, matching the expected result. The two cells were then restored to **0.25**, and the rerun restored the benchmark volatility to **10.46%**.

This test shows why diversification risk depends on covariance, not just the standalone volatility of each sleeve. A higher positive relationship between bond-fund and equity returns reduces the diversification benefit and raises total portfolio risk.

## 6. Meridian mandate interpretation

| Portfolio | What it meets | Limitation |
|---|---|---|
| Benchmark | Meets the 6.5% expected-return objective. All listed sleeves are within the five-business-day redemption window and issuer-exempt. | Has 0.0% reserve-eligible assets, so it fails the 3.0% payout reserve requirement. |
| Equal weight | Meets the 3.0% reserve requirement with 50.0% reserve-eligible assets; it also satisfies the observable liquidity and issuer conditions. | Its 5.20% expected return is below the 6.5% objective. |
| Inverse volatility | Meets the 3.0% reserve requirement with 90.3% reserve-eligible assets; it also satisfies the observable liquidity and issuer conditions. | Its 3.77% expected return is below the 6.5% objective. |

No portfolio can yet be confirmed to meet the full mandate. S9's calendar-year-loss rule is not measurable as written, and S10 does not say what the CIO wants the pilot to optimize. Those missing decisions determine whether the trade-off between expected return, risk, and liquidity is suitable for Meridian.

## 7. Conclusion

The benchmark is the only simple portfolio that meets the 6.5% expected-return target, but it fails the required reserve allocation. Equal weight and inverse volatility meet the mechanical reserve requirement but miss the return objective. Before optimizing a new portfolio, the CIO must define the loss measurement and breach response for S9 and state the portfolio's optimization criterion under S10.
