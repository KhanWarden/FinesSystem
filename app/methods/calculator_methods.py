from typing import Optional

prices = {
    "1_hour": {
        "fix": 100000,
        "16-25": 6000,
        "26-34": 5500,
        "35": 4500
    },
    "1.5_hours": {
        "fix": 150000,
        "16-25": 9000,
        "26-34": 8250,
        "35": 6750
    },
    "2_hours": {
        "fix": 200000,
        "16-25": 12000,
        "26-34": 11000,
        "35": 9000
    }
}


def count_game_sum(guests_amount: int,
                   duration: int,
                   range_value: Optional[str] = None,
                   percentage_discount: Optional[int] = None,
                   numerical_discount: Optional[str] = None):

    pass
