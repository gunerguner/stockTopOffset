
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


def _left_pad(text: str, w: int) -> str:
    """左对齐：文本靠左，右边补空格"""
    real_width = _width(text)
    if real_width >= w:
        return text[:w]  # 截断超长文本
    return text + ' ' * (w - real_width)


def _right_pad(text: str, w: int) -> str:
    """右对齐：文本靠右，左边补空格"""
    real_width = _width(text)
    if real_width >= w:
        return text[:w]  # 截断超长文本
    return ' ' * (w - real_width) + text


def _cell(val: str, is_sister: bool) -> str:
    return f"{Color.GREEN}{val}{Color.RESET}" if is_sister else val


def print_table(results: List[StockData], use_color: bool = True) -> None:
    headers = ['股票代码', '公司名称', '市值 (B)', '实时价格', '历史最高价', '差异百分比', '距最高天数', '分析结论']
    # 增加列宽以确保对齐
    widths = [12, 12, 14, 14, 14, 12, 12, 14]
    sep = '+-' + '-+-'.join('-' * w for w in widths) + '-+'

    def row(cells: List[str]) -> str:
        # 字符串列左对齐，数值列右对齐
        align_left = [True, True, False, False, False, False, False, True]
        padded = []
        for c, w, left in zip(cells, widths, align_left):
            if left:
                padded.append(_left_pad(c, w))
            else:
                padded.append(_right_pad(c, w))
        return '| ' + ' | '.join(padded) + ' |'

    print(sep)
    print(row(headers))
    print(sep)
    for r in results:
        sis = r.get('is_sister', False)
        con = str(r['conclusion'])
        con_cell = (_CONCLUSION_COLOR.get(con, '') + con + (Color.RESET if con in _CONCLUSION_COLOR else '')) if use_color else con
        cells = [
            (_cell(str(r['ticker']), sis) if use_color else str(r['ticker'])),
            (_cell(str(r['name']), sis) if use_color else str(r['name'])),
            (_cell(f"{r['market_cap'] / 1e9:.2f}", sis) if use_color else f"{r['market_cap'] / 1e9:.2f}"),
            (_cell(f"{r['current_price']:.2f}", sis) if use_color else f"{r['current_price']:.2f}"),
            (_cell(f"{r['all_time_high']:.2f}", sis) if use_color else f"{r['all_time_high']:.2f}"),
            (_cell(f"{r['percentage_diff']:.2f}%", sis) if use_color else f"{r['percentage_diff']:.2f}%"),
            (_cell(f"{r['ath_days']}天", sis) if use_color else f"{r['ath_days']}天"),
            con_cell,
        ]
        print(row(cells))
    print(sep)

