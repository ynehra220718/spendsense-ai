"""
Product and price history analysis helpers used by the Product Intelligence Agent.
Pure functions — no API calls, no side effects.
"""
from datetime import datetime, timedelta
from statistics import median


def parse_price_history(price_history: list[dict]) -> list[dict]:
    """Parses and sorts price history by date ascending."""
    parsed = []
    for entry in price_history:
        try:
            parsed.append({
                "date": datetime.strptime(entry["date"], "%Y-%m-%d"),
                "price": float(entry["price"]),
            })
        except (KeyError, ValueError):
            continue
    return sorted(parsed, key=lambda x: x["date"])


def compute_median_price(price_history: list[dict]) -> float:
    prices = [e["price"] for e in price_history]
    return median(prices) if prices else 0.0


def filter_anomalous_prices(
    price_history: list[dict],
    min_duration_days: int = 3,
    max_drop_pct: float = 0.40,
) -> tuple[list[dict], list[dict]]:
    """
    Filters out prices that are likely errors or flash anomalies.

    Rules:
      1. Exclude prices sustained for fewer than min_duration_days consecutive days.
      2. Exclude prices more than max_drop_pct below the median.

    Returns:
      (clean_history, excluded_entries)
    """
    if not price_history:
        return [], []

    parsed = parse_price_history(price_history)
    median_price = compute_median_price(parsed)
    threshold = median_price * (1 - max_drop_pct)

    clean, excluded = [], []

    for i, entry in enumerate(parsed):
        price = entry["price"]

        # Rule 2: too far below median
        if price < threshold:
            excluded.append({**entry, "reason": f"Price ${price:.2f} is more than {int(max_drop_pct*100)}% below median ${median_price:.2f}"})
            continue

        # Rule 1: check duration — how many consecutive days at this price?
        duration = _compute_price_duration_days(parsed, i)
        if duration < min_duration_days:
            excluded.append({**entry, "reason": f"Price ${price:.2f} lasted only {duration} day(s) — below {min_duration_days}-day minimum"})
            continue

        clean.append(entry)

    return clean, excluded


def _compute_price_duration_days(parsed: list[dict], index: int) -> int:
    """
    Estimates how many days a price at a given index was active,
    measured as the gap to the next price change.
    """
    if index >= len(parsed) - 1:
        # Last entry — assume it's still active; treat as long duration
        return 30

    current_price = parsed[index]["price"]
    current_date = parsed[index]["date"]

    # Find next entry with a different price
    for j in range(index + 1, len(parsed)):
        if parsed[j]["price"] != current_price:
            return (parsed[j]["date"] - current_date).days

    # All remaining entries have the same price — assume long duration
    return (parsed[-1]["date"] - current_date).days + 1


def find_sensible_lowest_price(price_history: list[dict]) -> dict | None:
    """
    Returns the lowest price entry that survives anomaly filtering.
    Returns None if price_history is empty.
    """
    clean, _ = filter_anomalous_prices(price_history)
    if not clean:
        return None
    return min(clean, key=lambda x: x["price"])


def summarise_price_trend(price_history: list[dict]) -> str:
    """Returns a one-sentence human-readable trend description."""
    parsed = parse_price_history(price_history)
    if len(parsed) < 2:
        return "Insufficient price history to determine trend."

    first_price = parsed[0]["price"]
    last_price = parsed[-1]["price"]
    change_pct = ((last_price - first_price) / first_price) * 100

    if change_pct > 10:
        return f"Price has risen {change_pct:.0f}% over the tracked period (from ${first_price:.2f} to ${last_price:.2f})."
    elif change_pct < -10:
        return f"Price has dropped {abs(change_pct):.0f}% over the tracked period (from ${first_price:.2f} to ${last_price:.2f})."
    else:
        return f"Price has been relatively stable, ranging from ${min(e['price'] for e in parsed):.2f} to ${max(e['price'] for e in parsed):.2f}."
