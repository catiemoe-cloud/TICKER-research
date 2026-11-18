# Decision Memo — Cautious Growth Portfolio

Built with AI help for coding, research organization, and debugging; the analysis and decision are mine.  
Education, not investment advice.

## Recommendation and committee ask

I recommend a **monitored pilot** rather than full adoption. The committee should authorize a
pilot allocation range of 55–65% BIL and 35–45% ACWI, with quarterly review. The committee should
not add LQD or IEF until it agrees on how the corporate-spread monitor will be used in review.

## Evidence

The base case uses 59 monthly ETF returns from November 2021 through September 2026. The
constrained portfolio is 60% BIL and 40% ACWI. It has a 6.69% historical net return estimate and
6.03% annualized volatility before the simplified cost stress. It passes the long-only, 10% BIL,
70% maximum-ETF, full-allocation, and 6.5% net-return rules.

The equal-weight portfolio and the 60% ACWI / 40% LQD benchmark are shown beside the constrained
portfolio in the app. Their mandate verdicts make the tradeoff visible instead of assuming that a
familiar benchmark automatically fits this client.

## Sensitivity and risks

The model is sensitive to the estimation window. Using the latest 36 monthly returns produces a
70% BIL / 15% IEF / 15% ACWI constrained portfolio, instead of the 60% BIL / 40% ACWI base case.
ACWI moves by 25 percentage points, which reaches the committee-review trigger. A one-percentage-
point reduction in the ACWI return estimate changes the mix to 55% BIL / 45% ACWI and increases
estimated volatility to 6.77%.

The app also runs a 50-basis-point annual cost stress and a tighter 20% BIL constraint. These are
scenario results, not forecasts. The model uses historical arithmetic-mean returns, a five-point
allocation grid, and ETF prices; it does not establish future returns, taxes, or investor
suitability.

## Monitoring and reversal triggers

- Review the portfolio quarterly and rebalance if an allocation moves outside its 5-point band.
- Review LQD if the point-in-time `BAMLC0A0CM` credit spread is above its trailing 12-month median.
- Pause or reverse the pilot if the latest-36-month window moves any recommended allocation by
  25 percentage points or more versus the all-history base window, if the portfolio no longer
  reaches the net-return target, or if the signal-data process cannot confirm that a value was
  available on the decision date.

## AI disclosure and validation

The named AI-use record, data sources, point-in-time rule, tests, and Locked Changed-Input Record
are in [validation-and-ai-use.md](validation-and-ai-use.md). The change record is the controlling
evidence for the final stress test.
