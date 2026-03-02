"""美股价格分析 - 主入口"""

import argparse
from datetime import datetime
from typing import List

from config import STOCKS, SEVEN_SISTERS, CRYPTOS
from models import StockData
from data_fetcher import fetch_all_stocks
from analyzer import parse_stock_info
from ai_service import prepare_analysis_data, analyze_with_ai, save_ai_analysis
from display import print_table


def _analyze_assets(assets, title, use_ai, no_color, show_title=True):
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
        print_table(results, use_color=not no_color)
        if use_ai:
            print("\n" + "=" * 100 + "\nAI 智能分析\n" + "=" * 100 + "\n")
            data = prepare_analysis_data(results)
            analysis = analyze_with_ai(data)
            print(analysis)
            path = save_ai_analysis(analysis)
            print(f"\n✅ 报告已保存：{path}")

    if errors:
        print(f"\n获取失败：{', '.join(errors)}")

    return results, errors


def main(use_ai: bool = False, no_color: bool = False, show_crypto: bool = False, show_stocks: bool = False) -> None:
    # 如果没有指定任何参数，默认显示股票
    if not show_crypto and not show_stocks:
        show_stocks = True

    # 显示股票
    if show_stocks:
        _analyze_assets(STOCKS, "美股价格分析报告", use_ai, no_color)

    # 显示加密货币（如果两个都显示，中间加换行分隔）
    if show_crypto:
        if show_stocks:
            print("\n")
        _analyze_assets(CRYPTOS, "加密货币价格分析报告", use_ai, no_color)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='美股价格分析')
    p.add_argument('--ai', action='store_true', help='启用 AI 分析')
    p.add_argument('--no-color', action='store_true', help='不显示颜色（用于生成 txt）')
    p.add_argument('-c', '--crypto', action='store_true', help='获取比特币和以太坊数据')
    p.add_argument('-s', '--stocks', action='store_true', help='获取美股数据')
    args = p.parse_args()

    main(use_ai=args.ai, no_color=args.no_color, show_crypto=args.crypto, show_stocks=args.stocks)
