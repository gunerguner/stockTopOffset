"""数据分析与结论"""

from typing import Optional

from models import StockData, FetchResult

_CONCLUSIONS = [(5, "接近历史高点"), (20, "适度回调"), (50, "显著回调")]


def parse_stock_info(ticker: str, name: str, data: Optional[FetchResult], is_sister: bool = False) -> Optional[StockData]:
    if not data:
        return None
    info = data.get('info', {})
    cur = info.get('currentPrice') or info.get('regularMarketPrice')
    ath = info.get('allTimeHigh')
    if cur is None or ath is None:
        return None
    cur, ath = float(cur), float(ath)
    diff_pct = (cur - ath) / ath * 100
    abs_pct = abs(diff_pct)
    conclusion = "深度回调"
    for thresh, label in _CONCLUSIONS:
        if abs_pct < thresh:
            conclusion = label
            break

    # 计算日涨跌幅
    daily_change = None
    prev_close = data.get('prev_close')
    if prev_close and prev_close > 0:
        daily_change = (cur - prev_close) / prev_close * 100

    # 计算周涨跌幅
    weekly_change = None
    last_week_close = data.get('last_week_close')
    if last_week_close and last_week_close > 0:
        weekly_change = (cur - last_week_close) / last_week_close * 100

    return {
        'ticker': ticker, 'name': name, 'current_price': cur, 'all_time_high': ath,
        'price_diff': cur - ath, 'percentage_diff': diff_pct,
        'market_cap_usd': float(info.get('marketCap') or 0),
        'ath_days': data.get('ath_days') or 0,
        'conclusion': conclusion, 'is_sister': is_sister,
        'weekly_change': weekly_change, 'daily_change': daily_change,
    }
