"""美股价格分析 - 主入口"""


import argparse
from datetime import datetime
from typing import List

from config import STOCKS, SEVEN_SISTERS
from models import StockData
from data_fetcher import fetch_all_stocks
from analyzer import parse_stock_info
from ai_service import prepare_analysis_data, analyze_with_ai, save_ai_analysis
from display import print_table


def main(use_ai: bool = False) -> None:
    print("=" * 100)
    print("美股价格分析报告".center(100))
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(100))
    print("=" * 100 + "\n")

    info_map = fetch_all_stocks()
    results: List[StockData] = []
    errors: List[str] = []

    for ticker, name in STOCKS:
        parsed = parse_stock_info(ticker, name, info_map.get(ticker), ticker in SEVEN_SISTERS)
        if parsed:
            results.append(parsed)
        else:
            errors.append(ticker)

    if not results:
        print("错误: 未能获取任何股票数据，请检查网络连接")
    else:
        results.sort(key=lambda r: r['percentage_diff'])
        print_table(results)
        if use_ai:
            print("\n" + "=" * 100 + "\nAI 智能分析\n" + "=" * 100 + "\n")
            data = prepare_analysis_data(results)
            analysis = analyze_with_ai(data)
            print(analysis)
            path = save_ai_analysis(analysis)
            print(f"\n✅ 报告已保存: {path}")

    if errors:
        print(f"\n获取失败: {', '.join(errors)}")


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='美股价格分析')
    p.add_argument('--ai', action='store_true', help='启用AI分析')
    main(use_ai=p.parse_args().ai)

