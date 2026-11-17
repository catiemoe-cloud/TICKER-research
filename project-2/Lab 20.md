# Lab 20 — Project 2 Readiness

**Date:** November 17, 2026  
**Project due date:** November 23, 2026

## D — the question

> Could a committee member who has never met me reach my decision from my repository — and does the decision survive one changed input?

## R — current readiness

| Requirement | Current evidence | Status |
|---|---|---|
| Tool | `app.py` opens the Cautious Growth Portfolio dashboard. | Ready locally |
| README | [README.md](README.md) includes setup and the one command to run the app. | Partner cold run passed |
| Visible output | [outputs/visible_output.md](outputs/visible_output.md) shows the base allocation, stress results, and decision. | Ready locally |
| Decision memo | [docs/decision-memo.md](docs/decision-memo.md) states the pilot recommendation, range, risks, and triggers. | Draft ready locally |
| Validation and AI use | [docs/validation-and-ai-use.md](docs/validation-and-ai-use.md) records sources, checks, limitations, and the AI-use record. | Needs the AI-closed Changed-Input Record |
| Videos and transcripts | Not recorded yet. | Not started |
| GitHub | Current files are published in the Project 2 repository. | Complete |

## Current committee decision

**Pilot** a cautious-growth portfolio in the range of 55–65% BIL and 35–45% ACWI. Pause or review the pilot if the data-window stress moves an allocation by 25 points or more, the portfolio misses the return target, or the credit-spread monitor flags LQD.

## I — partner cold run

**Instructions for my partner:** I will send only my Project 2 GitHub repository link. My partner will use the README alone, without coaching, and record:

- Command used:
- First failure, or `no failure`:
- Elapsed time:
- Where the committee decision/output appeared:

### Partner cold-run record

- Command used: `python3 -m venv .venv`, `source .venv/bin/activate`, `pip install -r requirements.txt`, then `streamlit run app.py`.
- First failure, or `no failure`: No failure.
- Elapsed time: About one minute.
- Where the result appeared: The Streamlit Project 2 dashboard in the browser, including the committee decision and portfolio comparison.
- Fix made, or why no fix was needed: No fix was needed because the app ran successfully from the README instructions.
- Commit/push after fix (if applicable): Not applicable; the clean cold run was completed from the GitHub repository.

## V — Locked Changed-Input Record

> **AI closed from this point until the prediction is committed and pushed.**At 2:09 PM on November 17, 2026, with AI off, I predict that if the Fallback latest spread (%) is increased above the median, there will be an error. The old value is 0.84%, and the median is 0.84%. I predict that the window stress moves an allocation by 25 points or more.

### Test result — 2:24 PM

I entered a Fallback latest spread of 0.87% and a Fallback trailing median of 0.86%. The app showed: “REVIEW LQD: the point-in-time corporate spread is above its trailing median. This flag triggers a committee review, not an automatic trade.” The result was a committee-review alert rather than a technical error or an automatic allocation change.

## Explain the code

The decision-number function is `search_project2_mix()` in [portfolio.py](portfolio.py). It tries
long-only allocations in five-point steps, rejects any mix above the maximum ETF weight or below
the BIL minimum/net-return target, then keeps the feasible mix with the lowest volatility.

### Partner question and answer

_Complete after explaining the function line by line without AI._

- Partner question:
- My answer from the code:

## E — fix one thing

- First issue found: No issue was found during the partner cold run.
- Repair made: No repair was needed.
- Rerun result: The partner completed a clean run from the README in about one minute.

## Decision line

**Pilot** the BIL/ACWI allocation only with quarterly monitoring; reverse or pause the process if the window stress moves an allocation by 25 points or more, the net-return target fails, or the corporate-spread monitor requires review.

## Reflect

1. The cold run showed that the README gives a new user enough information to create the environment, install the requirements, and open the dashboard without needing help from me.
2. Before the deadline, I will not change the stated mandate, decision rules, or the committed Changed-Input Record after I complete it; I will only make documented fixes if testing identifies a real problem.

## Checkout links

_Add the GitHub links after the current Project 2 work is pushed._

- Lab 20 record:
- App:
- Portfolio logic:
- README:
- Decision memo:
- Validation record:
- Visible output:
