# Lab 16 — Provenance Gate

**Category:** Tuesday completion checkout — 25 or 0  
**Decision date:** March 31, 2026

## Purpose

Build a point-in-time filter and prove, on the known answer, what was knowable on the decision date.

> On the day you would have traded, what did this data actually say — and how much of what you see now came later?

Before using the code, explain the distinction between the month a number measures and the date that number was published. The month measured is the period described by the value; the publication date determines whether the value was available for a decision made on a specific date.

## Pace

| Minutes | Activity |
|---|---|
| 0–8 | Opener |
| 8–15 | D and R |
| 15–35 | I — build the filter |
| 35–45 | V — known-answer proof |
| 45–52 | Explain the code |
| 52–60 | Swap and break |
| 60–70 | Learn and reflect |
| 70–75 | Checkout |

## Training table

The table represents fictional one-year zero-coupon bond funds with three ratings. `Month measured` is the observation period; `Published on` is when that value became knowable. A later publication for the same ticker and month is a revision.

| Row | Ticker | Month measured | Published on | Price |
|---:|---|---|---|---:|
| 1 | AAA | 2026-01 | 2026-02-10 | 101.0 |
| 2 | AAA | 2026-02 | 2026-03-10 | 104.0 |
| 3 | AAA | 2026-03 | 2026-04-10 | 109.0 |
| 4 | AAA | 2026-02 | 2026-03-25 | 103.0 |
| 5 | BBB | 2026-01 | 2026-02-10 | 98.0 |
| 6 | BBB | 2026-02 | 2026-03-10 | 97.0 |
| 7 | BBB | 2026-02 | 2026-03-10 | 97.0 |
| 8 | BBB | 2026-03 | 2026-04-10 | 92.0 |
| 9 | CCC | 2026-01 | 2026-02-10 | 110.0 |
| 10 | CCC | 2026-02 | 2026-04-05 | 112.0 |
| 11 |  | 2026-02 | 2026-03-10 | 99.0 |
| 12 | CCC | 2026-02 | 2026-03-10 | 111.0 |

An API might return the two AAA February publications as records such as:

```json
{"realtime_start": "2026-03-10", "realtime_end": "2026-03-24", "date": "2026-02-01", "value": "104.0"}
{"realtime_start": "2026-03-25", "realtime_end": "9999-12-31", "date": "2026-02-01", "value": "103.0"}
```

## Provenance gate

Every row must be admitted, quarantined, or removed by a stated rule while retaining its original row number. Apply these rules in order:

1. Quarantine a row with no ticker.
2. Remove an exact duplicate.
3. Remove a row published after March 31, 2026.
4. For a ticker/month with multiple publications, keep the latest one published on or before the decision date.

The signal is the fund return: the percentage change from the previous month to the latest knowable month.

## Fixed-income checks

Each price is a fund of one-year zero-coupon bonds, priced per 100 of face value. Its yield is:

```text
yield = 100 / price − 1
```

Two checks fall outside the provenance gate and must be identified separately:

- A price above 100 produces a negative yield because the investor pays more than the 100 received at maturity.
- For the same maturity, riskier credit should yield more and therefore price lower: AAA > BBB > CCC.

The training data deliberately violates these economic checks: AAA and CCC trade above 100, and CCC is priced above BBB. The provenance rules do not remove them.

## Implementation requirement

Create `asof.py` using only the Python standard library. At the top, make the training table and decision date editable inputs. The script must:

- Apply the four provenance rules in the required order.
- Print a row funnel showing each rule, the number of rows removed, and their row numbers.
- Print the resulting as-of panel.
- For each ticker, print the as-of return to two decimals, naming the latest month used.
- Print a naive comparison signal using each row's latest publication without applying the publication-date filter.
- Calculate every result from the editable inputs rather than hard-coding answers.

Run it from this folder with:

```bash
python3 asof.py
```

## Checkout evidence

- Known-answer funnel, as-of panel, and as-of versus naive signals.
- A partner explanation of the search/filter logic and one answered question about the code.
- The fixed-income errors identified separately from provenance failures.
- A brief reflection on how revisions and publication dates can change a trading signal.

## Known-answer proof

The `asof.py` output matches the required provenance funnel:

| Funnel step | Rows removed |
|---|---|
| Quarantined: no ticker | 11 |
| Exact duplicate | 7 |
| Published after March 31 | 3, 8, 10 |
| Older vintage replaced by a revision | 2 |
| As-of panel | 1, 4, 5, 6, 9, 12 |

| Ticker | As-of signal | Naive signal |
|---|---|---|
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | −1.02% (February) | −5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

The key revision check is AAA: row 4, published March 25, replaces row 2, published March 10. Retaining row 2 would incorrectly produce a +2.97% February AAA signal instead of +1.98%.

## Sanity gate — zero-coupon yields

The provenance gate admits records based on when they were available; it does not establish that their prices are economically plausible. Applying `100 / price − 1` to the as-of panel gives:

| Row | Fund | Month | Price | Yield | Breaks |
|---:|---|---|---:|---:|---|
| 1 | AAA | Jan. | 101.0 | −0.99% | Negative yield |
| 4 | AAA | Feb. | 103.0 | −2.91% | Negative yield |
| 5 | BBB | Jan. | 98.0 | +2.04% | Nothing |
| 6 | BBB | Feb. | 97.0 | +3.09% | Nothing |
| 9 | CCC | Jan. | 110.0 | −9.09% | Negative yield; priced above BBB and AAA |
| 12 | CCC | Feb. | 111.0 | −9.91% | Negative yield; priced above BBB and AAA |

On time is not the same as true: the provenance gate needs a sanity gate behind it.
