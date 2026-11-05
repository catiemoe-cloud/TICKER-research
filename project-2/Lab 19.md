# Lab 19 — Investor Skills Panel

**Status:** Ready for submission after the individual Brightspace quiz and checkout.  
**Working date:** November 5, 2026

## Run of show

Opener → Build the panel → COST proof and threshold probe → Your company → Explain code → Bull and bear → Decision and learn → Reflect and checkout.

## D — Shared question

> When three investors' skills read the same 10-K facts, where do they agree, where do they split — and would you trust the panel?

## Opening check — COST

Open the app with COST before beginning the panel analysis. Confirm that the five fiscal years, owner-earnings and net-income chart, table, Buffett checks, and memo are visible.

**Observed result:** COST’s five fiscal years, owner-earnings and net-income chart, table, Buffett checks, and Buffett memo loaded from the shared SEC facts file.

**Partner explanation:** Buffett would view Costco through owner earnings and ROE, while Graham focuses more on liquidity. That is why Graham’s original 2.0x current-ratio rule failed Costco even though Buffett’s three business-quality checks passed.

## Worklog

| Stage | Evidence / result | Status |
|---|---|---|
| D — Shared question and COST app check | COST facts loaded | Complete |
| R — Read investor skill pages and rules | Read Buffett, Graham, and Burry frameworks; retained SEC-only rules | Complete |
| I — Run the three skills on the same facts | Added Graham and Burry skills, common SEC facts engine, and three COST memos | Complete |
| V — Compare outputs and validate facts | COST ratios match the known answer. Original panel: Buffett 3/3, Graham 2/3, Burry 2/2. Threshold probe: Graham 3/3 at 1.0x. | Complete |
| E — Explain agreement and disagreement | Explained the Graham pass/fail/not-known function and missing-input behavior. | Complete |
| R — Reflect on whether to trust the panel | Recorded the NVDA agreement, split, threshold lesson, and conditional decision below. | Complete |

## Your company

**Company used:** NVIDIA Corporation (**NVDA**).

The portfolio’s largest position is BIL, an ETF rather than an operating company that files its own 10-K. I therefore used NVDA, the largest company holding in the portfolio’s equity fund, ACWI, so the panel could read an SEC 10-K for an actual company.

### NVDA panel result

| Investor | Checks | Verdict |
|---|---|---|
| Buffett | 3 of 3 pass | Own the business |
| Graham | 3 of 3 pass at the kept 1.0x current-ratio threshold | Watch the business |
| Burry | 1 of 2 pass: leverage passed; operating cash flow at least net income every year failed | Watch the business |

**Key facts from the app:** Owner earnings rose from $8,132 million to $96,676 million, and net income rose from $9,752 million to $120,067 million. The latest current ratio was 3.91x and the latest liabilities-to-equity ratio was 0.31x. Burry’s cash-flow check failed because operating cash flow was $9,108 million while net income was $9,752 million in the earliest displayed year.

**Final conclusion:** NVDA looks strong on growth, profitability, liquidity, and leverage in this five-year 10-K screen. I would use the panel to narrow companies for further research, but I would not treat its “own” or “watch” label as a buy decision because the panel does not assess price, competition, or future risks.

## V — COST ratio proof

| FY end | 2022-08-28 | 2023-09-03 | 2024-09-01 | 2025-08-31 | 2026-08-30 |
|---|---:|---:|---:|---:|---:|
| Current ratio | 1.02 | 1.07 | 0.97 | 1.03 | 1.06 |
| Liabilities ÷ equity | 2.11 | 1.75 | 1.96 | 1.64 | 1.49 |

**Original panel:** Buffett 3 of 3; Graham 2 of 3 because the original 2.0x current-ratio threshold failed; Burry 2 of 2.

**Threshold probe:** Graham’s threshold is now **1.0x**. COST’s latest 1.06x current ratio passes, so Graham now passes 3 of 3. The one-line rationale is recorded under the Graham memo.

## E — Explain the Graham checks

**Lines 120–123 — `check_text(value)`:** This is basically the code’s translator. If the value is `None`, it prints `not known`. If the result is true, it prints `PASS`; if it is false, it prints `FAIL`.

**Lines 158–162 — current ratio:** The code calculates current ratio by dividing current assets by current liabilities. It only does that when the needed numbers exist and current liabilities are not zero. Otherwise, it leaves the result as `None` instead of making up a ratio.

**Line 175 — positive-income check:** If net income is missing for even one year, the result is `None`. If every year has a number, `all(...)` checks that every net-income value is greater than zero.

**Lines 176–178 — income-growth check:** This check starts as `None`. The code only compares the first and last years if there are five years of data and both values are available. If the last year is higher, net income grew.

**Lines 182–184 — latest-year inputs:** The code treats the final row as the newest fiscal year and pulls its current ratio for the latest-year Graham check.

**Lines 198–201 — Graham panel results:** The current-ratio test uses the 1.0x threshold we chose. If the ratio is missing, the code sends `None` to `check_text`, so the app says `not known`. The other two Graham results use the net-income checks the code already calculated.

**Answer to the partner’s missing-input question:** If an input is missing, the code keeps it as `None`, and `check_text` turns that into `not known`. That matters because the program should not give a pass or fail based on a number it guessed.

## Bull and Bear — Partner attack

**My bull case:** “I think Costco looks pretty solid from the panel. Buffett and Burry both passed all their checks, and the cash flow being higher than net income every year makes the earnings seem more real.”

**Allie’s bear case:** “Yeah, but Graham’s original liquidity test still failed because Costco’s current ratio is only 1.06, not 2.0. Also, we’re only looking at old 10-K numbers, so that doesn’t guarantee Costco will keep growing or that its advantage over competitors will last.”

### NVDA follow-up

**Bull case:** NVDA’s owner earnings increased from $8,132 million to $96,676 million, and Buffett passed every check. The latest 3.91x current ratio and 0.31x liabilities-to-equity ratio also show strong liquidity and manageable leverage.

**Bear case:** Burry’s cash-flow test failed because operating cash flow was below net income in at least one reported year. The panel also only uses historic 10-K facts, so it cannot prove that NVDA’s growth or competitive advantage will continue.

## Your decision — A panel of AI agents

**Decision:** Only with a condition: I would let the panel screen Project 2 companies only if the shared facts are calculated and checked in code, while I review the thresholds, assumptions, and final judgment myself. NVDA shows why: Buffett says own the business, but Burry says watch it because the cash-flow check fails.

**What it is:** A panel of AI agents is a group of separate AI roles that analyze the same company from different investing perspectives.

**How it works:** All three skills receive the same SEC 10-K facts, but they apply different rules and priorities. Buffett focuses on owner earnings and returns, Graham focuses on financial safety and liquidity, and Burry focuses on whether cash flow supports earnings and whether leverage is manageable. They can disagree because the facts stay the same while the screen design, threshold choices, and interpretation differ.

**Partner explanation:** “The panel is useful because it gives us more than one way to look at the same numbers. But it is not automatically right: the agents can disagree because their rules are different, and we still have to decide whether those rules make sense for the company.”

## Reflect

**Where the panel agreed and split:** On NVDA, the panel agreed that the company had positive and growing net income, strong liquidity, and low latest-year leverage. Buffett passed all three checks and said to own the business. Graham also passed all of its checks at the 1.0x threshold, but stayed more cautious with a watch verdict. Burry split from Buffett because operating cash flow was not at least net income in every year, even though the leverage check passed.

**What the threshold probe shows:** The threshold probe shows that a screen’s verdict depends on its design choice, not just on the company’s reported facts. Costco’s current ratio stayed 1.06x, but lowering Graham’s threshold to 1.0x changed the result from fail to pass. That means I should review the rule behind any pass or fail rather than blindly trusting the label.

**Reflection to share with my partner:** The skills make the data collection and tests repeatable, but the model still decides how to describe the company and choose “own,” “watch,” or “pass.” “Not found” is better than an estimate because it shows exactly where the SEC facts do not support a calculation; an estimate could make a screen look more certain than it really is.
