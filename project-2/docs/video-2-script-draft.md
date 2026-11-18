# Video 2 Script Draft — Technical Walkthrough

**Maximum length:** 5:00
**Before recording:** Rehearse from this outline, but explain the code in your own words. Show the named files and live app as you speak.

## Opening — 0:00–0:15

“I used Codex for coding, research organization, debugging, and document drafting. The analysis and committee decision are mine. Education, not investment advice.”

“This is the technical walkthrough of my Cautious Growth Portfolio app.”

## Repository and data flow — 0:15–1:20

Show `README.md`, `app.py`, `portfolio.py`, `prices.csv`, `outputs/visible_output.md`, and the two files in `docs/`.

“A clean user follows the README commands to create the environment, install Streamlit, and run `streamlit run app.py`. My partner completed that cold run from the README in about one minute with no failure.”

“`prices.csv` contains monthly adjusted-close prices for BIL, IEF, LQD, and ACWI. `portfolio.py` converts prices to monthly returns, calculates annual return estimates, annualized volatility, and correlations. The app uses those results for every portfolio so the comparison uses the same inputs.”

## Decision-number logic — 1:20–2:35

Open `search_project2_mix()` in `portfolio.py`.

“This function searches long-only weights in five-point steps. It checks that BIL exists and that the grid divides 100% exactly. It tries each feasible allocation, rejects weights above the 70% maximum, evaluates the mandate, rejects mixes that miss the 6.5% return target or 10% BIL minimum, and keeps the feasible mix with the lowest volatility. If nothing qualifies, it returns `None` instead of inventing a portfolio.”

## App results and validation — 2:35–4:05

Show the comparison table, the allocation/return charts, the stress table, and the point-in-time signal card.

“The app compares equal weight, the 60% ACWI / 40% LQD benchmark, and the constrained portfolio. It also displays which mandate rules pass or fail. The base constrained result is 60% BIL and 40% ACWI. The required stresses change the return estimate, time window, cost, and BIL constraint.”

“For the credit-monitoring test, I changed the fallback latest spread from 0.84% to 0.87% and the trailing median to 0.86%. The app correctly displayed an LQD committee-review message. This is intentionally not an automatic trade rule, so it did not automatically change the portfolio weights.”

## Limitation and closing — 4:05–5:00

“The main limitation is that historical return estimates are not forecasts, and the five-point search can miss a better allocation between grid points. The app makes those limits visible instead of hiding them. The validation record documents the sources, stress tests, limitations, and changed-input evidence.”
