# Video 1 Script Draft — System Change and AI Check

**Maximum length:** 3:00
**Webcam:** Keep your face visible in a small frame throughout the recording.
**Before recording:** Replace every bracketed note with your own truthful wording. This is a recording outline, not a transcript.

## Opening — 0:00–0:15

“I used Codex for coding, research organization, debugging, and document drafting. The analysis and committee decision are mine. Education, not investment advice.”

“My Project 2 system is a cautious-growth portfolio process using BIL, IEF, LQD, and ACWI.”

## How the system and my thinking changed — 0:15–1:25

“At first, I was focused on finding one lowest-volatility allocation that reached the 6.5% historical return target. Building the app changed how I thought about that answer. The base-case result is 60% BIL and 40% ACWI, with a 6.69% net return estimate and 6.03% annualized volatility, but it is not automatically a permanent recommendation.”

“The last-36-month stress changed the mix to 70% BIL, 15% IEF, and 15% ACWI. That moves ACWI by 25 points from the base case, which reaches my committee-review trigger. Because of that sensitivity, I changed my recommendation from treating one output as the answer to recommending a monitored pilot with a 55–65% BIL and 35–45% ACWI range. I also added a robustness map so the committee can see whether the allocation changes across return targets and time windows instead of seeing only one result.”

## One AI output I checked — 1:25–2:20

“One AI-assisted part I checked was the portfolio-display and mandate-check structure. I did not accept a recommendation just because the AI helped organize the app. I checked the portfolio results in `portfolio.py`, compared the equal-weight and 60/40 benchmark results against the same mandate, and verified that the base case, window stress, cost stress, and constraint stress appear in the app and validation record.”

“One specific AI-assisted output I checked was the boundary-condition correction for the 70% maximum ETF limit. A floating-point representation had treated an exactly 70% BIL result as slightly above the limit. I checked the rule by running the calculation: 70% BIL now passes the 70% maximum, while 75% BIL still fails it. I accepted that correction because it follows the stated mandate rather than changing the mandate to fit a result.”

## Closing — 2:20–3:00

“The biggest change in my thinking was that a portfolio screen is only helpful if it also shows when its answer is unstable. My process does not promise future returns. It gives the committee a transparent pilot, stress results, and conditions for review or reversal.”
