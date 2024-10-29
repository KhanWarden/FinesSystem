from typing import Optional

prices = {
    "1_hour": {
        "fix": 100000,
        "17-25": 6000,
        "26-34": 5500,
        "35": 4500
    },
    "1.5_hours": {
        "fix": 150000,
        "17-25": 9000,
        "26-34": 8250,
        "35": 6750
    },
    "2_hours": {
        "fix": 200000,
        "17-25": 12000,
        "26-34": 11000,
        "35": 9000
    }
}


def count_game_sum(guests_amount: int,
                   duration: int,
                   range_value: Optional[str] = None,
                   percentage_discount: Optional[int] = None,
                   numerical_discount: Optional[str] = None):
    range_value = int(range_value.replace(".", ""))
    numerical_discount = int(numerical_discount.replace(".", ""))

    start_sum = duration_calculation(guests_amount, duration)

    if percentage_discount:
        start_sum = subtract_percentage_game_sum(start_sum, percentage_discount)

    total_sum = start_sum + range_value - numerical_discount

    return total_sum


def detailed_count_game_sum(guests_amount: int,
                             duration: int,
                             range_value: Optional[str] = None,
                             percentage_discount: Optional[int] = None,
                             numerical_discount: Optional[str] = None) -> str:

    range_value = int(range_value.replace(".", "")) if range_value else 0
    numerical_discount = int(numerical_discount.replace(".", "")) if numerical_discount else 0

    start_sum = duration_calculation(guests_amount, duration)
    details = [f"{start_sum:,} (fix)"]

    if guests_amount <= 16:
        details.append(f"{start_sum:,} (fix) = {start_sum:,}")
    else:
        if duration == 60:
            cost_per_person = prices["1_hour"]["17-25"] if guests_amount <= 25 else prices["1_hour"]["26-34"] if guests_amount <= 34 else prices["1_hour"]["35"]
        elif duration == 90:
            cost_per_person = prices["1.5_hours"]["17-25"] if guests_amount <= 25 else prices["1.5_hours"]["26-34"] if guests_amount <= 34 else prices["1.5_hours"]["35"]
        else:  # duration == 120
            cost_per_person = prices["2_hours"]["17-25"] if guests_amount <= 25 else prices["2_hours"]["26-34"] if guests_amount <= 34 else prices["2_hours"]["35"]

        total_guests_cost = cost_per_person * guests_amount
        details.append(f"{total_guests_cost:,} (for {guests_amount} guests at {cost_per_person:,} each)")

    total_sum = start_sum + range_value
    details.append(f"{start_sum:,} + {range_value:,} = {total_sum:,}")

    if percentage_discount:
        discounted_sum = subtract_percentage_game_sum(total_sum, percentage_discount)
        details.append(f"{total_sum:,} - {percentage_discount}% скидка = {discounted_sum:,}")
        total_sum = discounted_sum

    total_sum -= numerical_discount
    details.append(f"{total_sum + numerical_discount:,} - {numerical_discount:,} (За дальность) = {total_sum:,}")

    return "\n".join(details)


def subtract_percentage_game_sum(start_sum, percentage_discount):
    return start_sum * (1 - percentage_discount / 100)


def duration_calculation(guests_amount: int, duration: int) -> float:
    duration_map = {
        60: "1_hour",
        90: "1.5_hours",
        120: "2_hours"
    }

    price_key = duration_map.get(duration)
    if not price_key:
        raise ValueError(f"Invalid duration: {duration}")

    if guests_amount <= 16:
        return prices[price_key]["fix"]
    elif guests_amount <= 25:
        return prices[price_key]["17-25"] * guests_amount
    elif guests_amount <= 34:
        return prices[price_key]["26-34"] * guests_amount
    else:
        return prices[price_key]["35"] * guests_amount
