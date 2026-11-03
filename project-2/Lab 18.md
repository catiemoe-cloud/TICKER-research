# Lab 18 — Buffett Skill from SEC EDGAR

**Status:** Complete — ready for Tuesday checkout  
**Working date:** November 3, 2026  
**Purpose:** Turn Buffett’s business-quality framework into a repeatable Codex skill: code computes the 10-K facts; the model makes the business judgment.

## D — Decision question

> Can an investor’s philosophy become a skill your AI runs the same way every time — every number computed by code from the 10-K, the judgment the model’s?

**Partner explanation:** Code can compute **owner earnings** as operating cash flow minus capital spending. Judgment is needed to decide whether Costco has a **durable economic moat**; reported numbers support that conclusion but cannot prove that competitors will not erode it.

## R — Research and rules

I read FAskills’ Buffett page for the framework only. I did not install FAskills or use its paid data sources. This work uses keyless SEC EDGAR `company_tickers.json` and `companyfacts` only.

| Rule | Implementation |
|---|---|
| Filings and periods | 10-K only; last five fiscal-year ends; flows must span 300–380 days |
| Repeated facts | Latest `filed` date wins for the same fiscal-year end |
| Revenue | `RevenueFromContractWithCustomerExcludingAssessedTax`, then `Revenues` |
| Net income | `NetIncomeLoss` |
| Operating cash flow | `NetCashProvidedByUsedInOperatingActivities` |
| Capital spending | `PaymentsToAcquirePropertyPlantAndEquipment`, then `PaymentsToAcquireProductiveAssets` |
| Equity | `StockholdersEquity` |
| ROE | Net income ÷ year-end equity; `not known` when equity is zero/below or an input is missing |
| Liabilities ÷ equity | Computed internally from `Liabilities` ÷ equity; `not known` when equity is zero/below or an input is missing |
| Owner earnings | Operating cash flow − capital spending; `not known` if an input is missing |
| Missing reported fact | `not found`; never estimated |

## I — Implement

**Skill location:** `~/.codex/skills/edgar-buffett/`  
**Skill files:** `SKILL.md` and `scripts/edgar_financials.py`  
**App:** `lab18_app.py`  
**COST memo:** `reports/COST_buffett_memo.md`

The skill uses SEC facts only, prints the five-year table with source XBRL tags, and computes these checks in code:

1. ROE is at least 15% every year.
2. Owner earnings are positive every year.
3. Owner earnings grew from the first year to the last.

ROE and owner earnings are labeled **computed** because they are calculations rather than separate XBRL facts. The AI memo makes only an **Own the business**, **Watch it**, or **Pass** business judgment—no price data, target, or recommendation.

**Your decision:** I mostly trust Buffett’s **Own the business** verdict because COST’s verified five-year record shows consistently high ROE and rising, positive owner earnings; I would still treat the moat conclusion as judgment rather than a fact proven by the 10-K numbers.

## Floor probes

- **COST:** The five-year table matches the known answer and all three checks pass.
- **JPM:** Capital spending is unavailable under the prescribed tags, so it prints `not found`. Owner earnings and both owner-earnings checks print `not known`; no estimate is substituted.
- **Memo audit:** The app extracts every number in the memo and flags any number absent from the script’s printed output. A hand-typed `$999,999` test was flagged.
- **Submission:** Submit this work individually.

Run from `project-2/` with a real contact value supplied in the terminal only, not saved in this workspace:

```bash
SEC_EDGAR_USER_AGENT='Your Name your.email@example.com' \
streamlit run lab18_app.py
```

## V — Verify: COST known answer (USD millions)

| FY end | Revenue | Net income | Operating cash flow | Capital spending | Equity | ROE | Owner earnings |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2022-08-28 | 226,954 | 5,844 | 7,392 | 3,891 | 20,642 | 28.3% | 3,501 |
| 2023-09-03 | 242,290 | 6,292 | 11,068 | 4,323 | 25,058 | 25.1% | 6,745 |
| 2024-09-01 | 254,453 | 7,367 | 11,339 | 4,710 | 23,622 | 31.2% | 6,629 |
| 2025-08-31 | 275,235 | 8,099 | 13,335 | 5,498 | 29,164 | 27.8% | 7,837 |
| 2026-08-30 | 303,154 | 9,226 | 15,817 | 6,435 | 35,803 | 25.8% | 9,382 |

| Buffett check | COST result |
|---|---|
| ROE of 15% or more every year | Pass |
| Owner earnings positive every year | Pass |
| Owner earnings grew, first year to last | Pass |

**Result:** The script reproduces every required COST value in USD millions. Owner earnings and net income both rose from FY2022 to FY2026. The Streamlit app shows their chart, the tagged table, the checks, the memo, and a number audit that flags any memo number absent from the script output.

## E — Explain

1. The script finds the ticker’s CIK in the SEC ticker file, pads it to ten digits, and downloads its company facts.
2. It admits only 10-K facts; cash-flow and income-statement values also need a one-year period.
3. If filings contain several facts for the same fiscal-year end, it retains the latest filed value.
4. It chooses the required XBRL tags in order, calculates ROE and owner earnings, then evaluates the three checks.
5. The memo uses only the resulting printed values. The app independently audits its numbers.

## R — Reflect

**What the skill makes the same every time:** It uses the same SEC-only source, 10-K and one-year-period filters, latest-filing rule, XBRL-tag order, formulas, units, and three Buffett checks for every ticker. The model is left to judge whether the verified record supports **Own the business**, **Watch it**, or **Pass**; it cannot prove a durable moat, management quality, or future performance from the historical numbers alone.

**Why `not found` is better than an estimate:** `not found` preserves the boundary between a reported fact and an assumption. Replacing a missing prescribed XBRL fact with an estimate could make owner earnings and its checks look precise when they are not. Returning `not found` and `not known` makes the gap visible, prevents a false pass/fail result, and tells the analyst what evidence still needs to be found.

## Checkout

- [x] Read the Buffett framework without installing or using FAskills data.
- [x] Created and installed the `edgar-buffett` Codex skill with `SKILL.md` front matter and a bundled script.
- [x] Used only keyless SEC EDGAR data and no price data.
- [x] Ran the skill on COST; saved the facts JSON and Buffett memo.
- [x] Reproduced the known-answer table and all three passing checks.
- [x] Built and started the Streamlit app with the required caption, chart, table, checks, memo, and number audit.
- [ ] Opened the Lab 18 Brightspace quiz attempt.
- [ ] Completed partner swap/explanation and course checkout.
