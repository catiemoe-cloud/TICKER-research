# Project 2 — Complete Build and Submission Plan

**Prepared:** November 10, 2026  
**Brightspace due date:** November 23, 2026  
**Role:** Portfolio or quantitative analyst  
**Core decision:** Recommend that an investment committee **adopt, allocate to, rebalance, pilot, or reject** a portfolio process under explicit objectives and constraints.

## Official requirements, in plain language

The final product is a runnable Python web app that a stranger can start from the README and use without help. It is not enough to submit a notebook, a one-time script, a static memo, or an attractive app with no evidence behind it.

The app and evidence package must contain all of the following:

1. A clear **mandate**: client/objective, investable universe, benchmark, risk measure, hard limits, and the question the committee needs answered.
2. **Three portfolios shown side by side**: equal weight, one other transparent baseline, and the constrained portfolio/process being recommended. Each must show whether it passes the mandate, including the rule that fails when it does not pass.
3. One **point-in-time signal** with a data card: source/link, definition, units, publication lag, revision behavior, download date, and the as-of rule that prevents look-ahead bias.
4. A **stress run** that changes a meaningful estimate, window, cost, or constraint; reports the result; and identifies the condition that stops the process.
5. One **Locked Changed-Input Record**: write the prediction with AI closed, commit it to GitHub before the run, then retain the before/after result, actual decision effect, and explanation.
6. A committee recommendation with an **allocation range**, monitoring triggers, a reversal trigger, and a specific committee ask.
7. A readable, reproducible repository with visible executed output and final Markdown records in `docs/`.
8. Three distinct short videos, corrected transcripts, and a Brightspace manifest with working links.

## Two required opening statements

Open the README, `docs/decision-memo.md`, and **each video** with both statements:

1. Name the AI tool(s) used and what each was used for; state that the analysis and decision are yours.
2. State: **Education, not investment advice.**

## What already exists in this project folder

| Existing item | What it can contribute | What still needs project-level work |
|---|---|---|
| `mandate.py` and Meridian notes | Example rule-checking and a model for translating client words into testable constraints | Replace Meridian as the main case with the actual Project 2 client mandate and show the resulting mandate verdicts in the final app. |
| `portfolio.py`, `prices.csv`, and `app.py` | Long-only search, monthly return/risk estimates, editable inputs, and a first Streamlit interface | Make the actual client universe the default, add the required side-by-side baselines and mandate verdicts, add costs/stress/stop condition, and make the committee decision visible. |
| `asof.py` and `asof_app.py` | Point-in-time/ALFRED pattern and a possible data-provenance component | Select one actual signal; document its data card and ensure the final process uses only values knowable on each decision date. |
| Labs 18–19 investor skills/panel | Optional company-screening context for holdings | Keep only if it supports the mandate or monitoring decision. It is **not** one of the base Project 2 requirements. |

### Important historical-note check

The current course repository's Lab 19 calls for a **Cathie Wood + Burry** panel. Your existing Lab 19 folder has a **Graham + Burry** panel. Project 2 does not require either panel, so do not spend time rebuilding it unless it will materially support your recommendation or you need to correct the Lab 19 record separately.

## Chosen project direction

### Mandate

I am building this for a cautious investor who still wants some growth but needs a lot of liquidity available. The portfolio will use BIL, IEF, LQD, and ACWI. My goal is to reach at least a 6.5% historical annual return estimate while staying long-only, keeping at least 10% in BIL, keeping every ETF at or below 70%, and rebalancing quarterly. I will use annualized volatility as the main risk measure and compare the recommended portfolio to an equal-weight portfolio and a 60% ACWI / 40% LQD benchmark.

The main committee question is: **Can we pilot a 60% BIL / 40% ACWI allocation when the return estimate changes depending on the time window?**

### Point-in-time signal

I will use `BAMLC0A0CM`, the ICE BofA U.S. Corporate Index Option-Adjusted Spread, as a credit-risk monitoring signal for LQD. The signal is not an automatic buy or sell rule. If the spread moves above its trailing 12-month median, it will flag LQD for committee review. I will only use values that were available at the decision date through the ALFRED vintage, not later revised data.

### Tentative committee decision

My tentative recommendation is to **pilot** a portfolio with 55–65% BIL and 35–45% ACWI. I do not plan to allocate to LQD or IEF until the committee agrees on the credit-spread monitoring rule. This is only a pilot because my earlier test showed that changing the return window moved the BIL weight by 25 percentage points, which means the allocation is sensitive to the estimates.

I would reverse or pause the pilot if the 36-month window again changes an allocation by 25 percentage points or more, if the portfolio no longer reaches the return objective, or if the credit-spread signal requires a review.

> **Important:** The final Locked Changed-Input Record must be written by me with AI closed before I run the selected changed input. I will add the prediction, timestamp, old/new values, expected direction, and commit hash myself before any test is executed.

## Original extensions beyond the course baseline

The course baseline requires a runnable portfolio app, two baselines, a constrained portfolio, a point-in-time signal, a stress run, and a defendable recommendation. My additions should make those requirements more useful for a committee, not hide the underlying calculations or create unnecessary scope.

### Extension 1 — Allocation robustness map (recommended)

Instead of showing only one stress result, the app will show a small matrix of outcomes across return targets and data windows. For each scenario, it will show whether a feasible portfolio exists and the recommended BIL/ACWI allocation.

| What changes | Example settings | Why it adds value |
|---|---|---|
| Return target | 5.5%, 6.0%, 6.5%, 7.0% | Shows whether the recommendation only works because of one target assumption. |
| Estimation window | all available monthly returns vs. last 36 months | Shows whether a different market period changes the answer. |
| Output | feasible/infeasible, BIL, ACWI, volatility | Makes model sensitivity visible instead of burying it in a paragraph. |

**College-student explanation:** “I wanted to see whether the 60/40 BIL/ACWI result was actually stable or if it only looked good under one set of assumptions. The robustness map makes it easier to see where the strategy changes a lot and where it stays pretty similar.”

### Extension 2 — Rebalancing action card (recommended)

The app will convert the target allocation and the investor's current allocation into a plain-English operational recommendation: **hold**, **rebalance**, or **committee review**.

- `Hold`: every current weight is within a 5-percentage-point band around the target and the credit signal has no review flag.
- `Rebalance`: one or more weights are outside the band, but the signal has no review flag; show the weight changes and estimated turnover.
- `Committee review`: the corporate-spread monitor flags LQD, the model becomes infeasible, or a stress scenario changes an allocation by 25 points or more.

**College-student explanation:** “The optimizer gives weights, but a committee still needs to know what to do today. This card turns the numbers into a simple hold, rebalance, or review decision without pretending the app can trade automatically.”

### Extension 3 — Signal governance panel

The existing `BAMLC0A0CM` monitor will add a small governance panel: source, selected as-of date, last observation available on that date, trailing-median comparison, revision count if available, and current status. This expands the required data card into a simple audit trail.

**College-student explanation:** “I do not want to just say the credit-spread signal is point-in-time safe. I want the app to show the date and source it used, so someone else can check whether the signal was actually available before the decision.”

### Extension 4 — Baseline gap explanation

Under the portfolio-comparison table, the app will explain the largest practical difference between the constrained portfolio and each baseline: return gap, volatility gap, BIL/liquidity gap, and the exact mandate rule that caused a baseline to fail.

**College-student explanation:** “This helps explain why I am not automatically choosing the benchmark or equal-weight mix. I can show exactly what the pilot portfolio gives up or gains, instead of just saying that it has a lower volatility number.”

### Scope decision

I will build Extensions 1 and 2 first because they directly support the required stress test and the final committee action. Extension 3 is next because the project already uses the credit-spread signal. Extension 4 is optional if the core validation, documents, cold run, and videos are complete first.

## Recommended repository structure

```text
project-2/
├── README.md                         # cold-start instructions and project overview
├── requirements.txt                  # exact Python dependencies
├── app.py                            # final Streamlit app entry point
├── portfolio.py                      # reusable return, risk, search, and mandate functions
├── data/
│   ├── prices.csv                    # raw/cleaned price input, source and download date documented
│   └── signal_*.csv                  # only if a local snapshot is needed for reproducibility
├── outputs/
│   ├── visible_output.md             # decision, as-of date, material inputs, portfolio table
│   ├── baseline_results.*            # reproducible output artifact(s)
│   └── stress_results.*
├── docs/
│   ├── decision-memo.md
│   ├── validation-and-ai-use.md
│   ├── transcript-video-1.txt
│   ├── transcript-video-2.txt
│   └── transcript-video-3.txt
├── tests/                            # optional but strongly recommended
└── .env.example                      # only if credentials are required; variable names empty
```

Do not commit `.env` files, credentials, API keys, private data, or passwords. A live deployment is optional; a local app plus visible executed output is required.

## Timeline and work order

### Phase 0 — Freeze the project definition first (today)

**Goal:** Decide exactly what the app will recommend before adding features.

- [x] Confirm the Brightspace due date: **November 23, 2026**.
- [ ] Read the assignment points, assignment-specific manifest, and instructional-team GitHub access instructions in the Brightspace assignment header. The public repository does not publish these details.
- [ ] Write a one-paragraph client mandate: intended user, objective, universe of 3–6 funds, benchmark, risk measure, hard constraints, rebalancing assumption, and one CIO question that could change the design.
- [ ] Choose the committee action vocabulary now: likely `pilot`, `adopt`, or `reject`; do not call an optimizer result “optimal” by itself.
- [ ] Choose one defensible allocation range (for example, a range around the recommended weights rather than false point precision).
- [ ] Choose the point-in-time signal and state why it belongs in the process rather than merely being interesting.
- [ ] Define a stop/reversal condition before seeing the final result.

**Done when:** A reader can state what decision the committee is being asked to make, for whom, under what limits, and what would reverse it.

### Phase 1 — Build the final calculation spine (first build session)

**Goal:** Make all portfolio choices reproducible from source data.

- [ ] Preserve `portfolio.py` as the single source of portfolio math; do not duplicate calculations in the Streamlit page.
- [ ] Use the actual client ETF universe and label historical returns as **estimates, not forecasts**.
- [ ] Calculate and display expected return, volatility/risk measure, reserve/liquidity weight, all hard-constraint results, and any transaction-cost assumption.
- [ ] Make the investment universe and all editable assumptions visible in the app.
- [ ] Implement the constrained search/process and return an honest infeasible answer if no mix meets the mandate. Do not lower the objective merely to manufacture a portfolio.
- [ ] Add two transparent comparison portfolios: equal weight and a second baseline chosen in advance (for example, the stated benchmark). Display their weights, measures, and pass/fail mandate results next to the constrained portfolio.
- [ ] Test the core functions with known inputs: weight sums, long-only behavior, correlations, constraint failures, and an infeasible case.

**Done when:** The app's recommended portfolio and both baselines use the same inputs and every outcome is computed rather than typed.

### Phase 2 — Data integrity and point-in-time signal (second build session)

**Goal:** Show that the inputs would have been knowable when the decision was made.

- [ ] Create the signal data card in the README or `docs/validation-and-ai-use.md`: source URL, what it measures, units, frequency, release lag, revision policy, download date, and exact as-of rule.
- [ ] Use the Lab 16/17 approach: distinguish date measured from publication date; prevent later values/revisions from entering an earlier decision.
- [ ] Record a decision/as-of date in the app and visible output.
- [ ] Independently compare at least three signal values to the source page.
- [ ] Decide whether the signal is admitted, quarantined, or rejected; document what would change that decision.
- [ ] Add a clear source/as-of date label to every data-driven result.

**Done when:** A skeptical reader can trace the riskiest input from the on-screen result back to a source and explain why it was available at the decision date.

### Phase 3 — Stress, stopping rule, and Locked Changed-Input Record (third build session)

**Goal:** Test the financial claim most likely to change the committee action.

- [ ] Select one load-bearing input: expected return, lookback window, transaction cost, reserve minimum, signal threshold, or another material assumption.
- [ ] With AI closed, write in `docs/validation-and-ai-use.md`: old value, new value, units, expected direction of return/risk/weights, predicted decision effect, timestamp, and why this is a meaningful test.
- [ ] Commit and push this prediction **before** executing the change. Record that commit hash in the document.
- [ ] Run the changed input. Preserve before and after outputs.
- [ ] Add actual direction, actual decision effect, reconciliation to the prediction, and a failure diagnosis if the prediction was wrong or nothing changed.
- [ ] Run the required stress view(s) for estimates, lookback window, costs, and constraints as applicable. State the condition that stops the process or causes a reject/review.

**Done when:** The record makes it impossible to write the prediction after learning the answer, and the final recommendation honestly reflects the stress result.

### Phase 4 — Make the app committee-ready (fourth build session)

**Goal:** A committee can understand the action without reading the source code.

- [ ] Add a top-of-page decision panel: action, recommended allocation range, as-of date, key condition, reversal trigger, and monitoring triggers.
- [ ] Add a portfolio comparison table: equal weight, second baseline, constrained/recommended process; weights, return estimate, risk, costs/assumptions, constraint verdict, and failed rule if applicable.
- [ ] Add a visible stress-result section with before/after values and the stop condition.
- [ ] Add a point-in-time signal/data-card section or a direct link to it.
- [ ] Keep inputs, results, source dates, and limitations readable without running code by saving a validated report/screenshot in `outputs/`.
- [ ] Ensure the app opens with the two required statements.

**Done when:** A reader can see the decision, evidence, limits, and risks in one cold viewing.

### Phase 5 — Write the evidence package (after the system is stable)

#### README

- [ ] Start with the two required statements.
- [ ] State the finance decision and intended user.
- [ ] Explain setup, dependency installation, and **one command** to run the app from a clean folder.
- [ ] Include a concise repository map.
- [ ] Name all data sources, dates/as-of boundary, assumptions, known limitations, and where visible executed output lives.
- [ ] Link to the decision memo and validation record.

#### `docs/decision-memo.md`

- [ ] Start with the two required statements.
- [ ] Lead with the recommendation and committee ask.
- [ ] State the allocation range instead of implying false precision.
- [ ] Include the as-of date, strongest evidence, benchmarks/baselines, mandate verdict, and stress outcome.
- [ ] State material assumptions/sensitivities, main risks/failure conditions, monitoring triggers, and reversal condition.
- [ ] Reference the validation-and-AI-use record rather than hiding or duplicating the checks.

#### `docs/validation-and-ai-use.md`

- [ ] List sources and data/as-of boundary.
- [ ] Record known-answer checks, baseline comparisons, tests, results, failures, and limitations.
- [ ] Include the complete Locked Changed-Input Record.
- [ ] For each material AI use, state tool/model/version if available, interaction date, task/output summary, `accept`/`modify`/`reject`, independent check, and decision/resulting revision.

**Done when:** README, memo, app, visible output, and validation file all show the same numbers, dates, assumptions, and recommendation.

### Phase 6 — Week 12 cold review and defense

**Goal:** Find failures before submission.

- [ ] Before the cold run, write the committee action and the one claim most likely to reverse it without AI.
- [ ] Give a partner only the GitHub README link. Do not coach.
- [ ] Have the partner record the exact command, first failure, elapsed time, and where the result appears.
- [ ] Ask AI for one concrete test of the riskiest claim; independently check it and repair, qualify, or drop the claim.
- [ ] Freeze a short must-fix list. Do not add unrelated new analysis after this point.
- [ ] Rehearse Video 3 with a skeptical partner question about the mandate, timing, or baseline.

**Done when:** A stranger reaches the same decision from the README alone, or the README clearly documents the remaining limitation.

### Phase 7 — Lab 20 readiness evidence

**Goal:** Produce the final reproducibility proof.

- [ ] Record the partner cold-run note in the validation file.
- [ ] Confirm the Locked Changed-Input Record was committed before execution.
- [ ] Explain the function/block that creates the decision number line by line without AI assistance.
- [ ] Fix and push the first cold-run failure; if no failure occurred, record that clean result.
- [ ] Write one decision line: `adopt`, `allocate`, `rebalance`, `pilot`, or `reject`, plus the condition that reverses it.
- [ ] Record what the cold run revealed and what will deliberately remain untouched before the deadline.

### Phase 8 — Record videos and final submission

**Video 1 — research/system change and AI-output check (maximum 3:00):**

- [ ] Open with the two required statements.
- [ ] Explain how the system and your thinking changed from the original mandate.
- [ ] Show one concrete AI-generated claim, suggestion, code result, or output.
- [ ] Show the independent check and say whether you accepted, qualified, corrected, or rejected it and why.

**Video 2 — technical walkthrough (maximum 5:00):**

- [ ] Open with the two required statements.
- [ ] Show repository architecture, data flow, key functions/files, financial logic, and the clean-run command.
- [ ] Demonstrate the validation/changed-input test for the highest-risk financial or technical claim.
- [ ] Name one failure mode, limitation, or unresolved risk.

**Video 3 — investment-committee defense (maximum 5:00):**

- [ ] Open with the two required statements **and a live demonstration of the running app**.
- [ ] Lead with the committee action, allocation range, evidence, conditions, and risks—not the coding process.
- [ ] Defend the action against a skeptical question and end with a clear committee ask.

**For every video:**

- [ ] Upload as Unlisted or Public YouTube video (never Private), or approved Purdue-hosted equivalent.
- [ ] Enable captions, then correct finance terms, ticker symbols, names, speaker attribution, and material numbers.
- [ ] Save the corrected transcript as the matching `docs/transcript-video-#.txt` file.
- [ ] Confirm the link works while logged out.

**Brightspace final submission:**

- [ ] Attach the exact repository Markdown files: `docs/decision-memo.md` and `docs/validation-and-ai-use.md`.
- [ ] Attach all three corrected plain-text transcripts.
- [ ] Complete the assignment's manifest with stable GitHub links, video URLs, titles/durations, timestamp index, repository-access confirmation, and optional deployed-output link.
- [ ] Mark Project 2's research-evolution row **not required**; Project 2 has no Edition A or B.
- [ ] Confirm the instructional team can access the repository and videos at grading time.

## Final acceptance checklist

- [ ] A clean user can clone/open the repo, install dependencies, execute the one README command, and find the decision.
- [ ] The visible output shows material inputs, as-of date, and finance decision without running code.
- [ ] The constrained portfolio and two baselines are all displayed with mandate verdicts.
- [ ] Historical inputs are labeled as estimates; the point-in-time signal has a complete data card.
- [ ] The stress run, stop condition, and Locked Changed-Input Record are documented.
- [ ] The recommendation has an action, allocation range, monitoring triggers, reversal trigger, and committee ask.
- [ ] No artifact conflicts on values, dates, assumptions, or the recommendation.
- [ ] No secrets or private data are committed.
- [ ] Every GitHub/video/manifest link works logged out.

## Inputs still needed from you

1. The Brightspace assignment points, assignment-specific manifest, and any instructions that do not appear in the public GitHub repository.
2. Your final client mandate: objective, universe, benchmark, risk measure, hard limits, and rebalancing rule.
3. Your chosen point-in-time signal and its intended effect on the portfolio process.
4. The committee action you are leaning toward and the allocation range you can defend.
5. The exact stress/changed input you want to test and your AI-off prediction before we run it.

## Professor sources reviewed

- [Project 2 — Investment Management Application](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/projects/project-2-investment-management-application.md)
- [Major Project Student Checklist](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/projects/major-project-student-checklist.md)
- [Project Submission Architecture](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/PROJECT-SUBMISSION-ARCHITECTURE.md)
- [Week 12 Project 2 Studio](https://github.com/CinderZhang/FIN43900-Fall2026/tree/main/lessons/week-12)
- [Week 13 Lab 20 — Project 2 Readiness](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-13/lab-20-project2-readiness.md)
- [Labs 13–19 course map](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-12/student-handout.md)
