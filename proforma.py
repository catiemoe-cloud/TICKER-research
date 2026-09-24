"""Five-year ABG pro forma and FCFE valuation (USD millions, except per-share data)."""

YEARS = [2026, 2027, 2028, 2029, 2030]
opening = {"revenue": 17_999.0, "inventory": 2_135.8, "ppe": 3_070.4,
           "other_assets": 6_371.6, "cash": 40.4, "floor_plan": 2_027.0,
           "debt": 3_572.0, "revolver": 0.0, "other_liabilities": 2_127.5,
           "equity": 3_891.7}
growth, gross_margin = 0.018, 0.1705
sga_ratios = [0.665, 0.655, 0.645, 0.645, 0.645]
depreciation_ratio = 82.4 / 3_070.4
impairment, capex, tax_rate = 120.0, 250.0, 0.255
inventory_days = 2_135.8 / (17_999.0 - 3_071.7) * 365
floor_plan_ratio, other_wc_rate = 2_027.0 / 2_135.8, 0.008
minimum_cash, revolver_limit, revolver_rate = 25.0, 850.0, 0.06
debt_repayment, buyback = 150.0, 150.0
floor_plan_rate, debt_rate = 0.0467, 0.0544
cost_of_equity, terminal_growth, shares_outstanding = 0.10, 0.025, 17.951349


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


result = {key: {} for key in (
    "revenue gross_profit sga depreciation impairment operating_income interest pretax tax net_income "
    "inventory ppe other_assets cash floor_plan debt revolver other_liabilities equity "
    "fcfe balance_gap cash_check").split()}
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
        repayment = min(revolver, cash_before_financing - minimum_cash)
        revolver -= repayment
        cash = cash_before_financing - repayment
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

print_statement("Income Statement", [
    ("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"),
    ("Depreciation", "depreciation"), ("Impairment", "impairment"),
    ("Operating income", "operating_income"), ("Interest", "interest"),
    ("Pretax income", "pretax"), ("Tax", "tax"), ("Net income", "net_income")])
print_statement("Balance Sheet", [
    ("Inventory", "inventory"), ("PP&E", "ppe"), ("Other assets", "other_assets"),
    ("Cash", "cash"), ("Floor plan", "floor_plan"), ("Term debt", "debt"),
    ("Revolver", "revolver"), ("Other liabilities", "other_liabilities"), ("Equity", "equity")])
print_statement("Cash Flow", [("Free cash flow to equity", "fcfe")])
print_statement("Checks", [("Assets - liabilities - equity", "balance_gap"),
                           ("Cash at or above minimum", "cash_check")])
pv_fcfe = sum(result["fcfe"][year] / (1 + cost_of_equity) ** i
              for i, year in enumerate(YEARS, start=1))
terminal_value = ((result["fcfe"][2030] + debt_repayment) * (1 + terminal_growth)
                  / (cost_of_equity - terminal_growth))
pv_terminal = terminal_value / (1 + cost_of_equity) ** len(YEARS)
equity_value = pv_fcfe + pv_terminal
print(f"\nEquity value: ${equity_value:,.1f} million")
print(f"Share of value after 2030: {pv_terminal / equity_value:.1%}")
print(f"Value per share: ${equity_value / shares_outstanding:,.2f}")
