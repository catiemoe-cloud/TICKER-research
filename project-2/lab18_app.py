"""Lab 18 EDGAR Buffett review. Run: streamlit run lab18_app.py"""

import json
import re
import subprocess
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).parent
SCRIPT = ROOT / "edgar-buffett" / "scripts" / "edgar_financials.py"
REPORTS = ROOT / "reports"


def load_report(ticker):
    path = REPORTS / f"{ticker}_edgar_facts.json"
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), ticker, "--json-output", str(path)],
        text=True, capture_output=True, timeout=60, check=False,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    return json.loads(path.read_text(encoding="utf-8")), completed.stdout


def display_money(value):
    return "not found" if value is None else f"${value / 1_000_000:,.0f}"


def tagged_value(value, tag):
    return "not found" if tag == "not found" else f"{display_money(value)} [{tag}]"


def printed_numbers(report):
    values = set()
    for row in report["rows"]:
        fiscal_year_end = row["fiscal_year_end"]
        values.add(fiscal_year_end)
        values.add(fiscal_year_end[:4])  # Memo may refer to the printed date as FY2022.
        for key in ("revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "owner_earnings"):
            if row[key] is not None:
                values.add(f"{row[key] / 1_000_000:,.0f}".replace(",", ""))
        if row["roe"] is not None:
            values.add(f"{row['roe']:.2%}".replace("%", ""))
    values.add("15")
    return values


def audit_memo(memo, report):
    allowed = printed_numbers(report)
    found = re.findall(r"\$?\d[\d,]*(?:\.\d+)?%?", memo)
    unprinted = []
    for token in found:
        normalized = token.replace("$", "").replace(",", "").replace("%", "")
        if normalized not in allowed and normalized not in unprinted:
            unprinted.append(normalized)
    return unprinted


st.set_page_config(page_title="Lab 18 EDGAR Buffett Review", layout="wide")
st.title("Lab 18 — EDGAR Buffett Review")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
st.caption("To download or refresh facts, launch the app with `SEC_EDGAR_USER_AGENT='Your Name your.email@example.com'`; do not save personal contact details in this project.")

ticker = st.sidebar.text_input("Ticker", value="COST").strip().upper()
refresh = st.sidebar.button("Download 10-K facts")
report_path = REPORTS / f"{ticker}_edgar_facts.json"

if refresh or not report_path.exists():
    try:
        with st.spinner("Downloading keyless SEC EDGAR company facts..."):
            report, output = load_report(ticker)
        st.sidebar.success("EDGAR facts downloaded")
    except RuntimeError as error:
        st.error(str(error))
        st.stop()
else:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    output = "Loaded saved EDGAR report. Select Download 10-K facts to refresh."

st.subheader(f"{report['company']} ({report['ticker']})")
st.caption(f"CIK {report['cik']} · Latest-filing-wins 10-K facts")

chart_rows = [
    {
        "Fiscal year end": row["fiscal_year_end"],
        "Owner earnings (USD millions)": None if row["owner_earnings"] is None else row["owner_earnings"] / 1_000_000,
        "Net income (USD millions)": None if row["net_income"] is None else row["net_income"] / 1_000_000,
    }
    for row in report["rows"]
]
st.subheader("Owner earnings and net income")
st.line_chart(chart_rows, x="Fiscal year end", y=["Owner earnings (USD millions)", "Net income (USD millions)"])

table = []
for row in report["rows"]:
    table.append({
        "Fiscal year end": row["fiscal_year_end"],
        "Revenue": tagged_value(row["revenue"], row["revenue_tag"]),
        "Net income": tagged_value(row["net_income"], row["net_income_tag"]),
        "Operating cash flow": tagged_value(row["operating_cash_flow"], row["operating_cash_flow_tag"]),
        "Capital spending": tagged_value(row["capital_spending"], row["capital_spending_tag"]),
        "Equity": tagged_value(row["equity"], row["equity_tag"]),
        "ROE": (
            "not known" if row["roe"] is None
            else f"{row['roe']:.2%} [computed: NetIncomeLoss / StockholdersEquity]"
        ),
        "Owner earnings": (
            f"{display_money(row['owner_earnings'])} "
            "[computed: operating cash flow - capital spending]"
        ),
    })
st.subheader("Five fiscal years — USD millions")
st.dataframe(table, hide_index=True, use_container_width=True)

st.subheader("Buffett checks")
st.table([{"Check": label, "Result": result} for label, result in report["checks"].items()])

memo_path = REPORTS / f"{ticker}_buffett_memo.md"
st.subheader("Buffett memo")
if memo_path.exists():
    memo = memo_path.read_text(encoding="utf-8")
    st.markdown(memo)
    unexpected = audit_memo(memo, report)
    if unexpected:
        st.error("Memo numbers not printed by the script: " + ", ".join(unexpected))
    else:
        st.success("Memo-number audit passed: every numeric claim appears in the script output.")
else:
    st.warning(f"Memo not found: {memo_path.name}. Use the edgar-buffett skill after reviewing the script output.")

with st.expander("Exact script output"):
    st.code(output)
