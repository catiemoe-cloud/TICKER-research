"""Five-year FCFF discounted cash flow model (USD millions)."""

# Apple inputs (USD millions, except per-share values and rates).
# Financial-statement inputs are from Apple's Q3 FY2026 Form 10-Q.
STARTING_FCFF = 131000.0  # TTM estimated FCFF; derived from operating cash flow, capex, and SBC.
GROWTH_RATES = [0.07, 0.07, 0.07, 0.07, 0.07]  # Analyst assumption.
WACC = 0.08  # Analyst assumption.
TERMINAL_GROWTH = 0.03  # Analyst assumption.
NON_OPERATING_CASH = 146517.0  # Cash plus current and non-current marketable securities.
DEBT = 84344.0  # Commercial paper plus current and non-current term debt.
DILUTED_SHARES = 14594.18  # Shares outstanding as of July 17, 2026.

# Sensitivity and reverse-DCF inputs: edit these values as needed.
SENSITIVITY_WACCS = [0.07, 0.08, 0.09]
SENSITIVITY_TERMINAL_GROWTHS = [0.02, 0.03, 0.04]
TARGET_SHARE_PRICE = 315.34
REVERSE_SHIFT_LOWER = -0.05
REVERSE_SHIFT_UPPER = 0.10
CASE_LABEL = "Apple"


def value_per_diluted_share(wacc, terminal_growth, growth_rates):
    """Return the DCF value per share, or None for an invalid terminal rate."""
    if terminal_growth >= wacc:
        return None

    fcff = STARTING_FCFF
    present_value_explicit_fcff = 0.0
    for year, growth_rate in enumerate(growth_rates, start=1):
        fcff *= 1.0 + growth_rate
        present_value_explicit_fcff += fcff / (1.0 + wacc) ** year

    terminal_value_year_5 = fcff * (1.0 + terminal_growth) / (wacc - terminal_growth)
    present_value_terminal_value = terminal_value_year_5 / (1.0 + wacc) ** 5
    enterprise_value = present_value_explicit_fcff + present_value_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    return equity_value / DILUTED_SHARES


def print_sensitivity_grid():
    print(f"Sensitivity Grid ({CASE_LABEL} Result): Value per Diluted Share")
    header = ["WACC \\ Terminal Growth"] + [
        f"{terminal_growth:.0%}" for terminal_growth in SENSITIVITY_TERMINAL_GROWTHS
    ]
    print(" | ".join(f"{column:>22}" for column in header))

    for wacc in SENSITIVITY_WACCS:
        row = [f"{wacc:.0%}"]
        for terminal_growth in SENSITIVITY_TERMINAL_GROWTHS:
            value = value_per_diluted_share(wacc, terminal_growth, GROWTH_RATES)
            row.append("invalid" if value is None else f"{value:.2f}")
        print(" | ".join(f"{column:>22}" for column in row))


def print_reverse_dcf():
    if any(growth + REVERSE_SHIFT_LOWER <= -1.0 for growth in GROWTH_RATES) or any(
        growth + REVERSE_SHIFT_UPPER <= -1.0 for growth in GROWTH_RATES
    ):
        print("Reverse DCF: no solution; the bracket creates annual growth of -100% or below.")
        return

    def price_difference(shift):
        shifted_growth_rates = [growth + shift for growth in GROWTH_RATES]
        return (
            value_per_diluted_share(WACC, TERMINAL_GROWTH, shifted_growth_rates)
            - TARGET_SHARE_PRICE
        )

    lower = REVERSE_SHIFT_LOWER
    upper = REVERSE_SHIFT_UPPER
    lower_difference = price_difference(lower)
    upper_difference = price_difference(upper)

    if lower_difference * upper_difference > 0.0:
        print("Reverse DCF: no solution in the specified bracket.")
        print(f"Target Price: {TARGET_SHARE_PRICE:.4f}")
        print(
            "Held Fixed: STARTING_FCFF, WACC, TERMINAL_GROWTH, "
            "NON_OPERATING_CASH, DEBT, DILUTED_SHARES"
        )
        return

    for _ in range(100):
        midpoint = (lower + upper) / 2.0
        midpoint_difference = price_difference(midpoint)
        if abs(midpoint_difference) < 1e-10:
            break
        if lower_difference * midpoint_difference < 0.0:
            upper = midpoint
        else:
            lower = midpoint
            lower_difference = midpoint_difference

    print(f"Reverse DCF ({CASE_LABEL} Result)")
    print(f"Solved Uniform Growth Shift: {midpoint * 100.0:.4f} percentage points")
    print(f"Target Price: {TARGET_SHARE_PRICE:.4f}")
    print(
        "Held Fixed: STARTING_FCFF, WACC, TERMINAL_GROWTH, "
        "NON_OPERATING_CASH, DEBT, DILUTED_SHARES"
    )


def main():
    if TERMINAL_GROWTH >= WACC:
        print("Error: terminal growth must be less than WACC.")
        return

    fcff = STARTING_FCFF
    present_value_explicit_fcff = 0.0

    for year, growth_rate in enumerate(GROWTH_RATES, start=1):
        fcff *= 1.0 + growth_rate
        print(f"FCFF Year {year}: {fcff:.4f}")
        present_value_explicit_fcff += fcff / (1.0 + WACC) ** year

    terminal_value_year_5 = fcff * (1.0 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    present_value_terminal_value = terminal_value_year_5 / (1.0 + WACC) ** 5
    enterprise_value = present_value_explicit_fcff + present_value_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    value_per_diluted_share = equity_value / DILUTED_SHARES
    terminal_value_share_of_enterprise_value = present_value_terminal_value / enterprise_value

    print(f"PV Explicit FCFF: {present_value_explicit_fcff:.4f}")
    print(f"Terminal Value at Year 5: {terminal_value_year_5:.4f}")
    print(f"PV Terminal Value: {present_value_terminal_value:.4f}")
    print(f"Enterprise Value: {enterprise_value:.4f}")
    print(f"Equity Value: {equity_value:.4f}")
    print(f"Value per Diluted Share: {value_per_diluted_share:.4f}")
    print(
        "PV Terminal Value / Enterprise Value: "
        f"{terminal_value_share_of_enterprise_value:.4f}"
    )
    print_sensitivity_grid()
    print_reverse_dcf()


if __name__ == "__main__":
    main()
