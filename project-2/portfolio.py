"""Meridian simple-portfolio return and risk engine (course training values)."""

import csv
import io
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


def reserve_eligible_weight(weights, reserve_eligible=None):
    """Calculate the combined Treasury-bills and 10-year-note allocation."""
    eligible_assets = RESERVE_ELIGIBLE if reserve_eligible is None else reserve_eligible
    return sum(weights.get(name, 0.0) for name in eligible_assets)


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


def _solve_linear_system(matrix, vector):
    """Solve a small square linear system with Gaussian elimination."""
    size = len(vector)
    augmented = [row[:] + [vector[index]] for index, row in enumerate(matrix)]
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            raise ValueError("Constraints do not identify a portfolio on this face.")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            multiplier = augmented[row][column]
            augmented[row] = [
                value - multiplier * pivot_value
                for value, pivot_value in zip(augmented[row], augmented[column])
            ]
    return [augmented[row][-1] for row in range(size)]


def _minimum_variance_on_face(names, covariances, constraints, targets):
    """Return the minimum-variance weights subject to equality constraints."""
    count = len(names)
    constraint_count = len(constraints)
    # KKT system: 2Σw + A'λ = 0, Aw = b.
    matrix = [[0.0] * (count + constraint_count) for _ in range(count + constraint_count)]
    vector = [0.0] * count + targets
    for row, left in enumerate(names):
        for column, right in enumerate(names):
            matrix[row][column] = 2.0 * covariances[left][right]
        for constraint_index, constraint in enumerate(constraints):
            matrix[row][count + constraint_index] = constraint[left]
            matrix[count + constraint_index][row] = constraint[left]
    solution = _solve_linear_system(matrix, vector)
    return {name: solution[index] for index, name in enumerate(names)}


def minimum_variance_portfolio(sleeves, correlations, objective, minimum_reserve=0.03):
    """Find the long-only minimum-volatility portfolio meeting Meridian's mandate.

    The search enumerates the small number of possible active constraints (return,
    reserve allocation, and zero-weight sleeves), then solves each candidate exactly.
    It therefore does not rely on a grid search or an external optimizer.
    """
    validate_correlations(sleeves, correlations)
    names = list(sleeves)
    covariances = covariance_matrix(sleeves, correlations)
    best = None

    # A face is defined by the sleeves allowed to have positive weights.  On each
    # face, either/both mandate inequalities may bind, or remain slack.
    for mask in range(1, 1 << len(names)):
        free_names = [names[index] for index in range(len(names)) if mask & (1 << index)]
        for return_binds in (False, True):
            for reserve_binds in (False, True):
                constraints = [{name: 1.0 for name in free_names}]
                targets = [1.0]
                if return_binds:
                    constraints.append(
                        {name: sleeves[name]["expected_return"] for name in free_names}
                    )
                    targets.append(objective)
                if reserve_binds:
                    constraints.append(
                        {name: float(name in RESERVE_ELIGIBLE) for name in free_names}
                    )
                    targets.append(minimum_reserve)
                if len(constraints) > len(free_names):
                    continue
                try:
                    partial_weights = _minimum_variance_on_face(
                        free_names, covariances, constraints, targets
                    )
                except ValueError:
                    continue
                weights = {name: partial_weights.get(name, 0.0) for name in names}
                result_return = expected_return(weights, sleeves)
                reserve_weight = reserve_eligible_weight(weights)
                if (
                    min(weights.values()) < -1e-9
                    or result_return < objective - 1e-9
                    or reserve_weight < minimum_reserve - 1e-9
                ):
                    continue
                volatility = portfolio_volatility(weights, covariances)
                if best is None or volatility < best["volatility"]:
                    best = {
                        "weights": {name: max(weight, 0.0) for name, weight in weights.items()},
                        "expected_return": result_return,
                        "reserve_weight": reserve_weight,
                        "volatility": volatility,
                    }
    if best is None:
        raise ValueError("No long-only portfolio can meet the stated mandate.")
    return best


def search_long_only_mix(
    sleeves, correlations, objective, minimum_reserve, reserve_eligible, step=0.05
):
    """Search every long-only allocation at a fixed step and return the least risky.

    Every tested weight is a non-negative multiple of ``step`` and all weights sum
    to 100%.  Return ``None`` when no mix meets the return and liquidity tests.
    """
    validate_correlations(sleeves, correlations)
    if step <= 0 or abs(round(1.0 / step) * step - 1.0) > 1e-9:
        raise ValueError("Step must divide 100% exactly.")

    names = list(sleeves)
    units = round(1.0 / step)
    covariances = covariance_matrix(sleeves, correlations)
    best = None

    def try_allocations(index, remaining, current):
        nonlocal best
        if index == len(names) - 1:
            weights = current.copy()
            weights[names[index]] = remaining * step
            result_return = expected_return(weights, sleeves)
            eligible_weight = reserve_eligible_weight(weights, reserve_eligible)
            if result_return < objective or eligible_weight < minimum_reserve:
                return
            volatility = portfolio_volatility(weights, covariances)
            if best is None or volatility < best["volatility"]:
                best = {
                    "weights": weights,
                    "expected_return": result_return,
                    "volatility": volatility,
                    "reserve_weight": eligible_weight,
                }
            return

        for units_here in range(remaining + 1):
            current[names[index]] = units_here * step
            try_allocations(index + 1, remaining - units_here, current)

    try_allocations(0, units, {})
    return best


def estimate_from_monthly_prices(csv_input, last_36_months=False):
    """Estimate annualized returns, volatilities, and correlations from prices.

    ``csv_input`` may be a path, text stream, or bytes stream. The file must have
    a date column first, oldest month first, and one price column per ticker.
    Returns are monthly price changes; the return estimate is mean × 12 and the
    volatility estimate is sample standard deviation × sqrt(12).
    """
    if hasattr(csv_input, "read"):
        contents = csv_input.read()
        if isinstance(contents, bytes):
            contents = contents.decode("utf-8-sig")
        rows = list(csv.reader(io.StringIO(contents)))
    else:
        with open(csv_input, newline="") as file:
            rows = list(csv.reader(file))

    if len(rows) < 3 or len(rows[0]) < 4:
        raise ValueError("CSV needs a date column, three or more tickers, and at least two prices.")
    headers = rows[0]
    tickers = headers[1:]
    if not 3 <= len(tickers) <= 6:
        raise ValueError("CSV needs between three and six ticker columns.")
    if not headers[0] or any(not ticker for ticker in tickers) or len(set(tickers)) != len(tickers):
        raise ValueError("CSV needs a named date column and unique ticker columns.")
    if any(len(row) != len(headers) for row in rows[1:]):
        raise ValueError("Every CSV row must contain one value for each header.")

    try:
        prices = {ticker: [float(row[index + 1]) for row in rows[1:]] for index, ticker in enumerate(tickers)}
    except ValueError as error:
        raise ValueError("Prices must be numeric.") from error
    if any(price <= 0 for values in prices.values() for price in values):
        raise ValueError("Prices must be greater than zero.")

    monthly_returns = {
        ticker: [values[index] / values[index - 1] - 1.0 for index in range(1, len(values))]
        for ticker, values in prices.items()
    }
    if last_36_months:
        monthly_returns = {ticker: values[-36:] for ticker, values in monthly_returns.items()}
    months_used = len(next(iter(monthly_returns.values())))
    if months_used < 2:
        raise ValueError("CSV needs at least three prices after selecting the time period.")

    means = {ticker: sum(values) / months_used for ticker, values in monthly_returns.items()}
    standard_deviations = {
        ticker: math.sqrt(sum((value - means[ticker]) ** 2 for value in values) / (months_used - 1))
        for ticker, values in monthly_returns.items()
    }
    if any(value == 0 for value in standard_deviations.values()):
        raise ValueError("Each ticker needs varying monthly prices to calculate correlations.")

    sleeves = {
        ticker: {
            "expected_return": means[ticker] * 12,
            "volatility": standard_deviations[ticker] * math.sqrt(12),
        }
        for ticker in tickers
    }
    correlations = {ticker: {} for ticker in tickers}
    for left_index, left in enumerate(tickers):
        for right in tickers[left_index:]:
            if left == right:
                correlation = 1.0
            else:
                covariance = sum(
                    (left_value - means[left]) * (right_value - means[right])
                    for left_value, right_value in zip(monthly_returns[left], monthly_returns[right])
                ) / (months_used - 1)
                correlation = covariance / (standard_deviations[left] * standard_deviations[right])
                # Rounding can produce 1.0000000000000002 for nearly identical data.
                correlation = max(-1.0, min(1.0, correlation))
            correlations[left][right] = correlation
            correlations[right][left] = correlation
    return {
        "sleeves": sleeves,
        "correlations": correlations,
        "months_used": months_used,
        "first_date": rows[-months_used][0],
        "last_date": rows[-1][0],
    }


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
