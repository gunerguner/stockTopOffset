"""数据模型"""

from typing import TypedDict, Optional


class StockData(TypedDict):
    ticker: str
    name: str
    current_price: float
    all_time_high: float
    price_diff: float
    percentage_diff: float
    market_cap_usd: float
    ath_days: int
    conclusion: str
    is_sister: bool
    weekly_change: Optional[float]  # 周涨跌幅百分比
    daily_change: Optional[float]   # 日涨跌幅百分比


class FetchResult(TypedDict):
    info: dict
    ath_days: Optional[int]
    prev_close: Optional[float]       # 前一交易日收盘价
    last_week_close: Optional[float]  # 上周收盘价（约5个交易日之前）


class Color:
    RED = '\033[91m'
    ORANGE = '\033[38;5;208m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
