"""股票数据获取模块"""


from typing import Dict, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import yfinance as yf

from config import STOCKS, MAX_WORKERS, MAX_RETRY_TIMES, RETRY_DELAY_SECONDS
from models import FetchResult


def _fetch_one(ticker: str) -> Optional[FetchResult]:
    """获取单只股票数据，带重试"""
    for attempt in range(MAX_RETRY_TIMES):
        try:
            t = yf.Ticker(ticker)
            info, hist = t.info, t.history(period='6y')
            ath_days = None
            if hist is not None and not hist.empty:
                ath_naive = hist['High'].idxmax().tz_localize(None)
                ath_days = (datetime.now() - ath_naive).days
            return {'info': info, 'ath_days': ath_days}
        except Exception:
            if attempt < MAX_RETRY_TIMES - 1:
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                return None
    return None


def fetch_all_stocks(assets=None) -> Dict[str, Optional[FetchResult]]:
    """并发获取所有资产数据"""
    if assets is None:
        from config import STOCKS as assets
    total = len(assets)
    asset_type = "加密货币" if assets and "BTC" in assets[0][0] else "股票"
    print(f"正在获取 {total} 只{asset_type}数据...")
    result: Dict[str, Optional[FetchResult]] = {}
    with ThreadPoolExecutor(max_workers=min(total, MAX_WORKERS)) as ex:
        fut_to_ticker = {ex.submit(_fetch_one, t): t for t, _ in assets}
        for fut in as_completed(fut_to_ticker):
            result[fut_to_ticker[fut]] = fut.result()
    ok = sum(1 for v in result.values() if v is not None)
    print(f"完成 ({ok}/{total})\n")
    return result

