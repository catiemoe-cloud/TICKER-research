# Validation and AI Use Record

Built with AI help for coding, research organization, and debugging; the analysis and decision are mine.  
Education, not investment advice.

## Sources and as-of boundary

| Input | Source | Boundary / check |
|---|---|---|
| BIL, IEF, LQD, ACWI prices | Yahoo Finance monthly adjusted-close download in `prices.csv` | Downloaded October 22, 2026; input includes October 2021–September 2026 prices. Historical returns are estimates. |
| Corporate-spread signal | [FRED BAMLC0A0CM](https://fred.stlouisfed.org/series/BAMLC0A0CM), sourced by FRED from Ice Data Indices, LLC, and ALFRED vintage | Daily percent series, not seasonally adjusted. The October 28, 2026 observation was updated October 29, indicating roughly next-business-day availability. FRED warns values can be revised; use only the ALFRED vintage available on the selected decision date. Download/vintage check: October 29, 2026. |
| Portfolio calculations | `portfolio.py` | Return = arithmetic monthly mean × 12; volatility = sample monthly standard deviation × square root of 12; weights are searched in 5-point steps. |

## Checks completed

| Check | Result | Evidence |
|---|---|---|
| Course engine check | Portfolio calculation functions compile and base case returns 60% BIL / 40% ACWI. | `portfolio.py`, `prices.csv`, `outputs/visible_output.md` |
| Base-case mandate | Constrained portfolio passes the stated rules. | App mandate table and visible output |
| Baseline comparison | Equal weight and 60/40 benchmark are evaluated against the same rules. | App comparison and baseline-gap table |
| Estimate stress | Reducing ACWI's return estimate by 1 point changes the allocation to 55% BIL / 45% ACWI. | App stress table |
| Window stress | Latest 36 monthly returns change the mix to 70% BIL / 15% IEF / 15% ACWI. | App stress table |
| Cost stress | The app applies a 50-basis-point annual portfolio cost drag. | App stress table |
| Constraint stress | The app increases the BIL minimum from 10% to 20%. | App stress table |
| Boundary-condition check | A 70.00% BIL result passes the “no ETF above 70%” limit; tolerance prevents a floating-point representation of 70% from becoming a false failure. | `portfolio.py`, 36-month window result |
| Point-in-time monitor | App requests the selected ALFRED vintage and displays source/date/fallback status. | `app.py`; inspect live app output before submission |
| Partner cold run | A partner followed the GitHub README without coaching; the app opened with no failure in about one minute. | `Lab 20.md` |

## Limitations and monitoring

- Historical estimates are not forecasts.
- The five-point allocation grid can miss a better allocation between grid points.
- The credit-spread signal is a review flag, not an automatic trading rule.
- A committee must still judge implementation costs, taxes, suitability, market conditions, and any data-download failure.

## Material AI-use record

| Date | Tool/model/version | Task or material output | My disposition | Independent check and resulting use |
|---|---|---|---|---|
| November 2026 | Codex — GPT-5.6-Terra (medium) | Helped organize the app structure, implement portfolio-display features, and identify validation items. | Modified and accepted after review. | I compiled `portfolio.py` and `app.py`, checked the base/window portfolio outputs, and retained the limits and explanations in this file. |
| November 2026 | Codex — GPT-5.6-Terra (medium) | Helped draft documentation language. | Modified. | I must review every number, source, and recommendation against the app before submission. |

## Locked Changed-Input Record — complete this section with AI closed

> **Stop here before the final changed-input run.** This prediction must be written by me with AI
> closed, committed and pushed to GitHub before I execute the selected change. Do not replace this
> placeholder with AI-written text.

### Before execution — student-authored prediction

- Timestamp: November 17, 2026, 2:09 PM.
- Repository commit evidence: `6292a2a` (prediction recorded in `Lab 20.md` and pushed after the reported 2:15 PM run).
- Exact input changed and units: Fallback latest spread (%).
- Old value: 0.84%.
- New value: Increased above the 0.84% median; the exact entered value was not recorded.
- Expected direction of return, volatility, and weights: I predicted that the window stress would move an allocation by 25 points or more.
- Expected effect on the pilot/reject/hold decision: I predicted there would be an error if the fallback latest spread was increased above the median.
- Why this is a load-bearing input: The corporate-spread input is the point-in-time credit-monitoring signal for LQD.

### After execution — complete after the committed run

- Command/run used: Streamlit Project 2 app, run at 2:24 PM on November 17, 2026.
- Before output location: Project 2 Streamlit dashboard with fallback latest spread of 0.84% and fallback trailing median of 0.84%.
- After output location: Project 2 Streamlit dashboard with fallback latest spread of 0.87% and fallback trailing median of 0.86%.
- Actual direction of return, volatility, and weights: No return, volatility, or allocation change was recorded for this signal-only test.
- Actual decision effect: The app displayed: “REVIEW LQD: the point-in-time corporate spread is above its trailing median. This flag triggers a committee review, not an automatic trade.”
- Did the result match the prediction? Why or why not? Partly. The above-median spread produced a review alert, not a technical error; this test did not show a 25-point allocation movement from the window stress.
- Failure diagnosis or explanation if nothing changed: The changed inputs are a credit-monitoring signal. They trigger review status but do not automatically recalculate or trade the portfolio allocation.

## Corrected Locked Changed-Input Record

### Before execution — student-authored prediction

- Timestamp: 9:22 PM, November 23, 2026
- Starting repository commit: `ac13744161efc5391c41c662375cc6561c92303e`
- Exact input changed and units: Estimation window under Selected stress view, measured in monthly return observations. Kept the annual portfolio cost at 0 basis points.
- Old value: All 59 monthly returns, November 2021 through September 2026.
- New value: Latest 36 monthly returns, October 2023 through September 2026.
- Expected numeric change in return: The constrained portfolio’s estimated annual net return falls from 6.69% to 6.59%, a decrease of 0.10 percentage points.
- Expected numeric change in volatility: Estimated annualized volatility falls from 6.03% to 2.44%, a decrease of 3.59 percentage points.
- Expected numeric change in weights: BIL rises from 60% to 70% (+10 percentage points), IEF rises from 0% to 15% (+15 points), LQD stays at 0%, and ACWI falls from 40% to 15% (−25 points).
- Expected pilot/review/reject decision effect: Committee Review. The stressed portfolio still passes the 6.50% net return requirement, and the 25-point drop in ACWI hits the app’s review trigger.
- Why this is the highest-risk input: Chose the estimation window because it changes the historical data used to estimate both returns and risk. In the displayed stress tests, it produces the largest allocation shift. The estimated return changes by only 0.10 percentage points, while the recommended equity weight drops from 40% to 15%. That makes the pilot allocation sensitive to which months the model uses.

### After execution — student-reported result

- Before-output location: Section 07, Selected interactive view, in the Constrained portfolio row. The window was November 2021 through September 2026, with annual cost set to 0 basis points. Before screenshot: 9:21:45 PM.
- After-output location: Section 07, Selected interactive view, in the Constrained portfolio row. The window was October 2023 through September 2026, with annual cost still at 0 basis points. After screenshot: 9:27:45 PM. The full ETF weights are in Section 04, Required stress scenarios, in the Window stress row of screenshot 9:27:40 PM.
- Actual return, volatility, and weight changes: Estimated annual net return fell from 6.69% to 6.59% (−0.10 percentage points). Annualized volatility fell from 6.03% to 2.44% (−3.59 percentage points). BIL rose from 60% to 70% (+10 points), IEF rose from 0% to 15% (+15 points), LQD stayed at 0%, and ACWI fell from 40% to 15% (−25 points).
- Actual decision effect: The 36-month portfolio passed the 6.50% net return requirement. The Action today card continued to show COMMITTEE REVIEW because the 25-point drop in ACWI met the review threshold. The tentative recommendation at the top continued to show PILOT.
- Did it match my prediction? Why or why not?: Yes. The return, volatility, and weight changes matched the 36-month stress results used to make the prediction. The portfolio still met the mandate, and the ACWI shift was large enough to require committee review.
- Failure diagnosis if it did not match: N/A.
