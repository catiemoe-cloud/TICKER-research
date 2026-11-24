# Video 2 Script Draft — Technical Walkthrough

**Maximum length:** 5:00
**Webcam:** Keep your face visible in a small frame throughout the recording.
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

“Beyond the required comparison, I added a baseline-gap table that explains the return, volatility, BIL, and failed-rule differences between the recommended portfolio and each baseline. I also added an allocation robustness map across return targets and estimation windows.”

“My highest-risk financial test is the estimation-window stress. Before running it, I wrote an AI-off numeric prediction and committed it to GitHub. I changed the Selected stress view from all 59 monthly returns to the latest 36 monthly returns, while keeping annual cost at zero basis points.”

“The constrained mix changed to 70% BIL, 15% IEF, 0% LQD, and 15% ACWI. Its net return estimate fell from 6.69% to 6.59% and volatility fell from 6.03% to 2.44%. ACWI moved from 40% to 15%, a 25-point move that reaches the committee-review trigger. The portfolio still passed the 6.50% net-return requirement, the Action today card remained Committee Review, and the tentative recommendation remained Pilot.”

“For implementation, the rebalancing action card compares current weights with the constrained target. It returns hold, rebalance, or committee review rather than pretending the app can trade automatically. As a separate signal-governance check, entering a fallback latest spread of 0.87% against a 0.86% trailing median displays an LQD committee-review message. This is intentionally not an automatic trade rule, so it does not automatically change portfolio weights.”

## Limitation and closing — 4:05–5:00

“The main limitation is that historical return estimates are not forecasts, and the five-point search can miss a better allocation between grid points. The app makes those limits visible instead of hiding them. The validation record documents the sources, stress tests, limitations, and changed-input evidence.”
