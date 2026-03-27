"""显示与表格格式化"""

import re
from typing import List
from unicodedata import east_asian_width

from formatters import to_billions
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


def _format_change(value: float, use_color: bool) -> str:
    """格式化涨跌幅，正值绿色，负值红色"""
    if value is None:
        return "N/A"
    formatted = f"{value:+.2f}%"
    if use_color:
        if value > 0:
            return f"{Color.GREEN}{formatted}{Color.RESET}"
        elif value < 0:
            return f"{Color.RED}{formatted}{Color.RESET}"
    return formatted


def print_table(results: List[StockData], use_color: bool = True,
                show_weekly: bool = False, show_daily: bool = False) -> None:
    # 动态构建表头和列宽
    headers = ['股票代码', '公司名称', '市值 (B)', '实时价格', '历史最高价', '差异百分比', '距最高天数']
    widths = [12, 12, 14, 14, 14, 12, 12]

    if show_weekly:
        headers.append('周涨跌幅')
        widths.append(12)
    if show_daily:
        headers.append('日涨跌幅')
        widths.append(12)

    headers.append('分析结论')
    widths.append(14)

    sep = '+-' + '-+-'.join('-' * w for w in widths) + '-+'

    def row(cells: List[str], align_left: List[bool]) -> str:
        padded = []
        for c, w, left in zip(cells, widths, align_left):
            if left:
                padded.append(_left_pad(c, w))
            else:
                padded.append(_right_pad(c, w))
        return '| ' + ' | '.join(padded) + ' |'

    # 动态构建对齐方式：字符串列左对齐，数值列右对齐
    align_left = [True, True, False, False, False, False, False]
    if show_weekly:
        align_left.append(False)
    if show_daily:
        align_left.append(False)
    align_left.append(True)

    print(sep)
    print(row(headers, align_left))
    print(sep)
    for r in results:
        sis = r.get('is_sister', False)
        con = str(r['conclusion'])
        con_cell = (_CONCLUSION_COLOR.get(con, '') + con + (Color.RESET if con in _CONCLUSION_COLOR else '')) if use_color else con
        market_cap_b = f"{to_billions(r['market_cap_usd']):.2f}"

        cells = [
            (_cell(str(r['ticker']), sis) if use_color else str(r['ticker'])),
            (_cell(str(r['name']), sis) if use_color else str(r['name'])),
            (_cell(market_cap_b, sis) if use_color else market_cap_b),
            (_cell(f"{r['current_price']:.2f}", sis) if use_color else f"{r['current_price']:.2f}"),
            (_cell(f"{r['all_time_high']:.2f}", sis) if use_color else f"{r['all_time_high']:.2f}"),
            (_cell(f"{r['percentage_diff']:.2f}%", sis) if use_color else f"{r['percentage_diff']:.2f}%"),
            (_cell(f"{r['ath_days']}天", sis) if use_color else f"{r['ath_days']}天"),
        ]

        if show_weekly:
            weekly = r.get('weekly_change')
            cells.append(_format_change(weekly, use_color) if weekly is not None else "N/A")

        if show_daily:
            daily = r.get('daily_change')
            cells.append(_format_change(daily, use_color) if daily is not None else "N/A")

        cells.append(con_cell)

        print(row(cells, align_left))
    print(sep)
