---
name: edgar-burry
description: Apply Burry-style cash-quality and leverage screens to five annual 10-K histories from SEC EDGAR when a user requests a forensic no-price business review.
---

Use this skill for a Burry panel memo based only on the shared SEC EDGAR facts engine. Do not use FAskills data, price data, or estimates.

1. Run the bundled `scripts/edgar_financials.py TICKER --json-output PATH` with `SEC_EDGAR_USER_AGENT` set for the terminal session.
2. Use only printed numbers. Apply the code’s Burry checks: operating cash flow at least net income every year, and latest liabilities no more than twice equity.
3. Write `reports/TICKER_burry_memo.md` with a **Own the business**, **Watch it**, or **Pass** verdict about the business; state missing data as `not found` or `not known` and use no price data.
