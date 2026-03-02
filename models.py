
"""数据模型"""

from typing import TypedDict, Optional


class StockData(TypedDict):
    ticker: str
    name: str
    current_price: float
    all_time_high: float
    price_diff: float
    percentage_diff: float
    market_cap: float
    ath_days: int
    conclusion: str
    is_sister: bool


class FetchResult(TypedDict):
    info: dict
    ath_days: Optional[int]


class Color:
    RED = '\033[91m'
    ORANGE = '\033[38;5;208m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
