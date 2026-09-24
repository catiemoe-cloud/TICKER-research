"""Five-year Apple pro forma and FCFE valuation (USD millions, except per-share data)."""

YEARS = [2026, 2027, 2028, 2029, 2030]

# FY2025 opening balance sheet. Other assets/liabilities aggregate the remaining
# reported balance-sheet lines so the simplified model starts balanced.
opening = {
    "revenue": 416_161.0,
    "inventory": 5_718.0,
    "ppe": 49_834.0,
    "other_assets": 267_755.0,
    "cash": 35_934.0,
    "floor_plan": 0.0,  # Apple has no floor-plan equivalent.
    "debt": 98_657.0,  # Commercial paper plus current and non-current term debt.
    "revolver": 0.0,
    "other_liabilities": 186_851.0,
    "equity": 73_733.0,
}

# Assumptions: history ratios use FY2025 data; the remaining inputs are judgments.
growth = 0.05
gross_margin = 0.465
sga_ratios = [0.14] * 5
depreciation_ratio = 11_698.0 / 45_680.0  # FY2025 D&A / FY2024 PP&E.
impairment = 0.0
capex = 12_000.0
tax_rate = 0.18
inventory_days = 5_718.0 / 220_960.0 * 365
floor_plan_ratio = 0.0
other_wc_rate = 0.0
minimum_cash, revolver_limit, revolver_rate = 25_000.0, 100_000.0, 0.05
debt_repayment = 5_000.0
buyback = 85_000.0
floor_plan_rate, debt_rate = 0.0, 0.045
cost_of_equity, terminal_growth = 0.08, 0.03
shares_outstanding = 14_773.260

ASSUMPTION_SET = [
    ("Revenue growth", "5.0%", "judgment", "Below FY2025's rebound, but allows continued Services and product growth."),
    ("Gross margin", "46.5%", "judgment", "Near the FY2024-FY2025 range while allowing for mix, FX and tariff pressure."),
    ("SG&A / gross profit", "14.0%", "judgment", "Close to FY2025's 14.1%; scale should limit SG&A growth relative to gross profit."),
    ("D&A / opening PP&E", "25.61%", "history", "FY2025 reported D&A divided by FY2024 ending PP&E."),
    ("Impairment", "$0", "judgment", "Apple did not report a recurring annual impairment charge in the three 10-Ks."),
    ("Capital spending", "$12.0bn", "judgment", "Near the recent filed annual range of $9.4bn to $12.7bn."),
    ("Tax rate", "18.0%", "judgment", "Normalizes the three-year effective tax-rate range instead of using one unusual year."),
    ("Inventory days", "9.45 days", "history", "FY2025 ending inventory divided by FY2025 cost of sales times 365."),
    ("Floor-plan equivalent", "None / 0%", "history", "Apple has no disclosed dealer-style inventory financing; no such liability or financing-cash-flow offset is modeled."),
    ("Other working capital", "0% of revenue change", "judgment", "Apple's other working-capital balances moved unevenly, so the base case holds them flat."),
    ("Minimum cash", "$25.0bn", "judgment", "Keeps a meaningful liquidity cushion below Apple's FY2025 cash balance."),
    ("Revolver limit / rate", "$100.0bn / 5.0%", "judgment", "A model safeguard using a conservative borrowing cost; it is not a reported facility."),
    ("Debt repayment", "$5.0bn annually", "judgment", "Uses a modest ongoing reduction rather than assuming refinancing or full repayment."),
    ("Share buyback", "$85.0bn annually", "judgment", "Near Apple's recent annual repurchase pace while remaining below FY2025's $90.7bn."),
    ("Debt interest rate", "4.5%", "judgment", "A simplified blended rate for commercial paper and term debt."),
    ("Cost of equity", "8.0%", "judgment", "The base discount rate used in the Apple DCF sensitivity analysis."),
    ("Terminal growth", "3.0%", "judgment", "Below the explicit growth rate and intended to represent mature long-run growth."),
    ("Shares outstanding", "14.773bn", "history", "FY2025 year-end shares outstanding from the 10-K."),
]

FILING_SOURCES = {
    "FY25 Ops": "FY2025 10-K, Consolidated Statements of Operations: https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm",
    "FY25 CF": "FY2025 10-K, Consolidated Statements of Cash Flows: https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm",
    "FY25 BS": "FY2025 10-K, Consolidated Balance Sheets: https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm",
    "FY25 Eq": "FY2025 10-K, Consolidated Statements of Shareholders' Equity: https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm",
    "FY24 BS": "FY2024 10-K, Consolidated Balance Sheets: https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm",
    "MD&A": "FY2025/FY2024/FY2023 10-K MD&A; Apple reports product and geographic sales, not organic or same-store growth.",
}

HISTORY_GRID = [
    ("Revenue", "383,285", "391,035", "416,161", "FY25 Ops"),
    ("Gross profit", "169,148", "180,683", "195,201", "FY25 Ops"),
    ("SG&A", "24,932", "26,097", "27,601", "FY25 Ops"),
    ("Net income", "96,995", "93,736", "112,010", "FY25 Ops"),
    ("Inventory", "6,331", "7,286", "5,718", "FY24 BS / FY25 BS"),
    ("PP&E, net", "43,715", "45,680", "49,834", "FY24 BS / FY25 BS"),
    ("Shareholders' equity", "62,146", "56,950", "73,733", "FY25 Eq"),
]

RATIO_GRID = [
    ("Reported revenue growth", "-2.8%", "2.0%", "6.4%", "Revenue / prior-year revenue - 1; FY25 Ops"),
    ("Organic / same-store growth", "Not disclosed", "Not disclosed", "Not disclosed", "MD&A"),
    ("Gross margin", "44.13%", "46.21%", "46.91%", "Gross profit / revenue; FY25 Ops"),
    ("SG&A / gross profit", "14.74%", "14.44%", "14.14%", "SG&A / gross profit; FY25 Ops"),
    ("Inventory days", "10.79", "12.64", "9.45", "Ending inventory / cost of sales * 365; FY24 BS / FY25 BS"),
    ("D&A / opening PP&E", "27.35%", "26.18%", "25.61%", "Reported D&A / prior year-end PP&E; FY25 CF / FY24 BS"),
    ("Capital spending, filed", "10,959", "9,447", "12,715", "PP&E acquisition payments; FY25 CF"),
    ("Capital spending, data provider", "Unresolved", "Unresolved", "Unresolved", "No data-provider field was supplied for comparison."),
    ("Effective tax rate", "14.72%", "24.09%", "15.61%", "Tax provision / pretax income; FY25 Ops"),
]

MARKET_PRICE = 336.36
MARKET_PRICE_DATE = "September 24, 2026"
MARKET_PRICE_SOURCE = "Yahoo Finance AAPL historical prices: https://finance.yahoo.com/quote/AAPL/history/"

# Partner challenge
# Question: Why did you pick 5% revenue growth when Apple's growth has been all
# over the place?
# Answer: I picked 5% because it is below the recent rebound but still assumes
# Apple can grow through Services and new products. I would change it if upcoming
# results show iPhone demand or China sales are consistently stronger or weaker.
#
# Attaking Partners Company
# Question: Why did you assume Chipotle can keep growing same-store sales at that
# rate when customers might cut back on eating out if the economy slows down?
# Response: I used that rate because Chipotle has had strong pricing power
# and customer traffic, but I would lower it if traffic starts falling or management
# says consumers are spending less.


def assert_balanced(year, gap, cash):
    """Reject a forecast year whose balance sheet does not balance or lacks cash."""
    if abs(gap) > 0.05:
        raise AssertionError(f"FY{year}E is not balanced: gap {gap:.1f}")
    if cash < minimum_cash - 0.05:
        raise AssertionError(f"FY{year}E cash is below the minimum: {cash:.1f}")


def print_statement(title, rows):
    print(f"\n{title}")
    print(f"{'USD millions':<30}" + "".join(f"FY{y}E".rjust(12) for y in YEARS))
    for label, key in rows:
        print(f"{label:<30}" + "".join(f"{result[key][y]:>12.1f}" for y in YEARS))


def print_assumption_set():
    print("\nAssumption Set")
    print(f"{'Assumption':<28}{'Value':<24}{'Label':<12}Reason")
    for assumption, value, label, reason in ASSUMPTION_SET:
        print(f"{assumption:<28}{value:<24}{label:<12}{reason}")
    print("\nPartner Attack")
    print("Question: Why did you pick 5% revenue growth when Apple's growth has been all over the place?")
    print("Answer: I picked 5% because it is below the recent rebound but still assumes Apple can grow through Services and new products.")
    print("I would change it if upcoming results show iPhone demand or China sales are consistently stronger or weaker.")


def print_history_and_ratios():
    print("\nThree-Year History (USD millions)")
    print(f"{'Item':<28}{'FY2023':>12}{'FY2024':>12}{'FY2025':>12}  Source")
    for item, fy23, fy24, fy25, source in HISTORY_GRID:
        print(f"{item:<28}{fy23:>12}{fy24:>12}{fy25:>12}  {source}")
    print("Sources:")
    for name, source in FILING_SOURCES.items():
        print(f"  {name}: {source}")

    print("\nThree-Year Ratios")
    print(f"{'Ratio':<30}{'FY2023':>14}{'FY2024':>14}{'FY2025':>14}  Calculation / source")
    for ratio, fy23, fy24, fy25, source in RATIO_GRID:
        print(f"{ratio:<30}{fy23:>14}{fy24:>14}{fy25:>14}  {source}")


result = {key: {} for key in (
    "revenue gross_profit sga depreciation impairment operating_income interest pretax tax net_income "
    "inventory ppe other_assets cash floor_plan debt revolver other_liabilities equity "
    "fcfe balance_gap cash_check revolver_draw"
).split()}

prior = opening.copy()
for year, sga_ratio in zip(YEARS, sga_ratios):
    revenue = prior["revenue"] * (1 + growth)
    gross_profit = revenue * gross_margin
    sga = gross_profit * sga_ratio
    depreciation = prior["ppe"] * depreciation_ratio
    operating_income = gross_profit - sga - depreciation - impairment
    interest = (prior["floor_plan"] * floor_plan_rate + prior["debt"] * debt_rate
                + prior["revolver"] * revolver_rate)
    pretax = operating_income - interest
    tax = max(0.0, pretax) * tax_rate
    net_income = pretax - tax

    inventory = (revenue - gross_profit) * inventory_days / 365
    floor_plan = inventory * floor_plan_ratio
    ppe = prior["ppe"] + capex - depreciation
    other_assets = prior["other_assets"] + other_wc_rate * (revenue - prior["revenue"]) - impairment
    debt = prior["debt"] - debt_repayment
    other_liabilities = prior["other_liabilities"]
    equity = prior["equity"] + net_income - buyback

    change_inventory = inventory - prior["inventory"]
    change_other_wc = other_wc_rate * (revenue - prior["revenue"])
    change_floor_plan = floor_plan - prior["floor_plan"]
    fcfe = (net_income + depreciation + impairment - capex - change_inventory
            - change_other_wc + change_floor_plan - debt_repayment)
    cash_before_financing = prior["cash"] + fcfe - buyback
    revolver = prior["revolver"]
    if cash_before_financing < minimum_cash:
        draw = minimum_cash - cash_before_financing
        if revolver + draw > revolver_limit:
            raise AssertionError(f"FY{year}E revolver limit exceeded")
        revolver += draw
        cash = minimum_cash
    else:
        draw = 0.0
        repayment = min(revolver, cash_before_financing - minimum_cash)
        revolver -= repayment
        cash = cash_before_financing - repayment

    revolver_draw = draw
    values = locals()
    for key in result:
        if key in values:
            result[key][year] = values[key]
    assets = inventory + ppe + other_assets + cash
    liabilities_and_equity = floor_plan + debt + revolver + other_liabilities + equity
    result["balance_gap"][year] = assets - liabilities_and_equity
    result["cash_check"][year] = cash
    assert_balanced(year, result["balance_gap"][year], cash)
    prior = {key: values[key] for key in opening}

print_history_and_ratios()
print_assumption_set()
print_statement("Income Statement", [
    ("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"),
    ("Depreciation and amortization", "depreciation"), ("Impairment", "impairment"),
    ("Operating income", "operating_income"), ("Interest", "interest"),
    ("Pretax income", "pretax"), ("Tax", "tax"), ("Net income", "net_income"),
])
print_statement("Balance Sheet", [
    ("Inventory", "inventory"), ("PP&E", "ppe"), ("Other assets", "other_assets"),
    ("Cash", "cash"), ("Floor plan equivalent", "floor_plan"), ("Debt", "debt"),
    ("Revolver", "revolver"), ("Other liabilities", "other_liabilities"), ("Equity", "equity"),
])
print_statement("Cash Flow", [("Free cash flow to equity", "fcfe")])
print_statement("Checks", [
    ("Assets - liabilities - equity", "balance_gap"), ("Cash at or above minimum", "cash_check"),
])

draw_years = [(year, result["revolver_draw"][year]) for year in YEARS
              if result["revolver_draw"][year] > 0]
if draw_years:
    for year, draw in draw_years:
        print(f"FY{year}E revolver draw: {draw:.1f}; cash would otherwise fall below the minimum.")
else:
    print("Revolver note: no year draws the revolver because FCFE covers capital spending, debt repayment and buybacks.")

pv_fcfe = sum(result["fcfe"][year] / (1 + cost_of_equity) ** i
              for i, year in enumerate(YEARS, start=1))
terminal_value = ((result["fcfe"][2030] + debt_repayment) * (1 + terminal_growth)
                  / (cost_of_equity - terminal_growth))
pv_terminal = terminal_value / (1 + cost_of_equity) ** len(YEARS)
equity_value = pv_fcfe + pv_terminal
print(f"\nEquity value: ${equity_value:,.1f} million")
print(f"Share of value after 2030: {pv_terminal / equity_value:.1%}")
print(f"Value per share: ${equity_value / shares_outstanding:,.2f}")
print(
    f"Market comparison: on the same {shares_outstanding / 1_000:.3f} billion-share basis, "
    f"the model says ${equity_value / shares_outstanding:,.2f} per share while the market says "
    f"${MARKET_PRICE:.2f} on {MARKET_PRICE_DATE}; what future cash-flow or terminal-value "
    "assumption is the market making that this model is not?"
)
print(f"Market-price source: {MARKET_PRICE_SOURCE}")
