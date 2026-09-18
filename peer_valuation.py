"""Peer P/E valuation for Apple (all inputs are editable)."""

from statistics import median


# Editable inputs: prices are September 10, 2026 closes; EPS is annual GAAP diluted EPS.
TARGET = {
    "ticker": "AAPL",
    "name": "Apple",
    "price": 315.34,
    "diluted_eps": 7.46,
}

PEERS = [
    {
        "ticker": "MSFT",
        "name": "Microsoft",
        "price": 492.44,
        "diluted_eps": 17.95,
    },
    {
        "ticker": "GOOGL",
        "name": "Alphabet Class A",
        "price": 332.60,
        "diluted_eps": 10.81,
    },
]


def is_positive_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def format_price(value):
    return "not meaningful" if value is None else f"${value:.2f}"


def format_multiple(value):
    return "not meaningful" if value is None else f"{value:.6f}x"


def valid_peer(peer):
    return is_positive_number(peer.get("price")) and is_positive_number(
        peer.get("diluted_eps")
    )


def implied_price(pe_multiple):
    target_eps = TARGET.get("diluted_eps")
    if pe_multiple is None or not is_positive_number(target_eps):
        return None
    return pe_multiple * target_eps


def print_removal_sensitivity(valid_peers, full_median):
    print("\nPeer-Removal Sensitivity")
    if full_median is None or not is_positive_number(TARGET.get("diluted_eps")):
        print("not meaningful: no full-peer median-implied price is available.")
        return

    full_estimate = implied_price(full_median)
    for removed_peer in valid_peers:
        remaining_multiples = [
            peer["pe"] for peer in valid_peers if peer["ticker"] != removed_peer["ticker"]
        ]
        if not remaining_multiples:
            print(f"Remove {removed_peer['ticker']}: no estimate (no peers remain).")
            continue

        remaining_estimate = implied_price(median(remaining_multiples))
        change = remaining_estimate - full_estimate
        print(
            f"Remove {removed_peer['ticker']}: remaining median-implied price "
            f"{format_price(remaining_estimate)}; change {change:+.2f}"
        )


def main():
    target_ticker = str(TARGET.get("ticker", "")).upper()
    seen_tickers = set()
    valid_peers = []

    print(f"Target: {TARGET.get('name', 'Unnamed')} ({target_ticker})")
    print(f"Target closing price: {format_price(TARGET.get('price'))}")
    print(f"Target diluted EPS: {TARGET.get('diluted_eps', 'not meaningful')}")
    if not is_positive_number(TARGET.get("price")):
        print("Target price comparison: not meaningful (missing or nonpositive price).")
    if not is_positive_number(TARGET.get("diluted_eps")):
        print("Implied prices: not meaningful (missing or nonpositive target EPS).")

    print("\nPeer P/E Multiples")
    for peer in PEERS:
        ticker = str(peer.get("ticker", "")).upper()
        if ticker == target_ticker:
            print(f"{ticker or 'Unnamed'}: excluded (target cannot be its own peer).")
            continue
        if ticker in seen_tickers:
            print(f"{ticker or 'Unnamed'}: excluded (duplicate peer).")
            continue
        seen_tickers.add(ticker)

        if not valid_peer(peer):
            print(f"{ticker or 'Unnamed'}: P/E not meaningful (missing or nonpositive price or EPS).")
            continue

        peer_with_pe = dict(peer)
        peer_with_pe["ticker"] = ticker
        peer_with_pe["pe"] = peer["price"] / peer["diluted_eps"]
        valid_peers.append(peer_with_pe)
        print(f"{ticker}: {format_multiple(peer_with_pe['pe'])}")

    if not valid_peers:
        print("\nPeer valuation: no usable peers.")
        print_removal_sensitivity(valid_peers, None)
        return

    multiples = [peer["pe"] for peer in valid_peers]
    minimum_pe = min(multiples)
    median_pe = median(multiples)
    maximum_pe = max(multiples)

    print(f"\nUsable peers: {len(valid_peers)}")
    if len(valid_peers) == 1:
        print("Peer valuation: reference estimate only; no range (one valid peer).")
        print(f"Reference peer P/E: {format_multiple(median_pe)}")
        print(f"Reference-implied price: {format_price(implied_price(median_pe))}")
        print_removal_sensitivity(valid_peers, median_pe)
        return
    else:
        print("Peer valuation: range based on minimum, median, and maximum peer P/E.")

    print(f"Minimum peer P/E: {format_multiple(minimum_pe)}")
    print(f"Median peer P/E: {format_multiple(median_pe)}")
    print(f"Maximum peer P/E: {format_multiple(maximum_pe)}")
    print(f"Minimum-implied price: {format_price(implied_price(minimum_pe))}")
    print(f"Median-implied price: {format_price(implied_price(median_pe))}")
    print(f"Maximum-implied price: {format_price(implied_price(maximum_pe))}")

    print_removal_sensitivity(valid_peers, median_pe)


if __name__ == "__main__":
    main()
