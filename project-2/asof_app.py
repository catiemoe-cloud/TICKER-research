"""Lab 17: compare current FRED values with an ALFRED vintage."""

import csv
import io
import re
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import altair as alt
import pandas as pd
import streamlit as st


SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
ALFRED_URL = (
    "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}"
    "&vintage_date={vintage_date}"
)


def download_csv(url):
    """Download a public FRED-family CSV and return non-missing (date, value) pairs."""
    request = Request(url, headers={"User-Agent": "FIN43900-Lab17/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            text = response.read().decode("utf-8-sig")
    except HTTPError as error:
        raise ValueError(f"download failed (HTTP {error.code})") from error
    except URLError as error:
        raise ValueError(f"download failed ({error.reason})") from error

    rows = list(csv.reader(io.StringIO(text)))
    if len(rows) < 2 or len(rows[0]) < 2:
        raise ValueError("download did not contain a date and value column")
    observations = []
    for row in rows[1:]:
        if len(row) < 2 or row[1] == "." or not row[1]:
            continue
        try:
            observations.append((date.fromisoformat(row[0]), float(row[1])))
        except ValueError:
            continue
    if not observations:
        raise ValueError("download contained no numeric observations")
    return observations


@st.cache_data(ttl=3600, show_spinner=False)
def download_today(series_id):
    """Return the series as currently published by FRED."""
    return download_csv(FRED_URL.format(series_id=series_id))


@st.cache_data(ttl=3600, show_spinner=False)
def download_vintage(series_id, vintage_date):
    """Return the series as published in the requested ALFRED vintage."""
    return download_csv(
        ALFRED_URL.format(series_id=series_id, vintage_date=vintage_date.isoformat())
    )


def as_date_value_map(observations, end_date=None):
    """Map dates to values, optionally excluding observations after an as-of date."""
    return {
        observation_date: value
        for observation_date, value in observations
        if end_date is None or observation_date <= end_date
    }


def format_observation(observations):
    if not observations:
        return "No observation"
    observation_date = max(observations)
    return f"{observation_date.isoformat()}: {observations[observation_date]:.2f}"


def table_html(rows):
    header = (
        "<tr><th>Series</th><th>Last known then</th><th>Last value today</th>"
        "<th>Today's values after then</th><th>Revised values on shared dates</th></tr>"
    )
    body = "".join(
        "<tr>"
        f"<td><a href='https://fred.stlouisfed.org/series/{row['series']}' target='_blank'>{row['series']}</a></td>"
        f"<td>{row['known_then']}</td><td>{row['today']}</td>"
        f"<td>{row['after_count']}</td><td>{row['revision_count']}</td>"
        "</tr>"
        for row in rows
    )
    return (
        "<table><thead>" + header + "</thead><tbody>" + body + "</tbody></table>"
    )


def render_rate_chart(frame, chart_style, key):
    """Render one rate series as a line, bar, or transparent change-candle chart."""
    if chart_style == "Line":
        st.line_chart(frame, x="Date", y="Value", y_label="Value")
    elif chart_style == "Bar":
        st.bar_chart(frame, x="Date", y="Value", y_label="Value")
    else:
        candles = frame.copy()
        candles["Open"] = candles["Value"].shift(1).fillna(candles["Value"])
        candles["Close"] = candles["Value"]
        candles["High"] = candles[["Open", "Close"]].max(axis=1)
        candles["Low"] = candles[["Open", "Close"]].min(axis=1)
        candles["Direction"] = candles["Close"] >= candles["Open"]
        st.vega_lite_chart(
            candles,
            {
                "layer": [
                    {
                        "mark": {"type": "rule", "color": "#666"},
                        "encoding": {
                            "x": {"field": "Date", "type": "temporal"},
                            "y": {"field": "Low", "type": "quantitative"},
                            "y2": {"field": "High"},
                        },
                    },
                    {
                        "mark": {"type": "bar", "size": 5},
                        "encoding": {
                            "x": {"field": "Date", "type": "temporal"},
                            "y": {"field": "Open", "type": "quantitative"},
                            "y2": {"field": "Close"},
                            "color": {
                                "condition": {"test": "datum.Direction", "value": "#2ca02c"},
                                "value": "#d62728",
                            },
                        },
                    },
                ]
            },
            key=key,
            use_container_width=True,
        )
        st.caption(
            "Rate-change candles: open is the prior observation and close is the current observation. "
            "This is not a true market OHLC candlestick chart."
        )


def render_combined_chart(rows):
    """Show every selected rate with visible, distinct line styles and tooltips."""
    frame = pd.DataFrame(rows)
    colors = ["#0057b8", "#e45756", "#2ca02c", "#9467bd", "#ff7f0e"]
    order = list(dict.fromkeys(frame["Series"]))
    chart = (
        alt.Chart(frame)
        .mark_line(strokeWidth=2.5)
        .encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("Value:Q", title="Rate value", scale=alt.Scale(zero=False)),
            color=alt.Color(
                "Series:N", title="Series",
                scale=alt.Scale(domain=order, range=colors[:len(order)]),
            ),
            strokeDash=alt.StrokeDash("Series:N", title="Series"),
            tooltip=[
                alt.Tooltip("Date:T", title="Date"),
                alt.Tooltip("Series:N", title="Series"),
                alt.Tooltip("Value:Q", title="Value", format=".2f"),
            ],
        )
        .properties(height=430)
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True)

    indexed = frame.copy()
    first_values = indexed.groupby("Series")["Value"].transform("first")
    indexed["Index"] = indexed["Value"] / first_values * 100
    indexed_chart = (
        alt.Chart(indexed)
        .mark_line(strokeWidth=2.5)
        .encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("Index:Q", title="Index (first displayed value = 100)"),
            color=alt.Color(
                "Series:N", title="Series",
                scale=alt.Scale(domain=order, range=colors[:len(order)]),
            ),
            strokeDash=alt.StrokeDash("Series:N", title="Series"),
            tooltip=[
                alt.Tooltip("Date:T", title="Date"),
                alt.Tooltip("Series:N", title="Series"),
                alt.Tooltip("Index:Q", title="Indexed value", format=".1f"),
            ],
        )
        .properties(height=300)
        .interactive()
    )
    st.caption("Normalized comparison: each series begins at 100, making relative moves easy to compare.")
    st.altair_chart(indexed_chart, use_container_width=True)


st.set_page_config(page_title="Lab 17 — FRED Vintage Gate", layout="wide")
st.title("Lab 17 — FRED Vintage Gate")
st.caption(
    "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today; "
    "built with AI help, a learning demonstration, not investment advice."
)

with st.sidebar:
    selected = st.multiselect(
        "Series",
        options=list(SERIES),
        default=list(SERIES),
        format_func=lambda series_id: f"{series_id} — {SERIES[series_id]}",
    )
    extra_series = st.text_input("Add another FRED series ID").strip().upper()
    start_date = st.date_input("Start date", value=date(2020, 1, 1))
    as_known_on = st.date_input("As known on", value=date.today())
    chart_style = st.selectbox("Individual chart style", ("Line", "Bar", "Candlestick"))

series_ids = selected.copy()
if extra_series:
    if re.fullmatch(r"[A-Z0-9_]+", extra_series):
        if extra_series not in series_ids:
            series_ids.append(extra_series)
    else:
        st.sidebar.error("A series ID may contain only letters, numbers, and underscores.")

if not series_ids:
    st.info("Select at least one series to begin.")
    st.stop()

table_rows = []
loaded_series = []
for series_id in series_ids:
    try:
        today_observations = download_today(series_id)
        vintage_observations = download_vintage(series_id, as_known_on)
        today_values = as_date_value_map(today_observations)
        vintage_values = as_date_value_map(vintage_observations, end_date=as_known_on)
        chart_values = {
            observation_date: value
            for observation_date, value in today_values.items()
            if observation_date >= start_date
        }
        last_known_date = max(vintage_values) if vintage_values else None
        after_count = sum(
            observation_date > last_known_date for observation_date in today_values
        ) if last_known_date else len(today_values)
        shared_dates = set(today_values) & set(vintage_values)
        revision_count = sum(
            abs(today_values[observation_date] - vintage_values[observation_date]) > 1e-12
            for observation_date in shared_dates
        )
        table_rows.append(
            {
                "series": series_id,
                "known_then": format_observation(vintage_values),
                "today": format_observation(today_values),
                "after_count": after_count,
                "revision_count": revision_count,
            }
        )
        loaded_series.append(
            {
                "series_id": series_id,
                "chart_values": chart_values,
                "last_known_date": last_known_date,
            }
        )
    except ValueError as error:
        st.error(f"{series_id}: {error}. The other selected series can still load.")

if loaded_series:
    combined_rows = [
        {"Date": observation_date, "Series": item["series_id"], "Value": value}
        for item in loaded_series
        for observation_date, value in item["chart_values"].items()
    ]
    if combined_rows:
        st.subheader("All selected series — current values compared over time")
        render_combined_chart(combined_rows)
        if chart_style != "Line":
            st.caption("The combined comparison remains a line chart so all series stay readable together.")

    for item in loaded_series:
        series_id = item["series_id"]
        if not item["chart_values"]:
            st.warning(f"{series_id}: no current observations on or after {start_date.isoformat()}.")
            continue
        st.subheader(f"{series_id} — {SERIES.get(series_id, 'Custom FRED series')}")
        chart_frame = pd.DataFrame(
            sorted(item["chart_values"].items()), columns=["Date", "Value"]
        )
        render_rate_chart(chart_frame, chart_style, f"chart_{series_id}")
        st.caption(
            f"Last date known on {as_known_on.isoformat()}: "
            f"{item['last_known_date'].isoformat() if item['last_known_date'] else 'no numeric observation'}"
        )

st.subheader("Vintage comparison")
if table_rows:
    st.markdown(table_html(table_rows), unsafe_allow_html=True)
else:
    st.info("No selected series returned usable data.")
