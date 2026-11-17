# Lab 20 — Project 2 Readiness

**Date:** November 17, 2026  
**Project due date:** November 23, 2026

## D — the question

> Could a committee member who has never met me reach my decision from my repository — and does the decision survive one changed input?

## R — current readiness

| Requirement | Current evidence | Status |
|---|---|---|
| Tool | `app.py` opens the Cautious Growth Portfolio dashboard and shows a mandate verdict when a control changes. | Partner cold run passed |
| README | [README.md](README.md) includes setup and the one command to run the app. | Partner cold run passed |
| Visible output | [outputs/visible_output.md](outputs/visible_output.md) shows the base allocation, stress results, and decision. | Published |
| Decision memo | [docs/decision-memo.md](docs/decision-memo.md) states the pilot recommendation, range, risks, and triggers. | Published |
| Validation and AI use | [docs/validation-and-ai-use.md](docs/validation-and-ai-use.md) records sources, checks, limitations, the changed-input run, and the AI-use record. | Published; exact changed value was recorded after the run |
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

> **AI closed from this point until the prediction is committed and pushed.**

At 2:09 PM on November 17, 2026, with AI off, I predict that if the Fallback latest spread (%) is increased above the median, there will be an error. The old value is 0.84%, and the median is 0.84%. I predict that the window stress moves an allocation by 25 points or more.

### Test result — 2:24 PM

I entered a Fallback latest spread of 0.87% and a Fallback trailing median of 0.86%. The app showed: “REVIEW LQD: the point-in-time corporate spread is above its trailing median. This flag triggers a committee review, not an automatic trade.” The result was a committee-review alert rather than a technical error or an automatic allocation change.

## Explain the code

The decision-number function is `search_project2_mix()` in [portfolio.py](portfolio.py). It tries
long-only allocations in five-point steps, rejects any mix above the maximum ETF weight or below
the BIL minimum/net-return target, then keeps the feasible mix with the lowest volatility.

Line by line, the function first checks that the correlations are valid and that BIL is included in
the data. It confirms that the five-point grid divides 100% exactly, then creates the list of ETF
names, the number of grid units, and an empty `best` result. The nested `try_allocations()`
function assigns each possible five-point weight. At the final ETF, it gives that ETF every
remaining grid unit so the weights sum to 100%. It rejects a weight above the maximum, evaluates
the mandate, rejects a portfolio that misses the return target or BIL minimum, and replaces
`best` only when a feasible result has lower volatility. The final line begins the search and
returns the best feasible portfolio, or `None` when no portfolio qualifies.

### Partner question and answer

- Partner question: No specific question was recorded during the explanation.
- My answer from the code: If no five-point allocation passes every required rule, `best` stays `None`, so the function returns `None` instead of making up a portfolio.

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

- Lab 20 record: [Lab 20.md](https://github.com/catiemoe-cloud/TICKER-research/blob/main/project-2/Lab%2020.md)
- App: [app.py](https://github.com/catiemoe-cloud/TICKER-research/blob/main/project-2/app.py)
- Portfolio logic: [portfolio.py](https://github.com/catiemoe-cloud/TICKER-research/blob/main/project-2/portfolio.py)
- README: [README.md](https://github.com/catiemoe-cloud/TICKER-research/blob/main/project-2/README.md)
- Decision memo: [decision-memo.md](https://github.com/catiemoe-cloud/TICKER-research/blob/main/project-2/docs/decision-memo.md)
- Validation record: [validation-and-ai-use.md](https://github.com/catiemoe-cloud/TICKER-research/blob/main/project-2/docs/validation-and-ai-use.md)
- Visible output: [visible_output.md](https://github.com/catiemoe-cloud/TICKER-research/blob/main/project-2/outputs/visible_output.md)
