"""美股价格分析 - 主入口"""

import argparse
from datetime import datetime
from typing import List, Tuple

from config import STOCKS, SEVEN_SISTERS, CRYPTOS, METALS
from models import StockData
from data_fetcher import fetch_all_stocks
from analyzer import parse_stock_info
from ai_service import prepare_analysis_data, analyze_with_ai, save_ai_analysis
from display import print_table

ASSET_TYPES = {
    'stocks': (STOCKS, "美股价格分析报告"),
    'metals': (METALS, "贵金属价格分析报告"),
    'crypto': (CRYPTOS, "加密货币价格分析报告"),
}


class Options:
    def __init__(self, asset_types: List[str] = None, use_ai: bool = False, no_color: bool = False,
                 weekly: bool = False, daily: bool = False):
        self.asset_types = asset_types or ['stocks']
        self.use_ai = use_ai
        self.no_color = no_color
        self.weekly = weekly
        self.daily = daily


def _analyze_assets(assets: List[Tuple[str, str]], title: str, options: Options, show_title: bool = True):
    """分析并显示指定资产数据"""
    if show_title:
        print("=" * 100)
        print(title.center(100))
        print(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(100))
        print("=" * 100 + "\n")

    info_map = fetch_all_stocks(assets)
    results: List[StockData] = []
    errors: List[str] = []

    for ticker, name in assets:
        parsed = parse_stock_info(ticker, name, info_map.get(ticker), ticker in SEVEN_SISTERS)
        if parsed:
            results.append(parsed)
        else:
            errors.append(ticker)

    if not results:
        print("错误：未能获取任何数据，请检查网络连接")
    else:
        results.sort(key=lambda r: r['percentage_diff'])
        print_table(results, use_color=not options.no_color,
                    show_weekly=options.weekly, show_daily=options.daily)
        if options.use_ai:
            print("\n" + "=" * 100 + "\nAI 智能分析\n" + "=" * 100 + "\n")
            data = prepare_analysis_data(results, include_weekly=options.weekly, include_daily=options.daily)
            analysis = analyze_with_ai(data, enable_web_search=True)
            print(analysis)
            path = save_ai_analysis(analysis)
            print(f"\n✅ 报告已保存：{path}")

    if errors:
        print(f"\n获取失败：{', '.join(errors)}")

    return results, errors


def main(options: Options) -> None:
    for idx, (key, (assets, title)) in enumerate(
        (k, v) for k, v in ASSET_TYPES.items() if k in options.asset_types
    ):
        if idx > 0:
            print("\n")
        _analyze_assets(assets, title, options)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='美股价格分析')
    parser.add_argument('--ai', action='store_true', help='启用 AI 分析')
    parser.add_argument('--no-color', action='store_true', help='不显示颜色（用于生成 txt）')
    parser.add_argument('-c', '--crypto', action='store_true', help='获取比特币和以太坊数据')
    parser.add_argument('-s', '--stocks', action='store_true', help='获取美股数据')
    parser.add_argument('-m', '--metals', action='store_true', help='获取黄金和白银数据')
    parser.add_argument('-w', '--weekly', action='store_true', help='显示周涨跌幅')
    parser.add_argument('-d', '--daily', action='store_true', help='显示日涨跌幅')
    args = parser.parse_args()

    selected = [k for k in ['crypto', 'stocks', 'metals'] if getattr(args, k)]
    main(Options(asset_types=selected, use_ai=args.ai, no_color=args.no_color,
                 weekly=args.weekly, daily=args.daily))