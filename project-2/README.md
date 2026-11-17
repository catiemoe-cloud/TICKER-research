# Project 2 — Cautious Growth Portfolio

Built with AI help for coding, research organization, and debugging; the analysis and decision are mine.  
Education, not investment advice.

## Committee decision

This project recommends a **monitored pilot**, not immediate full adoption. The pilot range is
55–65% BIL and 35–45% ACWI. The process pauses for committee review if a data-window stress
moves a recommended allocation by 25 percentage points or more, if the portfolio misses the net
return target, or if the point-in-time corporate-spread monitor flags LQD.

The intended user is a cautious investor who still wants growth but needs substantial liquidity.
The app compares three portfolios under the same mandate:

1. Equal weight across BIL, IEF, LQD, and ACWI.
2. A transparent 60% ACWI / 40% LQD benchmark.
3. A constrained, lowest-volatility portfolio found by the project engine.

## Mandate

- **Universe:** BIL, IEF, LQD, and ACWI.
- **Objective:** historical net annual return estimate of at least 6.5%.
- **Risk measure:** annualized volatility calculated from monthly adjusted-close returns.
- **Hard limits:** long-only; BIL at least 10%; no ETF above 70%; allocations sum to 100%.
- **Rebalancing:** quarterly, with a 5-percentage-point target band.
- **Benchmark:** 60% ACWI / 40% LQD.
- **Signal:** `BAMLC0A0CM`, the ICE BofA U.S. Corporate Index Option-Adjusted Spread, used only as a point-in-time LQD monitoring flag.

## Run the app

From the repository's `project-2` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The default app reads `prices.csv`. It can also accept a replacement CSV with a date column first
and exactly four ticker columns: `BIL`, `IEF`, `LQD`, and `ACWI`.

## What the app shows

- A decision panel with the action, allocation range, and reversal trigger.
- Point-in-time FRED/ALFRED corporate-spread governance data, with a clear fallback if a download fails.
- Equal-weight, 60/40 benchmark, and constrained portfolio results side by side.
- Pass/fail mandate checks and an explanation of why the baselines differ from the constrained portfolio.
- Required estimate, window, cost, and constraint stress scenarios.
- An original allocation-robustness map across return targets and time windows.
- An original rebalancing action card: hold, rebalance, or committee review.
- A download button that creates a readable visible-output Markdown artifact.

## Data sources and dates

- ETF prices: `prices.csv`, Yahoo Finance monthly adjusted-close data, downloaded October 22,
  2026; observations run from October 2021 through September 2026. Historical returns are
  estimates, not forecasts.
- Credit signal: [FRED BAMLC0A0CM](https://fred.stlouisfed.org/series/BAMLC0A0CM) and the matching
  ALFRED vintage. The app uses the vintage available on the selected decision date rather than
  later observations or revisions.
- The default signal as-of date is September 30, 2026. Change it in the sidebar only when the
  decision date changes and preserve the resulting visible output.

## Repository map

- `app.py` — final Streamlit committee dashboard.
- `portfolio.py` — reusable portfolio math, mandate checks, and constrained search.
- `prices.csv` — project ETF price input.
- `asof.py` and `asof_app.py` — Lab 16/17 point-in-time prototype and reference implementation.
- `docs/decision-memo.md` — written committee recommendation.
- `docs/validation-and-ai-use.md` — sources, tests, limitations, AI-use record, and Locked Changed-Input Record.
- `outputs/visible_output.md` — current readable executed-output artifact.
- `PROJECT2_PLAN.md` — complete build and submission timeline.

## Known limitations

- The allocation search uses five-percentage-point steps, so it does not optimize between grid points.
- Historical arithmetic-mean returns and historical volatility are estimates, not forecasts.
- The cost scenario uses a simplified portfolio-level annual return drag.
- The corporate-spread signal is a monitoring input, not a forecast or automatic trade rule.
- The model does not establish taxes, individual suitability, trading capacity, or future market returns.

## Reproducibility and validation

See [the validation record](docs/validation-and-ai-use.md) for tests, sources, limitations, and
the required Locked Changed-Input Record. The human-authored prediction in that record must be
completed with AI closed and committed before its final changed-input run.
