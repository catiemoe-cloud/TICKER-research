"""Meridian Foundation Reserve mandate checker (USD millions and percent weights)."""

# Editable inputs
HOLDINGS = [
    {"holding": "Cash", "issuer": "none", "days_to_redeem": 0, "reserve_eligible": True},
    {"holding": "Treasury bills", "issuer": "U.S. Treasury", "days_to_redeem": 1, "reserve_eligible": True},
    {"holding": "Treasury 10-year note", "issuer": "U.S. Treasury", "days_to_redeem": 1, "reserve_eligible": True},
    {"holding": "Global equity index fund", "issuer": "diversified fund", "days_to_redeem": 2, "reserve_eligible": False},
    {"holding": "Investment-grade bond fund", "issuer": "diversified fund", "days_to_redeem": 3, "reserve_eligible": False},
    {"holding": "Private real estate fund", "issuer": "diversified fund", "days_to_redeem": 90, "reserve_eligible": False},
    {"holding": "Acme Corp bonds", "issuer": "Acme Corp", "days_to_redeem": 4, "reserve_eligible": False},
    {"holding": "Acme Corp stock", "issuer": "Acme Corp", "days_to_redeem": 1, "reserve_eligible": False},
]

CANDIDATES = {
    "A": {
        "Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
        "Global equity index fund": 60, "Investment-grade bond fund": 26,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 55, "Investment-grade bond fund": 20,
        "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
        "Global equity index fund": 70, "Investment-grade bond fund": 20,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8,
    },
    # Candidate D is an intentional edge case for the CIO question.
    "D": {
        "Cash": 3, "Treasury bills": 0, "Treasury 10-year note": 97,
        "Global equity index fund": 0, "Investment-grade bond fund": 0,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    # Candidate E is the Meridian S4 benchmark: 40% IG bonds and 60% equity.
    "E": {
        "Cash": 0, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 60, "Investment-grade bond fund": 40,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
}

RESERVE_SIZE = 100.0
QUARTERLY_DISTRIBUTION = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_DAYS = 5
MINIMUM_LIQUID_SHARE = 90.0
ISSUER_LIMIT = 8.0
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def status(condition):
    return "pass" if condition else "FAIL"


def candidate_value(weights, holding_name):
    return weights.get(holding_name, 0.0)


def check_candidate(name, weights):
    total_weight = sum(candidate_value(weights, item["holding"]) for item in HOLDINGS)
    lowest_weight = min(candidate_value(weights, item["holding"]) for item in HOLDINGS)
    reserve_eligible_weight = sum(
        candidate_value(weights, item["holding"])
        for item in HOLDINGS
        if item["reserve_eligible"]
    )
    liquid_weight = sum(
        candidate_value(weights, item["holding"])
        for item in HOLDINGS
        if item["days_to_redeem"] <= LIQUIDITY_WINDOW_DAYS
    )

    issuer_weights = {}
    for item in HOLDINGS:
        issuer = item["issuer"]
        if issuer not in EXEMPT_ISSUERS:
            issuer_weights[issuer] = issuer_weights.get(issuer, 0.0) + candidate_value(
                weights, item["holding"]
            )
    largest_company_weight = max(issuer_weights.values(), default=0.0)

    results = [
        ("Weights sum to 100", total_weight, total_weight == 100.0),
        ("Long-only (lowest weight)", lowest_weight, lowest_weight >= 0.0),
        ("Reserve-eligible weight", reserve_eligible_weight, reserve_eligible_weight >= reserve_minimum),
        (
            f"Redeemable in {LIQUIDITY_WINDOW_DAYS} days",
            liquid_weight,
            liquid_weight >= MINIMUM_LIQUID_SHARE,
        ),
        ("Largest single company", largest_company_weight, largest_company_weight <= ISSUER_LIMIT),
    ]

    print(f"\nCandidate {name}")
    failures = 0
    for label, value, passed in results:
        print(f"{label}: {value:.1f}% {status(passed)}")
        failures += not passed
    print("Calendar-year loss: requires CIO clarification")
    if failures == 0:
        print("Verdict: passes every checkable rule")
    else:
        print(f"Verdict: fails {failures} rule(s)")


reserve_minimum = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100.0


def main():
    print(f"Reserve minimum: {reserve_minimum:.1f}% of the portfolio")
    for name, weights in CANDIDATES.items():
        check_candidate(name, weights)


if __name__ == "__main__":
    main()
