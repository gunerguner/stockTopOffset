
"""显示与表格格式化"""

import re
from typing import List
from unicodedata import east_asian_width

from models import StockData, Color

_CONCLUSION_COLOR = {
    '深度回调': Color.RED, '显著回调': Color.ORANGE,
    '适度回调': Color.YELLOW, '接近历史高点': Color.BLUE,
}


def _strip_ansi(text: str) -> str:
    return re.sub(r'\033\[[0-9;]+m', '', text)


def _width(text: str) -> int:
    return sum(2 if east_asian_width(c) in ('W', 'F') else 1 for c in _strip_ansi(text))


def _pad(text: str, w: int) -> str:
    return text + ' ' * max(w - _width(text), 0)


def _cell(val: str, is_sister: bool) -> str:
    return f"{Color.GREEN}{val}{Color.RESET}" if is_sister else val


def print_table(results: List[StockData]) -> None:
    headers = ['股票代码', '公司名称', '市值(B)', '实时价格', '历史最高价', '差异百分比', '距最高天数', '分析结论']
    widths = [10, 10, 12, 12, 12, 10, 10, 12]
    sep = '+-' + '-+-'.join('-' * w for w in widths) + '-+'

    def row(cells: List[str]) -> str:
        return '| ' + ' | '.join(_pad(c, w) for c, w in zip(cells, widths)) + ' |'

    print(sep)
    print(row(headers))
    print(sep)
    for r in results:
        sis = r.get('is_sister', False)
        con = str(r['conclusion'])
        con_cell = _CONCLUSION_COLOR.get(con, '') + con + (Color.RESET if con in _CONCLUSION_COLOR else '')
        cells = [
            _cell(str(r['ticker']), sis), _cell(str(r['name']), sis),
            _cell(f"{r['market_cap'] / 1e9:.2f}", sis), _cell(f"{r['current_price']:.2f}", sis),
            _cell(f"{r['all_time_high']:.2f}", sis), _cell(f"{r['percentage_diff']:.2f}%", sis),
            _cell(f"{r['ath_days']}天", sis), con_cell,
        ]
        print(row(cells))
    print(sep)

