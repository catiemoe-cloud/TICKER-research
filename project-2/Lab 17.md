# Lab 17 — Real-Time Series Gate

## Preparation

Arrive with the Lab 16 chat, the Lab 15 Streamlit app, the prework series, and a partner. When debugging, provide the exact command and exact error text.

## Decision question

> Was each number in the selected series knowable on the day it would have been traded on — and may Project 2 use it?

The decision requires comparing a series as shown today with its vintage as known on an earlier date. A value can be measured on one date but published or revised later, so it may not have been available for an earlier trading decision.

## Real, live data

FRED shows each series as it reads today. ALFRED shows a historical vintage: what the series read on an earlier date. Both sources are free and do not require an API key or account for the public CSV downloads.

| Series | What it is | FRED page |
|---|---|---|
| BAA | Moody's Baa corporate bond yield, monthly | [BAA](https://fred.stlouisfed.org/series/BAA) |
| FEDFUNDS | Effective federal funds rate, monthly | [FEDFUNDS](https://fred.stlouisfed.org/series/FEDFUNDS) |
| DGS10 | 10-year Treasury yield, daily | [DGS10](https://fred.stlouisfed.org/series/DGS10) |
| MORTGAGE30US | 30-year fixed mortgage rate, weekly | [MORTGAGE30US](https://fred.stlouisfed.org/series/MORTGAGE30US) |
| Prework selection | Student-selected series | Its FRED page; the series ID is the final part of the URL |

A `.` in a FRED or ALFRED CSV is a missing observation, not a number.

## App requirement

Create `asof_app.py`, a Streamlit page that works like a FRED page for interest rates. It must request one current CSV and one vintage CSV per selected series:

```text
https://fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES
https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=SERIES&vintage_date=YYYY-MM-DD
```

Cache the two download functions. The default sidebar controls are:

- A multiselect with BAA, FEDFUNDS, DGS10, and MORTGAGE30US selected.
- A text field for another FRED series ID.
- Start date: January 1, 2020.
- As-known-on date: today.

The page must show:

1. One line chart per selected series using today’s values from the start date.
2. Under each chart, the last date in that series known on the selected as-known-on date.
3. One table with a row per series containing:
   - Series ID linked to its FRED page.
   - Last date measured and value known on the selected date.
   - Last date measured and value today.
   - Count of values today after the last date known then.
   - Count of values on the same dates revised since.

The completed page also provides a combined current-values line chart for all selected series and an individual chart-style control. Line and bar views display the rate observations directly. The candlestick-style view uses the prior observation as the open and the current observation as the close; it is labeled as a rate-change visualization because these FRED series do not provide true market OHLC data.

An unknown series ID must display an error for that series without stopping the other series. Under the title, display:

> Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today; built with AI help, a learning demonstration, not investment advice.

## Run command

After `asof_app.py` is created, run it from the Project 2 folder:

```bash
cd /Users/catiemoe/fin43900-fall2026/project-2
streamlit run asof_app.py
```

## Checkout evidence

- Four default rate charts and their as-known-on dates.
- Table counts for future observations and revisions.
- A real-time-vintage conclusion for the chosen prework series.
- An explicit Project 2 use/no-use decision based on whether the data was knowable at the trade date.

## Project 2 prework series data card

**Selected series:** `BAMLC0A0CM` — ICE BofA U.S. Corporate Index Option-Adjusted Spread.

| Field | Data card |
|---|---|
| Source and link | [FRED: BAMLC0A0CM](https://fred.stlouisfed.org/series/BAMLC0A0CM); source shown by FRED: Ice Data Indices, LLC |
| What it measures | The option-adjusted spread between the investment-grade U.S. corporate-bond index and a spot Treasury curve. |
| Units | Percent, not seasonally adjusted. |
| Frequency | Daily close. |
| Why it is relevant | It is an external credit-spread indicator for the investment-grade corporate-bond sleeve (LQD), not the fund's own price. A widening spread can pressure corporate-bond values; a narrowing spread can support them, holding other factors constant. |
| Publication timing | The FRED page showed the October 28, 2026 observation updated October 29, 2026, indicating an approximately next-business-day availability pattern for this observation. |
| Revisions | FRED states that all data are subject to revision; the ALFRED comparison in `asof_app.py` must be used to test the actual vintage for a decision date. |
| Download date | October 29, 2026 |

Before checkout, add `BAMLC0A0CM` in the app's custom-series field. Compare the vintage as of September 30, 2026 with today, and manually read three observations from the FRED page against the displayed current-series chart.

### Manual FRED page check

On October 29, 2026, the FRED page showed these three daily-close observations:

| Date | OAS value (percent) |
|---|---:|
| October 28, 2026 | 0.86 |
| October 27, 2026 | 0.88 |
| October 26, 2026 | 0.90 |

These values should be checked directly against the FRED page and the app's current-series chart at checkout.

## Real-time-vintage result and Project 2 call

With the app set to an as-known-on date of September 30, 2026, the latest known `BAMLC0A0CM` observation was September 30 at **0.84%**. As of October 29, the current FRED file extended through October 28 at **0.86%**: it had 20 later observations, and the app's shared-date comparison found **0 revised values** for this particular vintage test.

**Call: admit, with a point-in-time condition.** `BAMLC0A0CM` is an economically relevant external credit-spread signal for LQD, and this test shows a roughly next-business-day publication pattern with no revisions in the tested September 30 vintage. Project 2 may use it only after the value was published and only from the ALFRED vintage available on each decision date—not by inserting today's FRED history into an earlier trade-date analysis. Quarantine it if a future vintage comparison reveals material revisions, if the decision precedes the series' publication, or if the three-year available history is too short for the intended analysis; those conditions would require a different source or a longer-history proxy.

## Partner attack

**Allie's attack:** “Could you create a better way to see the market effects on the different series?”

**Response:** I added a combined, high-contrast chart and a normalized comparison so the four series can be compared over time even when their levels overlap. I also added line, bar, and candlestick-style views for each individual series; because FRED supplies one rate observation rather than true intraday OHLC data, the candle view uses the prior observation as the open and the current observation as the close, with the endpoints as its high and low.

## Known-answer and revision proof

With the app's **as known on** control set to October 5, 2026, the FRED/ALFRED downloads reproduced these known values:

| Series | Last date known on October 5 | Value known then | Later current values | Revisions on shared dates |
|---|---|---:|---:|---:|
| BAA | September 1, 2026 | 6.47 | 0 | 0 |
| FEDFUNDS | September 1, 2026 | 3.75 | 0 | 0 |
| DGS10 | October 2, 2026 | 5.28 | 16 | 0 |
| MORTGAGE30US | October 1, 2026 | 7.28 | 4 | 0 |

The different last-known dates are the point-in-time result: the daily Treasury series had data through October 2, the weekly mortgage series through October 1, and the monthly series through September. The late-count column measures current observations after the date available in the October 5 vintage; it is not a return or a forecast.

### PAYEMS revision probe

Set the custom series ID to `PAYEMS` and **as known on** to January 10, 2025. The app's vintage series has December 1, 2024 employment at **159,536** (thousand persons); the same December observation is **158,316** in the current FRED file, a reduction of **1,220**. The app identifies 381 revised shared dates in that vintage comparison. This demonstrates why a historical Project 2 analysis must use the ALFRED vintage available at the decision date rather than a current-data download.
