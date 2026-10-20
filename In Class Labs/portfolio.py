"""Meridian simple-portfolio return and risk engine (course training values)."""

import math


# Editable course-authored training inputs. Rates and volatilities are decimals.
SLEEVES = {
    "Treasury bills": {"expected_return": 0.035, "volatility": 0.005},
    "Treasury 10-year note": {"expected_return": 0.043, "volatility": 0.070},
    "Investment-grade bond fund": {"expected_return": 0.050, "volatility": 0.060},
    "Global equity index fund": {"expected_return": 0.080, "volatility": 0.160},
}

CORRELATIONS = {
    "Treasury bills": {
        "Treasury bills": 1.00,
        "Treasury 10-year note": 0.10,
        "Investment-grade bond fund": 0.05,
        "Global equity index fund": 0.00,
    },
    "Treasury 10-year note": {
        "Treasury bills": 0.10,
        "Treasury 10-year note": 1.00,
        "Investment-grade bond fund": 0.80,
        "Global equity index fund": -0.10,
    },
    "Investment-grade bond fund": {
        "Treasury bills": 0.05,
        "Treasury 10-year note": 0.80,
        "Investment-grade bond fund": 1.00,
        "Global equity index fund": 0.25,
    },
    "Global equity index fund": {
        "Treasury bills": 0.00,
        "Treasury 10-year note": -0.10,
        "Investment-grade bond fund": 0.25,
        "Global equity index fund": 1.00,
    },
}

OBJECTIVE_RETURN = 0.065  # CPI estimate of 2.5% + 4.0%
RESERVE_ELIGIBLE = {"Treasury bills", "Treasury 10-year note"}


def validate_correlations(sleeves, correlations):
    """Raise ValueError when the correlation table is incomplete or invalid."""
    names = set(sleeves)
    if set(correlations) != names:
        raise ValueError("Correlation table must have one row for every sleeve.")

    for left in names:
        if set(correlations[left]) != names:
            raise ValueError(f"Correlation row for {left!r} is incomplete.")
        for right in names:
            value = correlations[left][right]
            if not -1.0 <= value <= 1.0:
                raise ValueError(
                    f"Correlation for {left!r} and {right!r} is outside -1 to 1."
                )
            if value != correlations[right][left]:
                raise ValueError(
                    f"Correlation table is not symmetric for {left!r} and {right!r}."
                )


def covariance_matrix(sleeves, correlations):
    """Return covariance values keyed by sleeve pair."""
    return {
        left: {
            right: (
                correlations[left][right]
                * sleeves[left]["volatility"]
                * sleeves[right]["volatility"]
            )
            for right in sleeves
        }
        for left in sleeves
    }


def expected_return(weights, sleeves):
    """Calculate a portfolio's weighted expected return."""
    return sum(weights[name] * sleeves[name]["expected_return"] for name in sleeves)


def portfolio_volatility(weights, covariances):
    """Calculate sqrt(w' covariance w)."""
    variance = sum(
        weights[left] * weights[right] * covariances[left][right]
        for left in weights
        for right in weights
    )
    return math.sqrt(max(variance, 0.0))


def reserve_eligible_weight(weights):
    """Calculate the combined Treasury-bills and 10-year-note allocation."""
    return sum(weights[name] for name in RESERVE_ELIGIBLE)


def equal_weight_portfolio(sleeves):
    """Return equal weights across all sleeves."""
    weight = 1.0 / len(sleeves)
    return {name: weight for name in sleeves}


def inverse_volatility_portfolio(sleeves):
    """Return weights proportional to each sleeve's inverse volatility."""
    inverse_volatilities = {
        name: 1.0 / details["volatility"] for name, details in sleeves.items()
    }
    total = sum(inverse_volatilities.values())
    return {name: value / total for name, value in inverse_volatilities.items()}


def print_portfolio(name, weights, sleeves, covariances, objective):
    """Print one portfolio's weights, return, risk, reserve allocation, and result."""
    result_return = expected_return(weights, sleeves)
    result_volatility = portfolio_volatility(weights, covariances)
    reserve_weight = reserve_eligible_weight(weights)

    print(f"\n{name}")
    for sleeve, weight in weights.items():
        print(f"{sleeve}: {weight:.1%}")
    print(f"Expected return: {result_return:.2%}")
    print(f"Volatility: {result_volatility:.2%}")
    print(f"Reserve-eligible weight: {reserve_weight:.1%}")
    print(f"Meets {objective:.1%} objective: {'yes' if result_return >= objective else 'no'}")


def main():
    try:
        validate_correlations(SLEEVES, CORRELATIONS)
    except ValueError as error:
        print(f"Cannot calculate portfolios: {error}")
        return

    covariances = covariance_matrix(SLEEVES, CORRELATIONS)
    portfolios = {
        "Benchmark": {
            "Treasury bills": 0.0,
            "Treasury 10-year note": 0.0,
            "Investment-grade bond fund": 0.40,
            "Global equity index fund": 0.60,
        },
        "Equal weight": equal_weight_portfolio(SLEEVES),
        "Inverse volatility": inverse_volatility_portfolio(SLEEVES),
    }

    print(f"Objective return: {OBJECTIVE_RETURN:.2%} (CPI estimate 2.5% + 4.0%)")
    for name, weights in portfolios.items():
        print_portfolio(name, weights, SLEEVES, covariances, OBJECTIVE_RETURN)


if __name__ == "__main__":
    main()
