# Project 2 Video Recording Guide

Use the default app state for every recording unless a step below explicitly says to change one control. Keep a small webcam view visible in every video. Record each video as Unlisted or Public, not Private.

## Default screen state and verified values

Before every recording, open the app with these settings:

- No replacement CSV uploaded.
- Estimation window: **All available monthly returns**.
- Annual portfolio cost: **0** basis points.
- Signal as-of date: **2026-09-30**.
- **Download FRED/ALFRED vintage unchecked**.
- Fallback latest spread: **0.84%**.
- Fallback trailing median: **0.84%**.

With those settings, the screen should show:

| Item | Verified value |
|---|---:|
| Tentative recommendation | PILOT |
| Pilot range | 55–65% BIL; 35–45% ACWI |
| Base constrained mix | 60% BIL; 0% IEF; 0% LQD; 40% ACWI |
| Base net return estimate | 6.69% |
| Base annualized volatility | 6.03% |
| Equal-weight net return / volatility | 3.06% / 7.53% |
| 60/40 benchmark net return / volatility | 6.38% / 12.30% |
| Default LQD signal status | No review flag |
| Operational action card | COMMITTEE REVIEW because the 36-month stress reaches the 25-point trigger |

The visible-output file, memo, validation record, scripts, and transcripts use these same base-case figures.

## Video 1 — system change and AI-output check

**Maximum:** 3:00.
**Screen plan:** Start with the default app at the committee-decision panel, scroll to the stress table and robustness map, then briefly show `portfolio.py` and `validation-and-ai-use.md` in VS Code.

| Time | Show on screen | Say |
|---|---|---|
| 0:00–0:15 | Webcam plus app title/committee decision | Required AI and education statements. |
| 0:15–0:45 | Base-case comparison and allocation chart | Base 60% BIL / 40% ACWI, 6.69% net return, 6.03% volatility. |
| 0:45–1:20 | Required stress scenarios | Point to Window stress: 70% BIL, 15% IEF, 0% LQD, 15% ACWI; ACWI moves from 40% to 15%. |
| 1:20–1:40 | Allocation robustness map | Explain that it shows how return targets and windows change feasibility/weights. |
| 1:40–2:25 | `portfolio.py` and validation record | Show the 70% maximum-ETF boundary check: 70% BIL passes; 75% fails. Explain that the tolerance corrected floating-point noise without changing the mandate. |
| 2:25–3:00 | Committee decision panel | Close with the monitored-pilot conclusion and the review/reversal condition. |

The Video 1 draft now includes the verified 70%-versus-75% boundary check as the AI-output check.

## Video 2 — technical walkthrough

**Maximum:** 5:00.
**Screen plan:** Start in VS Code with the repository tree; show the README command, `prices.csv`, `portfolio.py`, then the live app.

| Time | Show on screen | Say |
|---|---|---|
| 0:00–0:15 | Webcam plus repository tree | Required AI and education statements. |
| 0:15–1:20 | README, `prices.csv`, app/portfolio files | Explain the cold-start command and the price-to-return-to-portfolio data flow. |
| 1:20–2:20 | `search_project2_mix()` in `portfolio.py` | Explain the five-point search, 70% maximum, 10% BIL minimum, 6.5% target, lowest-volatility selection, and `None` for no feasible mix. |
| 2:20–3:20 | Live app comparison, mandate checks, baseline-gap table, and robustness map | Explain equal weight, 60/40 benchmark, constrained portfolio, and the original extensions. |
| 3:20–4:05 | Sidebar: switch Estimation window to **Last 36 monthly returns**; show Selected interactive view and Required stress scenarios | Read the exact high-risk result: 70% BIL, 15% IEF, 0% LQD, 15% ACWI; 6.59% net return; 2.44% volatility; ACWI down 25 points. |
| 4:05–4:30 | Sidebar: keep FRED/ALFRED unchecked; set fallback latest spread to **0.87** and fallback trailing median to **0.86** | Show the LQD committee-review warning and explain it is not an automatic trade. |
| 4:30–5:00 | Method and limitations expander / validation record | State the historical-estimate and five-point-grid limitations. |

The 36-month window result is a valid high-risk stress demonstration. It is separate from the strict Locked Changed-Input Record requirement in the validation file.

## Video 3 — committee presentation

**Maximum:** 5:00.
**Screen plan:** Begin with the live default app—not VS Code—and keep the committee decision panel visible in the opening seconds.

| Time | Show on screen | Say |
|---|---|---|
| 0:00–0:20 | Live app title and committee decision panel | Required AI and education statements; this is a monitored pilot, not full adoption. |
| 0:20–1:10 | Three top decision metrics | Ask for a 55–65% BIL / 35–45% ACWI monitored pilot with quarterly review. |
| 1:10–2:00 | Comparison table, return chart, allocation chart | State 60% BIL / 40% ACWI, 6.69% net return, 6.03% volatility; identify both baselines. |
| 2:00–2:45 | Required stress scenarios and stress chart | Explain the 36-month window result and the 25-point ACWI change. |
| 2:45–3:15 | Robustness map, baseline-gap table, rebalancing action card | Explain why these additions make the dashboard useful for committee review. |
| 3:15–3:45 | Signal data card | Explain `BAMLC0A0CM`, the trailing-median rule, and no automatic trading. |
| 3:45–5:00 | Return to decision panel | State the exact reversal conditions and final committee ask. |

## After each recording

1. Export or copy the platform captions.
2. Replace the matching draft transcript with the actual corrected words and timestamps.
3. Correct `BIL`, `IEF`, `LQD`, `ACWI`, `BAMLC0A0CM`, percentages, and any material finance term.
4. Add the YouTube URL, title, duration, timestamp indices, transcript link, and logged-out access confirmation to `submission-manifest.md`.
