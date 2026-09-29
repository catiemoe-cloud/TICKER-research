"""Lab 10 one-at-a-time sensitivity analysis for the Apple pro forma."""

import argparse
from copy import deepcopy

YEARS = [2026, 2027, 2028, 2029, 2030]
BASE = {
    "growth": 0.05, "gross_margin": 0.465, "sga_ratio": 0.14,
    "depreciation_ratio": 11_698 / 45_680, "impairment": 0.0,
    "capex": 12_000.0, "tax_rate": 0.18,
    "inventory_days": 5_718 / 220_960 * 365, "floor_plan_ratio": 0.0,
    "other_wc_rate": 0.0, "minimum_cash": 25_000.0,
    "revolver_limit": 100_000.0, "revolver_rate": 0.05,
    "debt_repayment": 5_000.0, "buyback": 85_000.0,
    "floor_plan_rate": 0.0, "debt_rate": 0.045,
    "cost_of_equity": 0.08, "terminal_growth": 0.03,
    "shares": 14_773.260,
    "opening": {"revenue": 416_161.0, "inventory": 5_718.0, "ppe": 49_834.0,
                "other_assets": 267_755.0, "cash": 35_934.0, "floor_plan": 0.0,
                "debt": 98_657.0, "revolver": 0.0, "other_liabilities": 186_851.0,
                "equity": 73_733.0},
}

DRIVERS = {
    "Revenue growth": ("growth", [("Lower", 0.03), ("Base", 0.05), ("Higher", 0.07)], "% annually, FY2026E-FY2030E"),
    "Gross margin": ("gross_margin", [("Lower", 0.455), ("Base", 0.465), ("Higher", 0.475)], "% of revenue, FY2026E-FY2030E"),
}


def run_model(inputs):
    """Run a fresh linked model and return traceable FY2030 outputs and checks."""
    prior, years = deepcopy(inputs["opening"]), {}
    valid, note = True, "Pass"
    for year in YEARS:
        revenue = prior["revenue"] * (1 + inputs["growth"])
        gross_profit = revenue * inputs["gross_margin"]
        sga = gross_profit * inputs["sga_ratio"]
        depreciation = prior["ppe"] * inputs["depreciation_ratio"]
        operating_income = gross_profit - sga - depreciation - inputs["impairment"]
        interest = (prior["floor_plan"] * inputs["floor_plan_rate"] + prior["debt"] * inputs["debt_rate"]
                    + prior["revolver"] * inputs["revolver_rate"])
        pretax = operating_income - interest
        tax = max(0.0, pretax) * inputs["tax_rate"]
        net_income = pretax - tax
        inventory = (revenue - gross_profit) * inputs["inventory_days"] / 365
        floor_plan = inventory * inputs["floor_plan_ratio"]
        ppe = prior["ppe"] + inputs["capex"] - depreciation
        other_assets = prior["other_assets"] + inputs["other_wc_rate"] * (revenue - prior["revenue"]) - inputs["impairment"]
        debt = prior["debt"] - inputs["debt_repayment"]
        equity = prior["equity"] + net_income - inputs["buyback"]
        fcfe = (net_income + depreciation + inputs["impairment"] - inputs["capex"]
                - (inventory - prior["inventory"]) - inputs["other_wc_rate"] * (revenue - prior["revenue"])
                + (floor_plan - prior["floor_plan"]) - inputs["debt_repayment"])
        cash_before = prior["cash"] + fcfe - inputs["buyback"]
        revolver = prior["revolver"]
        if cash_before < inputs["minimum_cash"]:
            draw = inputs["minimum_cash"] - cash_before
            if revolver + draw > inputs["revolver_limit"]:
                valid, note = False, f"FY{year}E revolver limit exceeded"
            revolver += draw
            cash = inputs["minimum_cash"]
        else:
            draw = 0.0
            repayment = min(revolver, cash_before - inputs["minimum_cash"])
            revolver -= repayment
            cash = cash_before - repayment
        gap = inventory + ppe + other_assets + cash - floor_plan - debt - revolver - prior["other_liabilities"] - equity
        if abs(gap) > 0.05 or cash < inputs["minimum_cash"] - 0.05:
            valid, note = False, f"FY{year}E check failed: gap {gap:.1f}, cash {cash:.1f}"
        years[year] = {"operating_income": operating_income, "fcfe": fcfe, "cash": cash, "gap": gap, "draw": draw}
        prior = {"revenue": revenue, "inventory": inventory, "ppe": ppe, "other_assets": other_assets,
                 "cash": cash, "floor_plan": floor_plan, "debt": debt, "revolver": revolver,
                 "other_liabilities": prior["other_liabilities"], "equity": equity}
    pv_fcfe = sum(years[y]["fcfe"] / (1 + inputs["cost_of_equity"]) ** n for n, y in enumerate(YEARS, 1))
    terminal = ((years[2030]["fcfe"] + inputs["debt_repayment"]) * (1 + inputs["terminal_growth"])
                / (inputs["cost_of_equity"] - inputs["terminal_growth"]))
    value_per_share = (pv_fcfe + terminal / (1 + inputs["cost_of_equity"]) ** 5) / inputs["shares"]
    return {"valid": valid, "note": note, "years": years, "value": value_per_share}


def print_driver(name, key, cases, units):
    runs = []
    for label, value in cases:
        inputs = deepcopy(BASE)
        inputs[key] = value
        output = run_model(inputs)
        runs.append((label, value, output))
    base = next(output for label, _, output in runs if label == "Base")
    print(f"\n{name} sensitivity ({units})")
    print("Case       Input       FY2030E operating income ($M)  FY2030E FCFE ($M)  Value/share ($)  Checks")
    for label, value, output in runs:
        y = output["years"][2030]
        change = "" if label == "Base" else f"; changes: OI {y['operating_income'] - base['years'][2030]['operating_income']:+.1f}, FCFE {y['fcfe'] - base['years'][2030]['fcfe']:+.1f}, value {output['value'] - base['value']:+.2f}"
        print(f"{label:<11}{value:>6.1%}  {y['operating_income']:>27.1f}  {y['fcfe']:>18.1f}  {output['value']:>15.2f}  {output['note']}{change}")
    for metric, getter, digits in (("operating income", lambda x: x["years"][2030]["operating_income"], 1),
                                   ("FCFE", lambda x: x["years"][2030]["fcfe"], 1),
                                   ("value per share", lambda x: x["value"], 2)):
        values = [getter(output) for _, _, output in runs if output["valid"]]
        print(f"Output span, {metric}: {max(values) - min(values):.{digits}f}")
    return base


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true", help="Run only after partner confirmation.")
    args = parser.parse_args()
    if not args.run:
        print("Sensitivity runner is ready. Obtain and record partner confirmation, then run: python3 apple_lab10_sensitivity.py --run")
    else:
        first_base = run_model(deepcopy(BASE))
        for name, (key, cases, units) in DRIVERS.items():
            print_driver(name, key, cases, units)
        restored_base = run_model(deepcopy(BASE))
        print("\nRestored-base check:", "Pass" if first_base == restored_base else "FAIL")
