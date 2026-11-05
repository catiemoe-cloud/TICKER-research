---
name: edgar-graham
description: Apply Graham-style balance-sheet and earnings screens to five annual 10-K histories from SEC EDGAR when a user requests a no-price business review.
---

Use this skill for a Graham panel memo based only on the shared SEC EDGAR facts engine. Do not use FAskills data, price data, or estimates.

1. Run the bundled `scripts/edgar_financials.py TICKER --json-output PATH` with `SEC_EDGAR_USER_AGENT` set for the terminal session.
2. Use only printed numbers. Apply the code’s Graham checks: latest current ratio at least 1.0, net income positive every year, and net income growth from first to last year.
3. Write `reports/TICKER_graham_memo.md` with a **Own the business**, **Watch it**, or **Pass** verdict about the business; state missing data as `not found` or `not known` and use no price data.
