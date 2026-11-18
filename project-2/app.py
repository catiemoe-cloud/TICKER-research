"""Project 2 investment-committee app. Run: streamlit run app.py"""

import csv
import io
import statistics
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import streamlit as st

from portfolio import (
    equal_weight_portfolio,
    estimate_from_monthly_prices,
    evaluate_mandate,
    search_project2_mix,
)


ROOT = Path(__file__).parent
PRICE_FILE = ROOT / "prices.csv"
TICKERS = ("BIL", "IEF", "LQD", "ACWI")
OBJECTIVE = 0.065
MINIMUM_BIL = 0.10
MAXIMUM_ETF = 0.70
GRID_STEP = 0.05
DRIFT_BAND = 0.05
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
ALFRED_URL = (
    "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}"
    "&vintage_date={vintage_date}"
)


def percent(value):
    """Format a decimal as a percent."""
    return "not known" if value is None else f"{value:.2%}"


def points(value):
    """Format a decimal as percentage points."""
    return f"{value * 100:+.1f} points"


def portfolio_rows(result, label):
    return {
        "Portfolio": label,
        "Gross return estimate": percent(result["gross_return"]),
        "Annual cost": percent(result["annual_cost"]),
        "Net return estimate": percent(result["net_return"]),
        "Annualized volatility": percent(result["volatility"]),
        "BIL": percent(result["bil_weight"]),
        "Largest ETF": f"{result['largest_asset']} ({percent(result['largest_weight'])})",
        "Mandate verdict": result["verdict"],
    }


def weights_rows(results):
    return [
        {
            "ETF": ticker,
            **{label: percent(result["weights"].get(ticker, 0.0)) for label, result in results.items()},
        }
        for ticker in TICKERS
    ]


def checks_rows(results):
    labels = list(next(iter(results.values()))["checks"])
    return [
        {
            "Mandate rule": label,
            **{
                portfolio: "PASS" if result["checks"][label] else "FAIL"
                for portfolio, result in results.items()
            },
        }
        for label in labels
    ]


def run_case(
    csv_source,
    last_36_months=False,
    annual_cost=0.0,
    objective=OBJECTIVE,
    minimum_bil=MINIMUM_BIL,
    maximum_etf=MAXIMUM_ETF,
    return_adjustments=None,
):
    """Calculate both baselines and the constrained portfolio from one data source."""
    estimates = estimate_from_monthly_prices(csv_source, last_36_months=last_36_months)
    sleeves = {ticker: details.copy() for ticker, details in estimates["sleeves"].items()}
    correlations = estimates["correlations"]
    if set(sleeves) != set(TICKERS):
        raise ValueError("The Project 2 price CSV must contain exactly BIL, IEF, LQD, and ACWI.")
    for ticker, adjustment in (return_adjustments or {}).items():
        sleeves[ticker]["expected_return"] += adjustment

    equal = evaluate_mandate(
        equal_weight_portfolio(sleeves),
        sleeves,
        correlations,
        objective,
        minimum_bil,
        maximum_etf,
        annual_cost,
    )
    benchmark = evaluate_mandate(
        {"BIL": 0.0, "IEF": 0.0, "LQD": 0.40, "ACWI": 0.60},
        sleeves,
        correlations,
        objective,
        minimum_bil,
        maximum_etf,
        annual_cost,
    )
    recommended = search_project2_mix(
        sleeves,
        correlations,
        objective,
        minimum_bil,
        maximum_etf,
        annual_cost,
        GRID_STEP,
    )
    return estimates, {
        "Equal weight": equal,
        "60/40 benchmark": benchmark,
        "Constrained portfolio": recommended,
    }


def download_csv(url):
    """Download a FRED-family CSV and return numeric date/value pairs."""
    request = Request(url, headers={"User-Agent": "FIN43900-Project2/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            contents = response.read().decode("utf-8-sig")
    except HTTPError as error:
        raise ValueError(f"FRED/ALFRED download failed (HTTP {error.code}).") from error
    except URLError as error:
        raise ValueError(f"FRED/ALFRED download failed ({error.reason}).") from error

    values = []
    for row in list(csv.reader(io.StringIO(contents)))[1:]:
        if len(row) < 2 or row[1] in ("", "."):
            continue
        try:
            values.append((date.fromisoformat(row[0]), float(row[1])))
        except ValueError:
            continue
    if not values:
        raise ValueError("FRED/ALFRED returned no numeric observations.")
    return values


@st.cache_data(ttl=3600, show_spinner=False)
def download_fred_pair(series_id, vintage_date):
    """Get the current series and the requested ALFRED vintage."""
    current = download_csv(FRED_URL.format(series_id=series_id))
    vintage = download_csv(
        ALFRED_URL.format(series_id=series_id, vintage_date=vintage_date.isoformat())
    )
    return current, vintage


def summarize_signal(as_of_date):
    """Calculate the point-in-time credit-monitor fields from FRED and ALFRED."""
    current, vintage = download_fred_pair("BAMLC0A0CM", as_of_date)
    vintage_values = {observation_date: value for observation_date, value in vintage if observation_date <= as_of_date}
    current_values = dict(current)
    if not vintage_values:
        raise ValueError("No BAMLC0A0CM value was available on the selected as-of date.")
    available_dates = sorted(vintage_values)
    last_date = available_dates[-1]
    trailing_values = [vintage_values[value_date] for value_date in available_dates[-252:]]
    shared_dates = set(vintage_values) & set(current_values)
    revisions = sum(
        abs(vintage_values[value_date] - current_values[value_date]) > 1e-12
        for value_date in shared_dates
    )
    return {
        "as_of_date": as_of_date,
        "last_available_date": last_date,
        "latest_spread": vintage_values[last_date],
        "trailing_median": statistics.median(trailing_values),
        "trailing_observations": len(trailing_values),
        "revision_count": revisions,
        "future_observations": sum(value_date > last_date for value_date in current_values),
    }


def largest_allocation_move(base, stressed):
    """Return the asset and absolute move between two constrained portfolios."""
    asset = max(
        TICKERS,
        key=lambda ticker: abs(
            stressed["weights"][ticker] - base["weights"][ticker]
        ),
    )
    return asset, stressed["weights"][asset] - base["weights"][asset]


def baseline_gap_rows(results):
    """Explain why the constrained portfolio differs from each baseline."""
    recommended = results["Constrained portfolio"]
    rows = []
    for name in ("Equal weight", "60/40 benchmark"):
        baseline = results[name]
        failures = [label for label, passed in baseline["checks"].items() if not passed]
        rows.append(
            {
                "Baseline": name,
                "Net-return gap vs. constrained": points(recommended["net_return"] - baseline["net_return"]),
                "Volatility gap vs. constrained": points(recommended["volatility"] - baseline["volatility"]),
                "BIL gap vs. constrained": points(recommended["bil_weight"] - baseline["bil_weight"]),
                "Baseline failed rule(s)": "; ".join(failures) if failures else "None",
            }
        )
    return rows


def action_card(current_weights, target, signal_review, stress_review):
    """Turn target/current weights and governance flags into an operational action."""
    if abs(sum(current_weights.values()) - 1.0) > 0.0001:
        return "CHECK INPUT", "Current weights must add to 100% before the committee can act.", None
    differences = {
        ticker: current_weights[ticker] - target["weights"][ticker] for ticker in TICKERS
    }
    turnover = sum(abs(value) for value in differences.values()) / 2.0
    largest_ticker = max(TICKERS, key=lambda ticker: abs(differences[ticker]))
    if signal_review or stress_review:
        reasons = []
        if signal_review:
            reasons.append("the credit-spread monitor is above its trailing median")
        if stress_review:
            reasons.append("the window stress moves an allocation by 25 points or more")
        return "COMMITTEE REVIEW", " and ".join(reasons).capitalize() + ".", {
            "turnover": turnover,
            "largest_ticker": largest_ticker,
            "largest_difference": differences[largest_ticker],
        }
    if abs(differences[largest_ticker]) > DRIFT_BAND + 1e-9:
        return "REBALANCE", f"{largest_ticker} is outside the {DRIFT_BAND:.0%} target band.", {
            "turnover": turnover,
            "largest_ticker": largest_ticker,
            "largest_difference": differences[largest_ticker],
        }
    return "HOLD", "Every current allocation is inside the 5% target band.", {
        "turnover": turnover,
        "largest_ticker": largest_ticker,
        "largest_difference": differences[largest_ticker],
    }


def visible_output_markdown(base_estimates, base_results, stress_rows, signal, action, action_reason):
    """Create a portable summary a user can save as visible executed output."""
    target = base_results["Constrained portfolio"]
    signal_text = "not available"
    if signal:
        signal_text = (
            f"BAMLC0A0CM as of {signal['as_of_date']}: {signal['latest_spread']:.2f}% "
            f"versus {signal['trailing_median']:.2f}% trailing median."
        )
    lines = [
        "# Project 2 — Visible Executed Output",
        "",
        "Built with AI help for coding, research organization, and debugging; the analysis and decision are mine.",
        "Education, not investment advice.",
        "",
        "## Committee decision",
        "",
        "Tentative action: **Pilot**, subject to the monitoring and reversal conditions below.",
        f"Operational action today: **{action}** — {action_reason}",
        f"Price window: {base_estimates['first_date']} through {base_estimates['last_date']}.",
        signal_text,
        "",
        "## Constrained portfolio",
        "",
        "| ETF | Weight |",
        "|---|---:|",
        *[f"| {ticker} | {percent(target['weights'][ticker])} |" for ticker in TICKERS],
        "",
        f"Net return estimate: {percent(target['net_return'])}; annualized volatility: {percent(target['volatility'])}.",
        "",
        "## Stress scenarios",
        "",
        "| Scenario | BIL | ACWI | Net return estimate | Volatility | Verdict |",
        "|---|---:|---:|---:|---:|---|",
        *[
            f"| {row['Scenario']} | {row['BIL']} | {row['ACWI']} | {row['Net return estimate']} | {row['Volatility']} | {row['Verdict']} |"
            for row in stress_rows
        ],
        "",
        "Stop or pause the pilot if the window stress moves any recommended allocation by 25 points or more, the portfolio misses the target, or the credit monitor requires committee review.",
    ]
    return "\n".join(lines) + "\n"


st.set_page_config(page_title="Project 2 — Cautious Growth Portfolio", layout="wide")
st.markdown(
    """
    <style>
      :root {
        --navy: #102a43;
        --blue: #247ba0;
        --teal: #2a9d8f;
        --gold: #f4a261;
        --mist: #f5f8fb;
      }
      .stApp { background: linear-gradient(180deg, #f7fafc 0%, #ffffff 32%); }
      [data-testid="stSidebar"] { background: #102a43; }
      [data-testid="stSidebar"] * { color: #f7fafc; }
      [data-testid="stSidebar"] [data-baseweb="select"] * { color: #102a43; }
      [data-testid="stSidebar"] input { color: #102a43 !important; }
      .hero {
        background: linear-gradient(120deg, #102a43, #247ba0);
        border-radius: 18px;
        color: white;
        margin: 0.35rem 0 1.5rem;
        padding: 1.8rem 2rem;
        box-shadow: 0 10px 26px rgba(16, 42, 67, .16);
      }
      .hero h1 { color: white; font-size: 2.45rem; margin: 0; }
      .hero p { color: #dbeafe; font-size: 1.06rem; margin: .55rem 0 0; }
      .eyebrow { color: #7dd3fc; font-weight: 700; letter-spacing: .11em; text-transform: uppercase; font-size: .75rem; }
      .section-label { color: #247ba0; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: .76rem; margin-bottom: -.55rem; }
      [data-testid="stMetric"] {
        background: white;
        border: 1px solid #dbe7f0;
        border-radius: 12px;
        padding: .9rem;
        box-shadow: 0 3px 10px rgba(16, 42, 67, .05);
      }
      h2, h3 { color: #102a43; }
      [data-testid="stDataFrame"] { border: 1px solid #dbe7f0; border-radius: 10px; overflow: hidden; }
      .small-note { color: #52606d; font-size: .9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Investment committee dashboard</div>
      <h1>Project 2 — Cautious Growth Portfolio</h1>
      <p>A transparent, monitored portfolio recommendation built from the same historical inputs and mandate rules.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption(
    "Built with AI help for coding, research organization, and debugging; the analysis and decision are mine. "
    "Education, not investment advice."
)

with st.sidebar:
    st.header("Portfolio data")
    uploaded_file = st.file_uploader("Optional replacement price CSV", type="csv")
    st.caption("Default data: BIL, IEF, LQD, and ACWI monthly adjusted-close prices in `prices.csv`.")
    st.header("Selected stress view")
    selected_window = st.selectbox("Estimation window", ("All available monthly returns", "Last 36 monthly returns"))
    selected_cost_bps = st.number_input(
        "Annual portfolio cost (basis points)", min_value=0, max_value=500, value=0, step=5
    )
    st.caption("Base mandate: 6.5% net return target, at least 10% BIL, no ETF above 70%, and five-point allocation steps.")
    st.header("Point-in-time credit monitor")
    as_of_date = st.date_input("Signal as-of date", value=date(2026, 9, 30))
    use_downloaded_signal = st.checkbox("Download FRED/ALFRED vintage", value=False)
    manual_latest = st.number_input("Fallback latest spread (%)", min_value=0.0, max_value=20.0, value=0.84, step=0.01)
    manual_median = st.number_input("Fallback trailing median (%)", min_value=0.0, max_value=20.0, value=0.84, step=0.01)


def source_for_run():
    if uploaded_file is not None:
        uploaded_file.seek(0)
        return uploaded_file
    return PRICE_FILE


try:
    base_estimates, base_results = run_case(source_for_run())
    window_estimates, window_results = run_case(source_for_run(), last_36_months=True)
    cost_estimates, cost_results = run_case(source_for_run(), annual_cost=0.005)
    estimate_estimates, estimate_results = run_case(
        source_for_run(), return_adjustments={"ACWI": -0.01}
    )
    constraint_estimates, constraint_results = run_case(source_for_run(), minimum_bil=0.20)
    selected_estimates, selected_results = run_case(
        source_for_run(),
        last_36_months=selected_window == "Last 36 monthly returns",
        annual_cost=selected_cost_bps / 10_000,
    )
except ValueError as error:
    st.error(str(error))
    st.stop()

signal = None
signal_error = None
if use_downloaded_signal:
    try:
        signal = summarize_signal(as_of_date)
    except ValueError as error:
        signal_error = str(error)
if signal is None:
    signal = {
        "as_of_date": as_of_date,
        "last_available_date": as_of_date,
        "latest_spread": manual_latest,
        "trailing_median": manual_median,
        "trailing_observations": None,
        "revision_count": None,
        "future_observations": None,
    }
signal_review = signal["latest_spread"] > signal["trailing_median"]

base_target = base_results["Constrained portfolio"]
window_target = window_results["Constrained portfolio"]
window_asset, window_move = largest_allocation_move(base_target, window_target)
stress_review = abs(window_move) >= 0.25 - 1e-9

st.markdown('<div class="section-label">01 · Committee recommendation</div>', unsafe_allow_html=True)
st.subheader("Committee decision")
decision, allocation, reversal = st.columns(3)
decision.metric("Tentative committee recommendation", "PILOT")
allocation.metric("Pilot allocation range", "BIL 55–65% · ACWI 35–45%")
reversal.metric("Pause/reversal trigger", "25+ point 36-month stress move")
st.info(
    "This is a monitored pilot, not a claim that the portfolio is permanently optimal. "
    "The committee should approve implementation only after reviewing the stress results, current drift, and credit monitor."
)

st.markdown('<div class="section-label">02 · Data boundary and credit signal</div>', unsafe_allow_html=True)
st.subheader("Data boundary and signal governance")
st.write(
    f"Price estimates use {base_estimates['months_used']} monthly returns from "
    f"{base_estimates['first_date']} through {base_estimates['last_date']}. "
    "Historical returns are estimates, not forecasts."
)
if signal_error:
    st.warning(f"Automatic vintage download was unavailable: {signal_error} Using the clearly labeled fallback values instead.")
signal_columns = st.columns(4)
signal_columns[0].metric("Signal as-of date", signal["as_of_date"].isoformat())
signal_columns[1].metric("Last available observation", signal["last_available_date"].isoformat())
signal_columns[2].metric("Latest OAS", f"{signal['latest_spread']:.2f}%")
signal_columns[3].metric("Trailing median", f"{signal['trailing_median']:.2f}%")
if signal_review:
    st.warning("REVIEW LQD: the point-in-time corporate spread is above its trailing median. This flag triggers a committee review, not an automatic trade.")
else:
    st.success("No LQD review flag: the point-in-time corporate spread is at or below its trailing median.")
with st.expander("Signal data card and audit trail"):
    st.markdown(
        "**Series:** `BAMLC0A0CM` — ICE BofA U.S. Corporate Index Option-Adjusted Spread.  \n"
        "**Source:** [FRED](https://fred.stlouisfed.org/series/BAMLC0A0CM) and ALFRED vintage CSV.  \n"
        "**Units/frequency:** percent; daily close.  \n"
        "**Purpose:** monitor credit risk relevant to the LQD sleeve.  \n"
        "**Rule:** flag LQD for committee review when the point-in-time spread is above its trailing 12-month median.  \n"
        "**As-of rule:** only values in the ALFRED vintage available on the selected decision date are used."
    )
    if signal["trailing_observations"] is not None:
        st.write(
            f"Trailing observations used: {signal['trailing_observations']}; revisions on shared dates: "
            f"{signal['revision_count']}; current observations after the vintage's last observation: "
            f"{signal['future_observations']}."
        )

st.divider()
st.markdown('<div class="section-label">03 · Baselines vs. recommendation</div>', unsafe_allow_html=True)
st.subheader("Base-case portfolio comparison")
st.dataframe(
    [portfolio_rows(result, label) for label, result in base_results.items()],
    hide_index=True,
    width="stretch",
)
left, right = st.columns(2)
with left:
    st.markdown("#### Allocation weights")
    st.dataframe(weights_rows(base_results), hide_index=True, width="stretch")
with right:
    st.markdown("#### Mandate verdicts")
    st.dataframe(checks_rows(base_results), hide_index=True, width="stretch")

chart_left, chart_right = st.columns(2)
with chart_left:
    st.markdown("#### Net return estimates")
    return_chart = [
        {"Portfolio": label, "Net return (%)": round(result["net_return"] * 100, 2)}
        for label, result in base_results.items()
    ]
    st.vega_lite_chart(
        return_chart,
        {
            "mark": {"type": "bar", "cornerRadiusTopLeft": 6, "cornerRadiusTopRight": 6},
            "encoding": {
                "x": {"field": "Portfolio", "type": "nominal", "sort": None, "axis": {"labelAngle": 0}},
                "y": {"field": "Net return (%)", "type": "quantitative", "title": "Annual net return (%)"},
                "color": {
                    "field": "Portfolio",
                    "type": "nominal",
                    "legend": None,
                    "scale": {"range": ["#9ecae1", "#f4a261", "#2a9d8f"]},
                },
                "tooltip": [
                    {"field": "Portfolio", "type": "nominal"},
                    {"field": "Net return (%)", "type": "quantitative", "format": ".2f"},
                ],
            },
            "height": 260,
        },
        width="stretch",
    )
with chart_right:
    st.markdown("#### Constrained portfolio allocation")
    allocation_chart = [
        {"ETF": ticker, "Weight (%)": round(base_target["weights"][ticker] * 100, 1)}
        for ticker in TICKERS
    ]
    st.vega_lite_chart(
        allocation_chart,
        {
            "mark": {"type": "bar", "cornerRadiusEnd": 6},
            "encoding": {
                "y": {"field": "ETF", "type": "nominal", "sort": "-x", "title": None},
                "x": {"field": "Weight (%)", "type": "quantitative", "title": "Portfolio weight (%)"},
                "color": {
                    "field": "ETF",
                    "type": "nominal",
                    "legend": None,
                    "scale": {"range": ["#247ba0", "#70c1b3", "#f4a261", "#102a43"]},
                },
                "tooltip": [
                    {"field": "ETF", "type": "nominal"},
                    {"field": "Weight (%)", "type": "quantitative", "format": ".1f"},
                ],
            },
            "height": 260,
        },
        width="stretch",
    )

st.markdown("#### Why the constrained portfolio differs from the baselines")
st.dataframe(baseline_gap_rows(base_results), hide_index=True, width="stretch")

st.divider()
st.markdown('<div class="section-label">04 · Decision durability</div>', unsafe_allow_html=True)
st.subheader("Required stress scenarios")
stress_cases = {
    "Base case": (base_estimates, base_results, "All monthly returns; no cost drag"),
    "Estimate stress": (estimate_estimates, estimate_results, "ACWI return estimate reduced by 1.00 percentage point"),
    "Window stress": (window_estimates, window_results, "Latest 36 monthly returns"),
    "Cost stress": (cost_estimates, cost_results, "50 basis-point annual portfolio cost drag"),
    "Constraint stress": (constraint_estimates, constraint_results, "Minimum BIL increased from 10% to 20%"),
}
stress_rows = []
for name, (estimates, results, change) in stress_cases.items():
    result = results["Constrained portfolio"]
    if result is None:
        stress_rows.append({"Scenario": name, "Change": change, "Result": "No feasible portfolio"})
        continue
    stress_rows.append(
        {
            "Scenario": name,
            "Change": change,
            "Window": f"{estimates['first_date']} to {estimates['last_date']}",
            "BIL": percent(result["bil_weight"]),
            "IEF": percent(result["weights"]["IEF"]),
            "LQD": percent(result["weights"]["LQD"]),
            "ACWI": percent(result["weights"]["ACWI"]),
            "Net return estimate": percent(result["net_return"]),
            "Volatility": percent(result["volatility"]),
            "Verdict": result["verdict"],
        }
    )
st.dataframe(stress_rows, hide_index=True, width="stretch")
stress_chart = [
    {
        "Scenario": row["Scenario"],
        "Net return (%)": float(row["Net return estimate"].rstrip("%")),
        "Volatility (%)": float(row["Volatility"].rstrip("%")),
    }
    for row in stress_rows
    if "Net return estimate" in row
]
st.markdown("#### Stress comparison")
st.vega_lite_chart(
    stress_chart,
    {
        "mark": {"type": "bar", "cornerRadiusTopLeft": 5, "cornerRadiusTopRight": 5},
        "encoding": {
            "x": {"field": "Scenario", "type": "nominal", "sort": None, "axis": {"labelAngle": -20}},
            "y": {"field": "Net return (%)", "type": "quantitative", "title": "Net return estimate (%)"},
            "color": {
                "field": "Scenario",
                "type": "nominal",
                "legend": None,
                "scale": {"range": ["#247ba0", "#e76f51", "#f4a261", "#70c1b3", "#2a9d8f"]},
            },
            "tooltip": [
                {"field": "Scenario", "type": "nominal"},
                {"field": "Net return (%)", "type": "quantitative", "format": ".2f"},
                {"field": "Volatility (%)", "type": "quantitative", "format": ".2f"},
            ],
        },
        "height": 300,
    },
    width="stretch",
)
st.info(
    f"The window stress moves {window_asset} by {points(window_move)}. "
    + ("This reaches the 25-point committee-review trigger." if stress_review else "This stays below the 25-point committee-review trigger.")
)

st.markdown('<div class="section-label">05 · Original extension</div>', unsafe_allow_html=True)
st.subheader("Allocation robustness map")
robustness_rows = []
for target in (0.055, 0.060, 0.065, 0.070):
    for window_label, last_36 in (("All monthly returns", False), ("Last 36 monthly returns", True)):
        estimates, results = run_case(source_for_run(), last_36_months=last_36, objective=target)
        result = results["Constrained portfolio"]
        row = {"Target": percent(target), "Window": window_label}
        if result is None:
            row.update({"Feasible?": "No", "BIL": "—", "ACWI": "—", "Volatility": "—"})
        else:
            row.update(
                {
                    "Feasible?": "Yes",
                    "BIL": percent(result["weights"]["BIL"]),
                    "ACWI": percent(result["weights"]["ACWI"]),
                    "Volatility": percent(result["volatility"]),
                }
            )
        robustness_rows.append(row)
st.dataframe(robustness_rows, hide_index=True, width="stretch")
st.caption("This map is an original extension: it shows whether the recommendation is stable across plausible return targets and data windows.")

st.divider()
st.markdown('<div class="section-label">06 · Operational next step</div>', unsafe_allow_html=True)
st.subheader("Rebalancing action card")
st.write("Enter the investor's current weights. The app compares them with the constrained target and gives a transparent operational recommendation.")
current_columns = st.columns(4)
current_weights = {}
for column, ticker in zip(current_columns, TICKERS):
    with column:
        current_weights[ticker] = st.number_input(
            f"Current {ticker} weight (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(base_target["weights"][ticker] * 100),
            step=1.0,
            key=f"current_{ticker}",
        ) / 100
action, action_reason, rebalance = action_card(
    current_weights, base_target, signal_review, stress_review
)
action_column, reason_column, turnover_column = st.columns(3)
action_column.metric("Action today", action)
reason_column.metric("Largest current-vs-target drift", "not known" if rebalance is None else f"{rebalance['largest_ticker']} {points(rebalance['largest_difference'])}")
turnover_column.metric("Estimated one-way turnover", "not known" if rebalance is None else percent(rebalance["turnover"]))
st.write(action_reason)

st.divider()
st.markdown('<div class="section-label">07 · Explore the mandate</div>', unsafe_allow_html=True)
st.subheader("Selected interactive view")
st.write(
    f"Window: {selected_estimates['first_date']} to {selected_estimates['last_date']}; "
    f"annual cost input: {selected_cost_bps} basis points."
)
st.dataframe(
    [portfolio_rows(result, label) for label, result in selected_results.items()],
    hide_index=True,
    width="stretch",
)

visible_output = visible_output_markdown(
    base_estimates, base_results, stress_rows, signal, action, action_reason
)
st.download_button(
    "Download visible executed output (.md)",
    visible_output,
    file_name="visible_output.md",
    mime="text/markdown",
)

with st.expander("Method and limitations"):
    st.markdown(
        "- The search tests long-only allocations in five-percentage-point steps, so it does not optimize between grid points.\n"
        "- Historical arithmetic-mean returns and historical volatility are estimates, not forecasts.\n"
        "- The cost input is a simplified portfolio-level annual return drag.\n"
        "- The credit signal is a monitoring input, not proof of future returns and not an automatic trading rule.\n"
        "- A committee decision still requires human judgment about suitability, taxes, trading, and changing market conditions."
    )
