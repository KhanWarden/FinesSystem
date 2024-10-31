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
                   numerical_discount: Optional[str] = None,
                   prepayment: Optional[str] = None):
    if prepayment:
        prepayment = int(prepayment.replace(".", ""))
    else:
        prepayment = 0
    if range_value:
        range_value = int(range_value.replace(".", ""))
    else:
        range_value = 0
    if numerical_discount:
        numerical_discount = int(numerical_discount.replace(".", ""))
    else:
        numerical_discount = 0

    start_sum = duration_calculation(guests_amount, duration)

    if percentage_discount:
        start_sum = subtract_percentage_game_sum(start_sum, percentage_discount)

    total_sum = start_sum + range_value - numerical_discount - prepayment

    return total_sum


def detailed_count_game_sum(guests_amount: int,
                            duration: int,
                            range_value: Optional[str] = None,
                            percentage_discount: Optional[int] = None,
                            numerical_discount: Optional[str] = None,
                            prepayment: Optional[str] = None) -> str:
    range_value = int(range_value.replace(".", "")) if range_value else 0
    numerical_discount = int(numerical_discount.replace(".", "")) if numerical_discount else 0
    prepayment = int(prepayment.replace(".", "")) if prepayment else 0

    start_sum = duration_calculation(guests_amount, duration)
    details = []

    if guests_amount <= 16:
        details.append(f"{start_sum:,} (фикс.) = {start_sum:,}")
    else:
        if duration == 60:
            cost_per_person = prices["1_hour"]["17-25"] if guests_amount <= 25 else prices["1_hour"][
                "26-34"] if guests_amount <= 34 else prices["1_hour"]["35"]
        elif duration == 90:
            cost_per_person = prices["1.5_hours"]["17-25"] if guests_amount <= 25 else prices["1.5_hours"][
                "26-34"] if guests_amount <= 34 else prices["1.5_hours"]["35"]
        else:  # duration == 120
            cost_per_person = prices["2_hours"]["17-25"] if guests_amount <= 25 else prices["2_hours"][
                "26-34"] if guests_amount <= 34 else prices["2_hours"]["35"]

        total_guests_cost = cost_per_person * guests_amount
        details.append(f"{total_guests_cost:,} ({guests_amount} участников * {cost_per_person:,})")

    total_sum = start_sum

    if percentage_discount:
        discounted_sum = subtract_percentage_game_sum(total_sum, percentage_discount)
        details.append(f"-{percentage_discount}% скидка = {discounted_sum:,}")
        total_sum = discounted_sum

    total_sum -= numerical_discount
    if numerical_discount != 0:
        details.append(f"{total_sum + numerical_discount:,} - {numerical_discount:,} (Скидка в сумме) = {total_sum:,}")

    total_sum += range_value
    if range_value != 0:
        details.append(f"+ {range_value:,} (За дальность) = {total_sum:,}")

    if prepayment != 0:
        total_sum -= prepayment
        details.append(f"- {prepayment:,} (ПО) = {total_sum:,}")

    return "\n".join(details)


def subtract_percentage_game_sum(start_sum, percentage_discount):
    return int(start_sum * (1 - percentage_discount / 100))


def duration_calculation(guests_amount, duration) -> float:
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
