#!/usr/bin/env python3
"""Annual 10-K facts and deterministic Buffett checks from keyless SEC EDGAR."""

import argparse
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
USER_AGENT = os.environ.get("SEC_EDGAR_USER_AGENT")
FLOW_TAGS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"],
    "net_income": ["NetIncomeLoss"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capital_spending": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
}
EQUITY_TAG = "StockholdersEquity"
LIABILITIES_TAG = "Liabilities"
DISPLAY = {
    "revenue": "Revenue",
    "net_income": "Net income",
    "operating_cash_flow": "Operating cash flow",
    "capital_spending": "Capital spending",
    "equity": "Equity",
    "roe": "ROE",
    "owner_earnings": "Owner earnings",
}


def fetch_json(url):
    if not USER_AGENT:
        raise RuntimeError(
            "Set SEC_EDGAR_USER_AGENT to a contact string such as "
            "'Your Name your.email@example.com' before downloading from SEC EDGAR."
        )
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except (HTTPError, URLError, TimeoutError) as error:
        raise RuntimeError(f"SEC EDGAR download failed: {error}") from error


def cik_for_ticker(ticker):
    ticker = ticker.upper()
    for row in fetch_json(TICKERS_URL).values():
        if row["ticker"].upper() == ticker:
            return int(row["cik_str"]), row["title"]
    raise ValueError(f"Ticker {ticker} was not found in SEC company_tickers.json")


def annual_duration(entry):
    if not entry.get("start") or not entry.get("end"):
        return False
    days = (date.fromisoformat(entry["end"]) - date.fromisoformat(entry["start"])).days
    return 300 <= days <= 380


def latest_by_end(entries, flows):
    """Use one-year 10-K flows or year-end 10-K instants; latest filed wins."""
    candidates = []
    for entry in entries:
        if entry.get("form") != "10-K" or not entry.get("end"):
            continue
        if flows and not annual_duration(entry):
            continue
        if not flows and entry.get("start") and not annual_duration(entry):
            continue
        try:
            filed = entry.get("filed", "0000-00-00")
            datetime.fromisoformat(entry["end"])
        except ValueError:
            continue
        candidates.append(entry)
    chosen = {}
    for entry in candidates:
        current = chosen.get(entry["end"])
        if current is None or entry.get("filed", "") > current.get("filed", ""):
            chosen[entry["end"]] = entry
    return chosen


def fact_series(facts, tags, flows):
    """Select the first permitted tag available for each fiscal-year end."""
    combined = {}
    for tag in tags:
        concept = facts.get("us-gaap", {}).get(tag, {})
        entries = concept.get("units", {}).get("USD", [])
        selected = latest_by_end(entries, flows)
        for end, entry in selected.items():
            if end not in combined:
                combined[end] = {**entry, "_tag": tag}
    return "not found", combined


def money(value):
    """Display all dollar facts in the lab's required USD-millions unit."""
    return "not found" if value is None else f"${value / 1_000_000:,.0f}"


def percent(value):
    return "not known" if value is None else f"{value:.2%}"


def cell(value, tag=None):
    shown = money(value)
    if tag == "not found":
        return "not found"
    return f"{shown} [{tag}]" if tag else shown


def check_text(value):
    if value is None:
        return "not known"
    return "PASS" if value else "FAIL"


def build_history(ticker):
    cik, company = cik_for_ticker(ticker)
    facts = fetch_json(FACTS_URL.format(cik=cik))["facts"]
    selected = {}
    for key, tags in FLOW_TAGS.items():
        selected[key] = fact_series(facts, tags, flows=True)
    selected["equity"] = fact_series(facts, [EQUITY_TAG], flows=False)
    selected["liabilities"] = fact_series(facts, [LIABILITIES_TAG], flows=False)

    available_ends = set()
    for key, (_, series) in selected.items():
        if key == "liabilities":
            continue
        available_ends.update(series)
    ends = sorted(available_ends)[-5:]
    rows = []
    for end in ends:
        row = {"fiscal_year_end": end}
        for key, (_, series) in selected.items():
            entry = series.get(end)
            row[key] = entry.get("val") if entry else None
            row[f"{key}_tag"] = entry["_tag"] if entry else "not found"
        income = row["net_income"]
        equity = row["equity"]
        row["roe"] = income / equity if income is not None and equity is not None and equity > 0 else None
        row["liabilities_to_equity"] = (
            row["liabilities"] / equity
            if row["liabilities"] is not None and equity is not None and equity > 0
            else None
        )
        row["owner_earnings"] = (
            row["operating_cash_flow"] - row["capital_spending"]
            if row["operating_cash_flow"] is not None and row["capital_spending"] is not None
            else None
        )
        rows.append(row)

    roe_check = None if any(row["roe"] is None for row in rows) else all(row["roe"] >= 0.15 for row in rows)
    owner_positive = None if any(row["owner_earnings"] is None for row in rows) else all(row["owner_earnings"] > 0 for row in rows)
    owner_growth = None
    if len(rows) == 5 and rows[0]["owner_earnings"] is not None and rows[-1]["owner_earnings"] is not None:
        owner_growth = rows[-1]["owner_earnings"] > rows[0]["owner_earnings"]
    return {
        "ticker": ticker.upper(), "company": company, "cik": f"{cik:010d}", "rows": rows,
        "checks": {
            "ROE at least 15% every year": check_text(roe_check),
            "Owner earnings positive every year": check_text(owner_positive),
            "Owner earnings grew, first year to last": check_text(owner_growth),
        },
    }


def print_report(report):
    print(f"{report['company']} ({report['ticker']}) | CIK {report['cik']} | 10-K annual facts | USD millions")
    headers = ["Fiscal year end", "Revenue", "Net income", "Operating cash flow", "Capital spending", "Equity", "ROE", "Owner earnings"]
    print(" | ".join(headers))
    for row in report["rows"]:
        values = [
            row["fiscal_year_end"], cell(row["revenue"], row["revenue_tag"]),
            cell(row["net_income"], row["net_income_tag"]), cell(row["operating_cash_flow"], row["operating_cash_flow_tag"]),
            cell(row["capital_spending"], row["capital_spending_tag"]), cell(row["equity"], row["equity_tag"]),
            f"{percent(row['roe'])} [computed: NetIncomeLoss / StockholdersEquity]",
            f"{money(row['owner_earnings'])} [computed: operating cash flow - capital spending]",
        ]
        print(" | ".join(values))
    print("\nBuffett checks")
    for label, result in report["checks"].items():
        print(f"- {label}: {result}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker")
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()
    report = build_history(args.ticker)
    print_report(report)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
