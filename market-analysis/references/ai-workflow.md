# AI Analysis Workflow Guide

## Request Classification

Identify the request type first, then follow the corresponding workflow:

| Request Type | Keywords | Workflow |
|-------------|---------|---------|
| **Single Asset** | ticker, stock name, "分析XX", "看看XX" | → Asset Analysis |
| **Market Overview** | "最近市场", "今天行情", "大盘" | → Market Overview |
| **Portfolio** | "我的持仓", "配置建议", "组合" | → Portfolio Analysis |
| **IPO** | "新股", "打新", "上市" | → IPO Analysis |
| **Macro** | "美联储", "CPI", "利率", "经济" | → Macro Analysis |
| **Crypto** | BTC/ETH/crypto names, "链上", "DeFi" | → Crypto Analysis |
| **Sector** | "板块", "赛道", "行业轮动" | → Sector Analysis |
| **Screener** | "找股票", "哪些股票", "筛选" | → Screening |

---

## Workflow 1: Single Asset Analysis

Use this for any specific stock, ETF, commodity, or bond analysis.

### Step 1: Fetch Data
```bash
python scripts/fetch_stock_data.py {TICKER} --period 1y --metrics
```

### Step 2: Technical Analysis
```bash
python scripts/technical_analysis.py {TICKER} --indicators SMA,EMA,RSI,MACD,BB
```

### Step 3: Sentiment Check
```bash
python scripts/sentiment_analysis.py fear-greed
python scripts/fetch_news.py {TICKER} --type recent
```

### Step 4: Fundamental (for stocks only)
- Read `references/fundamental-analysis.md` for valuation framework
- Extract: P/E, P/B, revenue growth, ROE, debt/equity

### Step 5: Synthesize → Output
Use `templates/analysis_report.md` as structure. Always include:
- **Signal** (Bullish / Bearish / Neutral) with confidence %
- **Price levels**: current, support, resistance, target, stop-loss
- **Time horizon**: short (1-4 weeks), medium (1-3 months), long (3-12 months)
- **Risk factors**: 3 specific risks
- **Position sizing**: conservative / moderate / aggressive %

---

## Workflow 2: Market Overview

For broad market questions ("最近市场怎么样？").

### Step 1: Market Snapshot
```bash
python scripts/fetch_stock_data.py SPY QQQ DIA IWM --period 1mo --metrics
python scripts/sentiment_analysis.py fear-greed
python scripts/sentiment_analysis.py vix
```

### Step 2: Sector Heat Map
```bash
python scripts/fetch_stock_data.py XLK XLF XLE XLV XLP XLU XLB XLI XLRE XLC XLY --period 1mo
```

### Step 3: Macro Context
```bash
python scripts/fetch_macro_data.py --rates --inflation
```

### Step 4: Synthesize
- Identify: Which sectors are leading/lagging?
- Assess: Risk-on vs risk-off environment
- Read `references/cross-asset.md` for macro regime context
- Read `references/sector-rotation.md` for rotation signals

**Output format:**
```
市场概览 [日期]
├── 整体情绪: [贪婪/中性/恐惧] (Fear & Greed: XX)
├── 主要指数: SPY[+/-X%] | QQQ[+/-X%] | VIX[XX]
├── 领涨板块: [板块] +X%
├── 领跌板块: [板块] -X%
├── 宏观信号: [关键指标]
└── 近期关注: [1-2 个催化剂]
```

---

## Workflow 3: Portfolio Analysis

For portfolio review, optimization, or allocation advice.

### Step 1: Get Current Holdings
Ask user for: tickers + weights (if not provided)

### Step 2: Portfolio Metrics
```bash
python scripts/portfolio_analytics.py --backtest --tickers "{TICKERS}" --weights "{WEIGHTS}" --period 1y
python scripts/risk_management.py var --tickers "{TICKERS}" --weights "{WEIGHTS}" --value {VALUE}
```

### Step 3: Correlation Analysis
```bash
python scripts/chart_generator.py --heatmap --tickers "{TICKERS}"
```

### Step 4: Stress Test
```bash
python scripts/risk_management.py stress --value {VALUE}
```

### Step 5: Rebalancing Recommendations
- Read `references/investment-frameworks.md` for allocation guidelines
- Compare current vs target allocation
- Identify concentration risks (>15% single position, >30% single sector)

**Output uses:** `templates/portfolio_report.md`

---

## Workflow 4: Crypto Analysis

For cryptocurrency analysis requests.

### Step 1: Price & Market Data
```bash
python scripts/fetch_crypto_realtime.py {COIN} --detailed
```

### Step 2: Sentiment
```bash
python scripts/sentiment_analysis.py fear-greed  # Crypto F&G
python scripts/fetch_crypto_data.py {COIN} --period 90d
```

### Step 3: On-Chain Context
- Read `references/crypto-onchain.md` for on-chain interpretation
- Identify market cycle phase based on MVRV / NUPL if data available
- Check funding rates for leverage conditions

### Step 4: Synthesize
- Combine price action + on-chain signals + sentiment
- Cross-reference with BTC dominance trend

---

## Workflow 5: Macro Analysis

For economic data, rate decisions, central bank actions.

### Step 1: Fetch Data
```bash
python scripts/fetch_macro_data.py --summary --rates --inflation --employment
```

### Step 2: Context
- Read `references/cross-asset.md` for macro regime framework
- Identify current quadrant: (Growth↑/↓) × (Inflation↑/↓)

### Step 3: Asset Implications
- Map current macro regime to expected asset performance
- Identify sectors/assets to overweight / underweight

---

## Workflow 6: Sector Analysis

For sector rotation and industry analysis.

```bash
python scripts/fetch_stock_data.py XLK XLF XLE XLV XLP XLU XLB XLI XLRE XLC XLY --period 3mo
```

- Read `references/sector-rotation.md` for cycle mapping
- Identify which phase of economic cycle we are in
- Output top 3 overweight and top 3 underweight sectors

---

## Workflow 7: Stock Screening

For requests like "找高股息股票", "筛选低估值科技股", "哪些股票RSI超卖", "找A股ROE>20%的消费股".

### Step 1: Extract Criteria

Parse the user request into structured filters:

| Criterion Type | Examples | Data Field |
|---------------|---------|-----------|
| Valuation | P/E < 15, P/B < 1, PEG < 1 | Fundamental |
| Quality | ROE > 15%, Debt/Equity < 0.5 | Fundamental |
| Growth | Revenue growth > 20% | Fundamental |
| Technical | RSI < 30, price > SMA200, near 52W low | Technical |
| Dividend | Yield > 3% | Fundamental |
| Size | Market cap > $10B | Market data |
| Sector | Tech, Healthcare, Consumer | Classification |

### Step 2: Define Universe

Determine the stock universe based on market context:

| User Intent | Universe |
|------------|---------|
| No market specified | S&P 500 (SPY constituents) |
| US stocks | S&P 500 or NASDAQ 100 |
| A股 / 中国 | CSI 300 (沪深300) or CSI 500 |
| 港股 / HK | Hang Seng Index constituents |
| 特定板块 | Sector ETF constituents |

### Step 3: Screen

```bash
# Fetch batch data for universe
python scripts/fetch_stock_data.py {TICKER_LIST} --period 1y --metrics

# Technical screening
python scripts/technical_analysis.py {TICKER_LIST} --indicators RSI,SMA
```

For large universes (>50 stocks), screen in two passes:
1. **Hard filters**: Eliminate by strict criteria (e.g., must be profitable, market cap > threshold)
2. **Ranking**: Score remaining by how well they meet soft criteria

### Step 4: Rank & Present Results

Score each passing stock (0-100) across criteria dimensions:

```
综合得分 = Σ(criteria_score × weight)
```

Suggested weights (adjust to user's stated priority):
- Valuation: 30%
- Quality/Growth: 30%
- Technical momentum: 25%
- Dividend/Income: 15%

### Step 5: Output Format

```
筛选结果 [日期] | 条件: [user criteria summary]
筛选池: [Universe] | 通过: X / Total

排名  股票      评分   P/E   ROE   RSI   亮点
────────────────────────────────────────────
 1   TICKER   87/100  12x   24%   42   [1句核心亮点]
 2   TICKER   81/100  14x   19%   38   [1句核心亮点]
 3   TICKER   76/100  11x   22%   35   [1句核心亮点]
...

⚠ 以上为筛选结果，非投资建议。如需对某只股票深入分析，请指定ticker。
```

**Maximum results to show**: 10 stocks (offer to show more if user asks)

### Screening Shortcuts

Common pre-built screens — run directly if user uses these terms:

| Term | Criteria |
|------|---------|
| "价值股" / "低估值" | P/E < industry avg, P/B < 1.5, positive FCF |
| "高股息" | Dividend yield > 3%, payout ratio < 70%, 3yr dividend growth |
| "成长股" | Revenue growth > 20% YoY, positive EPS trend, PEG < 2 |
| "超卖" / "技术底部" | RSI < 35, price near 52W low, above 200D SMA |
| "动量股" | Price > SMA(50) > SMA(200), RSI 50-65, volume above avg |
| "质量股" | ROE > 15%, Debt/Equity < 0.5, FCF positive 3 consecutive years |

---

## Output Quality Standards

Every analysis output MUST include:

### Required Elements
1. **Verdict first**: State the conclusion upfront (Bullish/Bearish/Neutral or Buy/Hold/Sell)
2. **Evidence**: 3-5 specific data points supporting the verdict (with actual numbers)
3. **Key levels**: Price targets, stop-loss, support/resistance
4. **Risk acknowledgment**: What could invalidate the thesis
5. **Disclaimer**: Brief investment risk note

### Signal Strength
Always indicate confidence:
- **Strong** (3+ confirming signals, aligned timeframes)
- **Moderate** (2 confirming signals, some divergence)
- **Weak** (conflicting signals, high uncertainty)

### Avoid
- Vague language ("might go up", "could be good") — state specific targets
- Only technical OR only fundamental — combine when possible
- Missing risk factors — always include at least 2

---

## Data Freshness Rules

| Data Type | Acceptable Delay | Action if Stale |
|-----------|-----------------|----------------|
| Stock price | <1 hour | Re-fetch |
| Crypto price | <5 minutes | Re-fetch |
| Fundamentals | <1 day | Use with caveat |
| Macro data | <1 week | Note release date |
| Sentiment | <4 hours | Re-fetch |

---

## Handling Ambiguous Requests

| Ambiguity | Action |
|-----------|--------|
| No ticker specified | Ask user to specify asset name/ticker |
| No timeframe specified | Default to medium-term (1-3 months) |
| No portfolio size | Provide % allocation only |
| Multiple assets | Analyze top 3, offer to continue |
| Market not specified | Infer from ticker format; if unclear, ask |
