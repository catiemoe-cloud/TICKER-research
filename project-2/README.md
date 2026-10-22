# Project 2 — Investment Management Application

Current work for Project 2, which opens in Week 9, is organized here. The earlier Apple corporate-finance work and its historical labs are retained in `../project-1/`.

## Meridian mandate and portfolio labs

- [mandate.py](mandate.py) — runnable Meridian Foundation Reserve checker.
- [meridian_foundation_reserve.md](meridian_foundation_reserve.md) — requirement sorting, IPS mapping, candidate analysis, and reflection.
- [meridian_checker_notes.md](meridian_checker_notes.md) — validation, stress test, Candidate D judgment, and CIO question.

Run the checker from this folder with:

```bash
python3 mandate.py
```

## Portfolio return and risk lab

- [portfolio.py](portfolio.py) — course-input engine for the benchmark, equal-weight, and inverse-volatility portfolios.
- [Lab 14.md](Lab%2014.md) — inputs, results, mandate interpretation, and correlation stress test.
- [Lab 15.md](Lab%2015.md) — fund universe, numeric objective, and hard constraint.
- [prices.csv](prices.csv) — five years of monthly adjusted-close prices for the Lab 15 ETF universe.

Run it from this folder with:

```bash
python3 portfolio.py
```

## Lab 15 client page

- [app.py](app.py) — Streamlit client page. It searches every long-only mix in 5-percentage-point steps, retaining the lowest-volatility mix that meets the selected return and eligible-liquidity requirements.

Run it from this folder in the Python environment where Streamlit is installed:

```bash
streamlit run app.py
```

The page starts with the Meridian course assumptions, then lets the client switch to the Project 2 ETF universe calculated from `prices.csv`. Historical ETF estimates are clearly labeled as historical estimates, not forecasts.

## Current contents

- `mandate.py`, `meridian_foundation_reserve.md`, and `meridian_checker_notes.md` — mandate interpretation and candidate checks.
- `portfolio.py` and `Lab 14.md` — expected return, risk, and mandate analysis.
- `prices.csv` and `Lab 15.md` — ETF universe and the historical price data for the next portfolio-design step.
