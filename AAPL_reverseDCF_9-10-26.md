# Apple Reverse DCF — September 10, 2026

## Scope and convention

This is a five-year FCFF DCF in USD millions. FCFF occurs at each year end; the Gordon-growth terminal value is measured at the end of Year 5 and discounted five years to today. Equity value equals enterprise value plus non-operating cash less debt, divided by diluted shares.

This is an educational valuation exercise, not investment advice.

## Sources and inputs

Apple's [Q3 FY2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/320193/000032019326000020/aapl-20260627.htm) reports nine-month operating cash flow of $116,996 million and capital expenditures of $6,799 million. The same filing reports $39,544 million cash, $22,855 million current marketable securities, $84,118 million non-current marketable securities, $1,997 million commercial paper, $11,007 million current term debt, $71,340 million non-current term debt, and 14,594.18 million shares outstanding as of July 17, 2026.

| Input | Value | Basis |
|---|---:|---|
| Starting FCFF | $131,000M | Estimated trailing-twelve-month FCFF from operating cash flow, capex, and stock-based compensation; rounded. |
| Year 1–5 FCFF growth | 7.0% each year | Analyst assumption. |
| WACC | 8.0% | Analyst assumption. |
| Terminal growth | 3.0% | Analyst assumption. |
| Non-operating cash | $146,517M | Cash plus marketable securities from the 10-Q. |
| Debt | $84,344M | Commercial paper plus term debt from the 10-Q. |
| Diluted shares | 14,594.18M | Shares outstanding from the 10-Q. |
| Target / market price | $315.34 | Observed September 10, 2026 market quote. [Price source](https://www.financialcontent.com/quote/NQ%3AAAPL/historical) |

## Base-case DCF

Running `python3 dcf.py` produces a base-case value of **$224.42 per diluted share**. The base case applies 7% FCFF growth for five years, then 3% terminal growth, discounted at 8% WACC.

The terminal value is discounted five years—not six—because it is the value at the end of Year 5 of all cash flows beginning in Year 6.

## Sensitivity grid — value per diluted share

| WACC \ terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 7% | $232.26 | $280.28 | $360.32 |
| 8% | $193.57 | $224.42 | $270.68 |
| 9% | $165.96 | $187.19 | $216.92 |

The base case is the center cell. Value falls as WACC rises and rises as terminal growth rises. The two opposite corners are $165.96 and $360.32 per share.

## Reverse DCF

At the $315.34 target price, the reverse DCF solves for a **+8.2837 percentage-point** uniform shift to all five explicit FCFF growth rates. This changes each 7.0% annual FCFF-growth assumption to approximately **15.2837%**.

The reverse DCF holds starting FCFF, WACC, terminal growth, non-operating cash, debt, and diluted shares fixed. Its bracket is −5 to +10 percentage points; it rejects a bracket that would cause any annual growth rate to be −100% or lower, and reports no solution if the target is unreachable within the bracket.

## Conditional call

**Watch—defer.** The base DCF value is $224.42 per share, below the observed $315.34 price. Initiate if the price falls below roughly $224 without a deterioration in the cash-flow outlook, or if sourced evidence supports a durable increase in the FCFF-growth path from 7% toward the roughly 15.3% growth implied by the target price. Otherwise, defer.

**Monitor:** operating margin in the next quarterly results. Sustained margin expansion would be evidence relevant to the higher FCFF growth implied by the market price.

The reverse-DCF growth requirement is a statement of what the model requires under its fixed assumptions; it is not proof that the stock is mispriced.

## Commands and files

Run the complete Apple base DCF, sensitivity grid, and reverse DCF with:

```bash
python3 dcf.py
```

The editable inputs and calculation logic are in `dcf.py`; this document records the Apple case and the completed analysis.
