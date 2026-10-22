"""Streamlit client page for FIN 43900 Lab 15. Run: streamlit run app.py"""

import streamlit as st

from portfolio import (
    CORRELATIONS,
    OBJECTIVE_RETURN,
    RESERVE_ELIGIBLE,
    SLEEVES,
    estimate_from_monthly_prices,
    search_long_only_mix,
)


def format_result(result):
    if result is None:
        st.error("No mix meets the objective and reserve requirement at 5-point steps.")
        return
    weights = [
        {"Asset": asset, "Weight": f"{weight:.2%}"}
        for asset, weight in result["weights"].items()
    ]
    st.dataframe(weights, hide_index=True, use_container_width=True)
    first, second, third = st.columns(3)
    first.metric("Expected return estimate", f"{result['expected_return']:.2%}")
    second.metric("Volatility estimate", f"{result['volatility']:.2%}")
    third.metric("Reserve-eligible weight", f"{result['reserve_weight']:.2%}")


def largest_weight_change(base, current):
    if base is None or current is None:
        return "Not available because one result has no feasible mix."
    asset, change = max(
        (
            (asset, current["weights"][asset] - base["weights"][asset])
            for asset in base["weights"]
        ),
        key=lambda item: abs(item[1]),
    )
    return f"Largest weight change: {asset}, {change:+.1%} ({change * 100:+.1f} points)."


st.set_page_config(page_title="Lab 15 Portfolio Builder", layout="wide")
st.title("Lab 15 Portfolio Builder")
st.caption("Built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    st.header("Mandate and data")
    objective_percent = st.number_input(
        "Minimum expected return (%)", min_value=-50.0, max_value=50.0,
        value=OBJECTIVE_RETURN * 100, step=0.5, format="%.1f",
    )
    minimum_reserve_percent = st.number_input(
        "Minimum reserve-eligible weight (%)", min_value=0.0, max_value=100.0,
        value=3.0, step=0.5, format="%.1f",
    )
    uploaded_file = st.file_uploader("Upload prices.csv", type="csv")
    last_36_months = st.toggle("Use only the last 36 monthly returns", value=False)

try:
    if uploaded_file is None:
        loaded_sleeves = {asset: details.copy() for asset, details in SLEEVES.items()}
        loaded_correlations = CORRELATIONS
        data_label = "Meridian course inputs as loaded"
        st.info("Showing Meridian inputs. Upload a CSV to use your three-to-six-fund universe.")
    else:
        all_months = estimate_from_monthly_prices(uploaded_file, last_36_months=False)
        uploaded_file.seek(0)
        selected_period = estimate_from_monthly_prices(uploaded_file, last_36_months=last_36_months)
        loaded_sleeves = selected_period["sleeves"]
        loaded_correlations = selected_period["correlations"]
        data_label = (
            f"CSV estimate: {selected_period['months_used']} monthly returns "
            f"from {selected_period['first_date']} to {selected_period['last_date']}"
        )
except ValueError as error:
    st.error(f"Could not use this CSV: {error}")
    st.stop()

st.write(data_label)
st.caption("Expected returns are historical arithmetic-mean estimates (monthly mean × 12), not forecasts.")

st.subheader("Editable expected-return estimates")
edited_sleeves = {asset: details.copy() for asset, details in loaded_sleeves.items()}
return_columns = st.columns(min(3, len(edited_sleeves)))
for index, asset in enumerate(edited_sleeves):
    with return_columns[index % len(return_columns)]:
        return_percent = st.number_input(
            f"{asset} return estimate (%)", min_value=-50.0, max_value=50.0,
            value=loaded_sleeves[asset]["expected_return"] * 100, step=0.5,
            format="%.1f", key=f"return_{asset}",
        )
        edited_sleeves[asset]["expected_return"] = return_percent / 100

st.subheader("Reserve-eligible assets")
eligible_columns = st.columns(min(3, len(edited_sleeves)))
reserve_eligible = set()
for index, asset in enumerate(edited_sleeves):
    default = asset in RESERVE_ELIGIBLE if uploaded_file is None else False
    with eligible_columns[index % len(eligible_columns)]:
        if st.checkbox(asset, value=default, key=f"eligible_{asset}"):
            reserve_eligible.add(asset)

# The baseline is always the original loaded case: Meridian, or all CSV months.
if uploaded_file is None:
    baseline_sleeves = {asset: details.copy() for asset, details in SLEEVES.items()}
    baseline_correlations = CORRELATIONS
    baseline_eligible = RESERVE_ELIGIBLE
else:
    baseline_sleeves = all_months["sleeves"]
    baseline_correlations = all_months["correlations"]
    baseline_eligible = reserve_eligible

baseline = search_long_only_mix(
    baseline_sleeves, baseline_correlations, OBJECTIVE_RETURN, 0.03, baseline_eligible
)
current = search_long_only_mix(
    edited_sleeves, loaded_correlations, objective_percent / 100,
    minimum_reserve_percent / 100, reserve_eligible
)

left, right = st.columns(2)
with left:
    st.subheader("Lowest-risk mix for current controls")
    format_result(current)
with right:
    st.subheader("Answer for inputs as loaded")
    format_result(baseline)

st.info(largest_weight_change(baseline, current))
st.caption("The search tests every long-only allocation in 5-percentage-point steps; it does not optimize between those grid points.")
