"""Lab 19 investor panel. Run: streamlit run lab19_app.py"""

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
    path = REPORTS / f"{ticker}_panel_facts.json"
    completed = subprocess.run([sys.executable, str(SCRIPT), ticker, "--json-output", str(path)], text=True, capture_output=True, timeout=60)
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    return json.loads(path.read_text(encoding="utf-8")), completed.stdout


def money(value):
    return "not found" if value is None else f"${value / 1_000_000:,.0f}"


def allowed_numbers(report):
    values = {"15", "1.0"}
    for row in report["rows"]:
        values.update({row["fiscal_year_end"], row["fiscal_year_end"][:4]})
        for key in ("revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "liabilities", "assets_current", "liabilities_current", "owner_earnings"):
            if row.get(key) is not None:
                values.add(f"{row[key] / 1_000_000:,.0f}".replace(",", ""))
        if row.get("current_ratio") is not None:
            values.add(f"{row['current_ratio']:.2f}")
        if row.get("roe") is not None:
            values.add(f"{row['roe']:.2%}".replace("%", ""))
        if row.get("liabilities_to_equity") is not None:
            values.add(f"{row['liabilities_to_equity']:.2f}")
    return values


def audit(memo, report):
    allowed = allowed_numbers(report)
    unprinted = []
    # A fiscal date is printed as one SEC fact (for example, 2022-01-30).
    # Remove those exact printed dates before checking individual numeric tokens.
    memo_without_dates = memo
    for row in report["rows"]:
        memo_without_dates = memo_without_dates.replace(row["fiscal_year_end"], "")
    for token in re.findall(r"\$?\d[\d,]*(?:\.\d+)?%?", memo_without_dates):
        number = token.replace("$", "").replace(",", "").replace("%", "")
        if number not in allowed and number not in unprinted:
            unprinted.append(number)
    return unprinted


st.set_page_config(page_title="Lab 19 Investor Panel", layout="wide")
st.title("Lab 19 — Investor Skills Panel")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
ticker = st.sidebar.text_input("Ticker", "COST").strip().upper()
refresh = st.sidebar.button("Download 10-K facts")
path = REPORTS / f"{ticker}_panel_facts.json"
try:
    report, output = load_report(ticker) if refresh or not path.exists() else (json.loads(path.read_text()), "Loaded saved panel facts.")
except RuntimeError as error:
    st.error(str(error)); st.stop()

st.subheader(f"{report['company']} ({ticker})")
chart = [{"Fiscal year end": r["fiscal_year_end"], "Owner earnings": None if r["owner_earnings"] is None else r["owner_earnings"] / 1_000_000, "Net income": None if r["net_income"] is None else r["net_income"] / 1_000_000} for r in report["rows"]]
st.line_chart(chart, x="Fiscal year end", y=["Owner earnings", "Net income"])
st.dataframe([{"Fiscal year end": r["fiscal_year_end"], "Revenue": money(r["revenue"]), "Net income": money(r["net_income"]), "Operating cash flow": money(r["operating_cash_flow"]), "Capital spending": money(r["capital_spending"]), "Equity": money(r["equity"]), "Current ratio": "not known" if r["current_ratio"] is None else f"{r['current_ratio']:.2f}x", "Liabilities / equity": "not known" if r["liabilities_to_equity"] is None else f"{r['liabilities_to_equity']:.2f}x", "ROE": "not known" if r["roe"] is None else f"{r['roe']:.2%}", "Owner earnings": money(r["owner_earnings"])} for r in report["rows"]], hide_index=True, use_container_width=True)

st.subheader("Panel checks")
checks = [{"Investor": investor, "Check": label, "Result": result} for investor, rows in report["panel_checks"].items() for label, result in rows.items()]
st.dataframe(checks, hide_index=True, use_container_width=True)

memo_specs = [("Buffett", f"{ticker}_buffett_memo.md"), ("Graham", f"{ticker}_graham_memo.md"), ("Burry", f"{ticker}_burry_memo.md")]
memo_results = []
for investor, filename in memo_specs:
    memo_path = REPORTS / filename
    if not memo_path.exists():
        memo_results.append({"Investor": investor, "Memo": None, "Verdict": "Memo not found", "Unprinted numbers": "Memo not found"})
        continue
    memo = memo_path.read_text(encoding="utf-8")
    verdict = re.search(r"\*\*(?:Verdict|Judgment):\s*([^*]+)\*\*", memo)
    flagged = audit(memo, report)
    memo_results.append({"Investor": investor, "Memo": memo, "Verdict": verdict.group(1).strip() if verdict else "Verdict not found", "Unprinted numbers": ", ".join(flagged) if flagged else "None"})

st.subheader("Panel verdicts")
st.dataframe([{"Investor": result["Investor"], "Verdict": result["Verdict"]} for result in memo_results], hide_index=True, use_container_width=True)
st.subheader("Memo-number audit across panel")
st.dataframe([{"Investor": result["Investor"], "Unprinted numbers": result["Unprinted numbers"]} for result in memo_results], hide_index=True, use_container_width=True)

st.subheader("Investor memos")
columns = st.columns(3)
for column, result in zip(columns, memo_results):
    with column:
        st.markdown(f"### {result['Investor']}")
        if result["Memo"] is None:
            st.warning("Memo not found")
            continue
        st.markdown(result["Memo"])
        if result["Unprinted numbers"] != "None":
            st.error("Unprinted: " + result["Unprinted numbers"])
        else:
            st.success("Memo numbers verified")

with st.expander("Exact script output"):
    st.code(output)
