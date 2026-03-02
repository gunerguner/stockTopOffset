"""配置"""

import os

from dotenv import load_dotenv

load_dotenv()

SEVEN_SISTERS = {'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA'}

STOCKS = [
    ('AAPL', '苹果'), ('MSFT', '微软'), ('GOOGL', '谷歌'), ('AMZN', '亚马逊'),
    ('NVDA', '英伟达'), ('META', 'Meta'), ('TSLA', '特斯拉'), ('TSM', '台积电'),
    ('INTC', '英特尔'), ('AMD', 'AMD'), ('QCOM', '高通'), ('MU', '美光'),
    ('IBM', 'IBM'), ('AVGO', '博通'), ('ORCL', '甲骨文'), ('ASML', '阿斯麦'),
    ('ADBE', 'Adobe'), ('NFLX', '奈飞'), ('CSCO', '思科'),
]

CRYPTOS = [
    ('BTC-USD', '比特币'),
    ('ETH-USD', '以太坊'),
]

AI_API_KEY = os.environ.get("AI_API_KEY", "")
AI_MODEL = "glm-4.5-air"
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 4096
PROMPT_FILE = "prompt.txt"
REPORT_DIR = "report"

MAX_WORKERS = 8
MAX_RETRY_TIMES = 1
RETRY_DELAY_SECONDS = 2
