"""AI 分析服务"""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

from zai import ZhipuAiClient

from config import AI_API_KEY, AI_MODEL, AI_TEMPERATURE, AI_MAX_TOKENS, PROMPT_FILE, REPORT_DIR
from formatters import to_billions
from models import StockData


def _get_client() -> Optional[ZhipuAiClient]:
    """按需创建 AI 客户端，未配置密钥时返回 None。"""
    if not AI_API_KEY.strip():
        return None
    return ZhipuAiClient(api_key=AI_API_KEY)


def prepare_analysis_data(results: List[StockData]) -> str:
    return "\n".join(
        f"{r['ticker']} ({r['name']}): 市值{to_billions(r['market_cap_usd']):.2f}B, 当前价{r['current_price']:.2f}, "
        f"历史最高{r['all_time_high']:.2f}, 回调{r['percentage_diff']:.2f}%, 距最高{r['ath_days']}天"
        for r in results
    )


def analyze_with_ai(stock_data: str) -> str:
    try:
        client = _get_client()
        if client is None:
            return "未配置 AI_API_KEY，跳过 AI 分析"

        prompt = Path(PROMPT_FILE).read_text(encoding='utf-8').format(stock_data=stock_data)
        resp = client.chat.completions.create(
            model=AI_MODEL, messages=[{"role": "user", "content": prompt}],
            temperature=AI_TEMPERATURE, max_tokens=AI_MAX_TOKENS,
        )
        return resp.choices[0].message.content or "AI未返回结果"
    except FileNotFoundError:
        return "提示词文件不存在"
    except Exception as e:
        return f"AI分析失败: {e!s}"


def save_ai_analysis(analysis: str) -> str:
    report_dir = Path(REPORT_DIR)
    report_dir.mkdir(exist_ok=True)
    path = report_dir / f"{datetime.now().strftime('%Y-%m-%d')}.txt"
    try:
        path.write_text(
            f"分析报告 - {path.stem}\n{'=' * 100}\n\n{analysis}\n\n"
            f"{'=' * 100}\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding='utf-8',
        )
        return str(path)
    except Exception as e:
        return f"保存失败: {e!s}"
