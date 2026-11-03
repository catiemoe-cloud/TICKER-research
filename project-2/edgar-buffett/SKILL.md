---
name: edgar-buffett
description: Retrieve five annual 10-K financial histories from SEC EDGAR and write a Buffett-style business memo when the user asks to assess a U.S. company without price data.
---

Use this skill for a ticker-based, Buffett-style business-quality review using only SEC EDGAR company facts. Do not use FAskills, paid services, estimates, price data, or non-10-K filings.

1. Run `scripts/edgar_financials.py TICKER --json-output PATH`. Set `SEC_EDGAR_USER_AGENT` to a contact string before running it; do not save a personal email in the workspace.
2. Treat the script output as the sole numerical source. It selects the five latest fiscal-year ends from 10-K facts, with the latest filing winning when facts share an end date.
3. Write `reports/TICKER_buffett_memo.md`. Make an **Own the business**, **Watch it**, or **Pass** judgment about the business—not its stock price. Use only numbers the script printed and identify uncertainty as `not found` or `not known`; do not add forecasts, estimates, or prices.
4. Run `streamlit run lab18_app.py` from the Project 2 directory to review the history, checks, memo, and memo-number audit.

The script prints revenue, net income, operating cash flow, capital spending, equity, ROE, and owner earnings with each XBRL tag. Its three deterministic checks are ROE at least 15% every year, positive owner earnings every year, and owner-earnings growth from first year to last.
