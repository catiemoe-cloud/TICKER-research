# Lab 20 — Project 2 Readiness

**Date:** November 17, 2026  
**Project due date:** November 23, 2026

## D — the question

> Could a committee member who has never met me reach my decision from my repository — and does the decision survive one changed input?

## R — current readiness

| Requirement | Current evidence | Status |
|---|---|---|
| Tool | `app.py` opens the Cautious Growth Portfolio dashboard. | Ready locally |
| README | [README.md](README.md) includes setup and the one command to run the app. | Ready locally |
| Visible output | [outputs/visible_output.md](outputs/visible_output.md) shows the base allocation, stress results, and decision. | Ready locally |
| Decision memo | [docs/decision-memo.md](docs/decision-memo.md) states the pilot recommendation, range, risks, and triggers. | Draft ready locally |
| Validation and AI use | [docs/validation-and-ai-use.md](docs/validation-and-ai-use.md) records sources, checks, limitations, and the AI-use record. | Needs the AI-closed Changed-Input Record |
| Videos and transcripts | Not recorded yet. | Not started |
| GitHub | Current files must be pushed before the partner cold run. | Not complete |

## Current committee decision

**Pilot** a cautious-growth portfolio in the range of 55–65% BIL and 35–45% ACWI. Pause or review the pilot if the data-window stress moves an allocation by 25 points or more, the portfolio misses the return target, or the credit-spread monitor flags LQD.

## I — partner cold run

**Instructions for my partner:** I will send only my Project 2 GitHub repository link. My partner will use the README alone, without coaching, and record:

- Command used:
- First failure, or `no failure`:
- Elapsed time:
- Where the committee decision/output appeared:

### Partner cold-run record

_Complete after my partner runs the repository from the GitHub README._

- Command used:
- First failure, or `no failure`:
- Elapsed time:
- Where the result appeared:
- Fix made, or why no fix was needed:
- Commit/push after fix (if applicable):

## V — Locked Changed-Input Record

> **AI closed from this point until the prediction is committed and pushed.** I must write the
> prediction myself in `docs/validation-and-ai-use.md` before running the change. I will record
> the exact old/new input, units, expected direction, expected decision effect, timestamp, and
> commit hash. After the run, I will add before/after output and explain the actual result.

## Explain the code

The decision-number function is `search_project2_mix()` in [portfolio.py](portfolio.py). It tries
long-only allocations in five-point steps, rejects any mix above the maximum ETF weight or below
the BIL minimum/net-return target, then keeps the feasible mix with the lowest volatility.

### Partner question and answer

_Complete after explaining the function line by line without AI._

- Partner question:
- My answer from the code:

## E — fix one thing

_Complete after the cold run._

- First issue found:
- Repair made:
- Rerun result:

## Decision line

**Pilot** the BIL/ACWI allocation only with quarterly monitoring; reverse or pause the process if the window stress moves an allocation by 25 points or more, the net-return target fails, or the corporate-spread monitor requires review.

## Reflect

_Complete after the cold run and changed-input test._

1. What did the cold run find that I could not see?
2. What will I not touch before the deadline?

## Checkout links

_Add the GitHub links after the current Project 2 work is pushed._

- Lab 20 record:
- App:
- Portfolio logic:
- README:
- Decision memo:
- Validation record:
- Visible output:
