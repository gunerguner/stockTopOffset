# Stock Top Offset - 资产价格分析工具

一个用于分析美股科技股、贵金属和加密货币价格位置的 Python 工具。自动获取实时价格，计算与历史最高价的偏离程度，并生成 AI 分析报告。

## 功能特性

- **实时数据获取**: 使用 yfinance 获取美股和加密货币实时行情
- **价格偏离分析**: 计算当前价格与历史最高价的百分比偏离
- **AI 智能分析**: 调用智谱 AI 生成专业的投资分析报告
- **彩色表格输出**: 终端友好的彩色表格展示，区分科技七姐妹与其他股票
- **自动定时报告**: 支持 GitHub Actions 定时运行并生成报告

## 支持的股票

### 科技七姐妹 (突出显示)
- AAPL (苹果)、MSFT (微软)、GOOGL (谷歌)、AMZN (亚马逊)
- NVDA (英伟达)、META (Meta)、TSLA (特斯拉)

### 其他科技股
TSM (台积电)、INTC (英特尔)、AMD、QCOM (高通)、MU (美光)、IBM、AVGO (博通)、ORCL (甲骨文)、ASML (阿斯麦)、ADBE (Adobe)、NFLX (奈飞)、CSCO (思科)

### 加密货币
BTC-USD (比特币)、ETH-USD (以太坊)

### 贵金属
GC=F (黄金)、SI=F (白银)

## 快速开始

### 安装依赖

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 配置

项目通过环境变量读取智谱 AI Key，推荐使用 `.env`：

```bash
cp .env.example .env  # 如果你有模板文件
# 或手动创建 .env 并写入
echo "AI_API_KEY=your-api-key-here" >> .env
```

也可以直接在当前 shell 导出：

```bash
export AI_API_KEY="your-api-key-here"
```

### 运行分析

```bash
# 默认分析美股
python main.py

# 只分析贵金属（黄金、白银）
python main.py -m

# 只分析加密货币（比特币、以太坊）
python main.py -c

# 分析美股和贵金属
python main.py -s -m

# 分析所有类型
python main.py -s -m -c

# 启用 AI 智能分析
python main.py --ai

# 显示周涨跌幅（约 5 个交易日）
python main.py -w

# 显示日涨跌幅（前一交易日对比）
python main.py -d

# 同时显示周/日涨跌幅并启用 AI 分析
python main.py -s -m -c -w -d --ai

# 不显示颜色（适合输出到文件）
python main.py --no-color
```

> 说明：不传 `-s/-m/-c` 时，默认分析美股（`stocks`）。

## 输出示例

```
+------------+------------+--------------+--------------+--------------+--------------+--------------+----------------+
| 股票代码   | 公司名称   |   市值 (B)   |   实时价格   |  历史最高价  |  差异百分比  |  距最高天数  | 分析结论       |
+------------+------------+--------------+--------------+--------------+--------------+--------------+----------------+
| AAPL       | 苹果       |         3.50 |       185.00 |       199.60 |       -7.31% |         45天 | 适度回调       |
| NVDA       | 英伟达     |         2.20 |       875.00 |       974.00 |      -10.16% |         12天 | 显著回调       |
| BTC-USD    | 比特币     |         1.30 |     67500.00 |     73750.00 |       -8.47% |         30天 | 适度回调       |
+------------+------------+--------------+--------------+--------------+--------------+--------------+----------------+
```

AI 分析报告将保存在 `report/YYYY-MM-DD.txt` 文件中。


### 数据字段说明

- 内部统一使用 `market_cap_usd` 表示美元单位市值。
- 展示层与 AI 分析层统一通过 `to_billions(value)` 转换为 `B`（十亿美元）单位，避免重复手写换算。
- `daily_change`：相对前一交易日收盘价的涨跌幅（%）。
- `weekly_change`：相对约 5 个交易日前收盘价的涨跌幅（%）。

## GitHub Actions 自动运行

项目配置了 GitHub Actions 工作流，可以定时自动运行分析:

- **定时触发**: 每周一至周五北京时间 08:30 自动运行
- **手动触发**: 支持通过 Actions 页面手动触发

### 配置 GitHub Actions

1. 在 GitHub 仓库设置中添加 Secrets（可选）:
   - `AI_API_KEY`: 你的智谱 AI API Key

2. 工作流文件位置: `.github/workflows/stock_analysis.yml`

## 项目结构

```
stockTopOffset/
├── main.py                 # 程序入口
├── config.py               # 配置文件（股票列表、API Key等）
├── models.py               # 数据模型定义
├── analyzer.py             # 数据分析和结论生成
├── ai_service.py           # AI 分析服务
├── display.py              # 表格格式化显示
├── prompt.txt              # AI 分析提示词模板
├── requirements.txt        # Python 依赖
├── report/                 # 生成的分析报告目录
└── .github/workflows/      # GitHub Actions 配置
```

## 自定义配置

### 添加/修改股票

在 `config.py` 中编辑 `STOCKS` 列表:

```python
STOCKS = [
    ('AAPL', '苹果'),
    ('TSLA', '特斯拉'),
    # 添加更多股票...
]
```

### 修改 AI 模型

在 `config.py` 中修改 AI 配置:

```python
AI_MODEL = "glm-4.5-air"  # 或其他智谱AI模型
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 4096
```

### 调整并发与重试

在 `config.py` 中可调整：

```python
MAX_WORKERS = 8
MAX_RETRY_TIMES = 1
RETRY_DELAY_SECONDS = 2
```

## 依赖项

- yfinance >= 0.2.36 - Yahoo Finance 数据获取
- pandas >= 2.0.0 - 数据处理
- python-dotenv >= 1.0.0 - 环境变量加载（`from dotenv import load_dotenv`）
- zai-sdk - 智谱 AI SDK

说明：项目当前使用了自定义表格渲染逻辑（`display.py`），未依赖 `tabulate`、`wcwidth`。

## 免责声明

本项目仅供参考学习，不构成任何投资建议。股市有风险，投资需谨慎。

## License

MIT License
