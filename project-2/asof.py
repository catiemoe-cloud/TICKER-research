"""Lab 16 provenance gate: point-in-time prices and naive comparison."""

from datetime import date


# Editable inputs
DECISION_DATE = date.fromisoformat("2026-03-31")
ROWS = [
    {"row": 1, "ticker": "AAA", "month": "2026-01", "published": "2026-02-10", "price": 101.0},
    {"row": 2, "ticker": "AAA", "month": "2026-02", "published": "2026-03-10", "price": 104.0},
    {"row": 3, "ticker": "AAA", "month": "2026-03", "published": "2026-04-10", "price": 109.0},
    {"row": 4, "ticker": "AAA", "month": "2026-02", "published": "2026-03-25", "price": 103.0},
    {"row": 5, "ticker": "BBB", "month": "2026-01", "published": "2026-02-10", "price": 98.0},
    {"row": 6, "ticker": "BBB", "month": "2026-02", "published": "2026-03-10", "price": 97.0},
    {"row": 7, "ticker": "BBB", "month": "2026-02", "published": "2026-03-10", "price": 97.0},
    {"row": 8, "ticker": "BBB", "month": "2026-03", "published": "2026-04-10", "price": 92.0},
    {"row": 9, "ticker": "CCC", "month": "2026-01", "published": "2026-02-10", "price": 110.0},
    {"row": 10, "ticker": "CCC", "month": "2026-02", "published": "2026-04-05", "price": 112.0},
    {"row": 11, "ticker": "", "month": "2026-02", "published": "2026-03-10", "price": 99.0},
    {"row": 12, "ticker": "CCC", "month": "2026-02", "published": "2026-03-10", "price": 111.0},
]


def row_key(row):
    """Return every field except the original row number for duplicate matching."""
    return row["ticker"], row["month"], row["published"], row["price"]


def report_rule(label, removed):
    numbers = ", ".join(str(row["row"]) for row in removed) or "none"
    print(f"{label}: removed {len(removed)} row(s): {numbers}")


def quarantine_missing_ticker(rows):
    removed = [row for row in rows if not row["ticker"]]
    kept = [row for row in rows if row["ticker"]]
    return kept, removed


def remove_exact_duplicates(rows):
    seen = set()
    kept = []
    removed = []
    for row in rows:
        key = row_key(row)
        if key in seen:
            removed.append(row)
        else:
            seen.add(key)
            kept.append(row)
    return kept, removed


def remove_after_decision_date(rows, decision_date):
    removed = [row for row in rows if date.fromisoformat(row["published"]) > decision_date]
    kept = [row for row in rows if date.fromisoformat(row["published"]) <= decision_date]
    return kept, removed


def keep_latest_publication(rows):
    """Keep the latest publication for each ticker/month, retaining its row number."""
    latest = {}
    for row in rows:
        key = row["ticker"], row["month"]
        if key not in latest or date.fromisoformat(row["published"]) > date.fromisoformat(latest[key]["published"]):
            latest[key] = row
    kept = [row for row in rows if latest[row["ticker"], row["month"]] is row]
    removed = [row for row in rows if latest[row["ticker"], row["month"]] is not row]
    return kept, removed


def provenance_gate(rows, decision_date):
    """Apply the four required rules in order and return the admissible panel."""
    print(f"Decision date: {decision_date.isoformat()}")
    print("\nRow funnel")
    rows, removed = quarantine_missing_ticker(rows)
    report_rule("1. Quarantine missing ticker", removed)
    rows, removed = remove_exact_duplicates(rows)
    report_rule("2. Remove exact duplicate", removed)
    rows, removed = remove_after_decision_date(rows, decision_date)
    report_rule("3. Remove publication after decision date", removed)
    rows, removed = keep_latest_publication(rows)
    report_rule("4. Keep latest eligible revision", removed)
    return sorted(rows, key=lambda row: (row["ticker"], row["month"]))


def print_panel(rows, title):
    print(f"\n{title}")
    print("Row  Ticker  Month    Published   Price")
    for row in rows:
        print(f"{row['row']:>3}  {row['ticker']:<6}  {row['month']}  {row['published']}  {row['price']:>6.1f}")


def print_signals(rows, title):
    """Print the latest-month return versus its previous available month by ticker."""
    print(f"\n{title}")
    tickers = sorted({row["ticker"] for row in rows})
    for ticker in tickers:
        series = sorted((row for row in rows if row["ticker"] == ticker), key=lambda row: row["month"])
        if len(series) < 2:
            print(f"{ticker}: not enough months for a signal")
            continue
        previous, latest = series[-2], series[-1]
        signal = (latest["price"] / previous["price"] - 1) * 100
        print(f"{ticker}: {latest['month']} signal {signal:+.2f}% ({previous['price']:.1f} → {latest['price']:.1f})")


def naive_panel(rows):
    """Keep latest publications without using a decision-date filter."""
    clean_rows, _ = quarantine_missing_ticker(rows)
    clean_rows, _ = remove_exact_duplicates(clean_rows)
    panel, _ = keep_latest_publication(clean_rows)
    return sorted(panel, key=lambda row: (row["ticker"], row["month"]))


def main():
    asof_panel = provenance_gate(ROWS, DECISION_DATE)
    print_panel(asof_panel, "As-of panel")
    print_signals(asof_panel, "As-of signals")

    latest_panel = naive_panel(ROWS)
    print_panel(latest_panel, "Naive panel (ignores publication date)")
    print_signals(latest_panel, "Naive signals")


if __name__ == "__main__":
    main()
