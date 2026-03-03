---
name: market-analysis
description: >-
  Financial market analysis for stocks, bonds, options, crypto, metals, and
  macroeconomic data. Use for investment analysis, technical/fundamental
  analysis, IPO evaluation, portfolio management, sector rotation, cross-asset
  macro analysis, and market research. Supports US, Hong Kong, China A-share
  markets. Triggers on stock/crypto tickers, "分析", "行情", "市场", "投资",
  "估值", "板块", "宏观", "配置", "打新", "链上", IPO queries, and
  portfolio/risk questions.
---

# Market Analysis Skill

## Workflow - Start Here

**Step 1: Classify the request** using the table below.
**Step 2: Follow the matching workflow** from `references/ai-workflow.md`.
**Step 3: Load relevant reference files** only as needed.

| Request Type | Workflow | Primary References |
|-------------|---------|-------------------|
| Single stock/ETF analysis | Asset Analysis | `technical-indicators.md`, `fundamental-analysis.md` |
| Market overview / 大盘 | Market Overview | `cross-asset.md`, `sector-rotation.md` |
| Portfolio review / allocation | Portfolio Analysis | `investment-frameworks.md`, `risk-metrics-guide.md` |
| IPO analysis | IPO Analysis | `ipo-analysis-guide.md` |
| Macro / rates / Fed | Macro Analysis | `cross-asset.md`, `macro-economics-guide.md` |
| Crypto / on-chain / DeFi | Crypto Analysis | `crypto-onchain.md` |
| Sector / industry rotation | Sector Analysis | `sector-rotation.md` |
| Options / derivatives | Options Analysis | `options-strategies.md` |
| Bonds / yield curve | Bond Analysis | `bond-analysis-guide.md` |
| Gold / precious metals | Metals Analysis | `precious-metals-guide.md` |

**For detailed workflow steps and output standards, read: [`references/ai-workflow.md`](references/ai-workflow.md)**

---

## Output Requirements

Every analysis MUST include (in order):
1. **Verdict first**: Bullish / Bearish / Neutral - state it immediately
2. **Signal strength**: Strong / Moderate / Weak with confidence %
3. **Key data points**: 3-5 specific numbers supporting verdict
4. **Price levels**: current, target, stop-loss, support/resistance
5. **Risk factors**: At least 2 specific risks that could invalidate thesis
6. **Disclaimer**: Brief investment risk note

Never use vague language ("might go up") - always state specific targets and levels.

---

## Supported Markets & Asset Classes

### Equities
- **US**: NYSE, NASDAQ (AAPL, TSLA, MSFT)
- **Hong Kong**: HKEX (00700.HK, 09988.HK)
- **China A-Shares**: SSE/SZSE (600519.SS, 000001.SZ)

### Fixed Income
- US Treasuries (Bills, Notes, Bonds)
- Corporate Bonds (IG, HY)
- China Government & Corporate Bonds

### Derivatives
- US Options (Calls, Puts, multi-leg strategies)
- Futures (Commodities, Indices)

### Commodities
- Precious Metals: Gold, Silver, Platinum, Palladium
- Energy: Crude Oil, Natural Gas
- Agricultural: Corn, Wheat, Soybeans

### Cryptocurrencies
- Major: Bitcoin, Ethereum
- Altcoins: BNB, SOL, XRP, etc.
- On-chain and DeFi analysis

### Macroeconomic Data
- **US**: GDP, CPI, Employment, Fed Funds Rate
- **China**: GDP, CPI, PMI, PBoC Rates

---

## Core Scripts Reference

### Data Fetching
```bash
python scripts/fetch_stock_data.py {TICKER} --period 1y --metrics
python scripts/fetch_crypto_realtime.py {COIN} --detailed
python scripts/fetch_macro_data.py --summary --rates --inflation
python scripts/fetch_news.py {TICKER} --type recent
python scripts/fetch_precious_metals.py gold --period 1y
python scripts/fetch_ipo_data.py --market A-SHARE --upcoming
```

### Analysis
```bash
python scripts/technical_analysis.py {TICKER} --indicators SMA,RSI,MACD,BB
python scripts/sentiment_analysis.py fear-greed
python scripts/sentiment_analysis.py vix
python scripts/risk_management.py var --ticker {TICKER} --confidence 0.95
python scripts/portfolio_analytics.py --backtest --tickers "{TICKERS}" --weights "{WEIGHTS}"
python scripts/options_analysis.py greeks --spot {PRICE} --strike {STRIKE} --time {DAYS} --vol {VOL}
```

### Visualization
```bash
python scripts/chart_generator.py {TICKER} --period 3mo --indicators sma,volume
python scripts/chart_generator.py --compare --tickers "{T1},{T2},{T3}" --period 1y
python scripts/chart_generator.py --heatmap --tickers "{TICKERS}"
```

---

## Reference Documentation

| Document | Load When |
|----------|-----------|
| [`ai-workflow.md`](references/ai-workflow.md) | Always - start here for workflow |
| [`fundamental-analysis.md`](references/fundamental-analysis.md) | Stock valuation, earnings, DCF, red flags |
| [`crypto-onchain.md`](references/crypto-onchain.md) | Crypto/DeFi/on-chain analysis |
| [`sector-rotation.md`](references/sector-rotation.md) | Sector analysis, industry rotation |
| [`cross-asset.md`](references/cross-asset.md) | Macro regime, cross-asset correlations |
| [`technical-indicators.md`](references/technical-indicators.md) | Indicator calculations and signals |
| [`investment-frameworks.md`](references/investment-frameworks.md) | Portfolio construction, decision checklists |
| [`risk-metrics-guide.md`](references/risk-metrics-guide.md) | VaR, Sharpe, position sizing |
| [`ipo-analysis-guide.md`](references/ipo-analysis-guide.md) | IPO scoring and analysis |
| [`options-strategies.md`](references/options-strategies.md) | Options Greeks and strategies |
| [`bond-analysis-guide.md`](references/bond-analysis-guide.md) | Duration, convexity, yield curve |
| [`precious-metals-guide.md`](references/precious-metals-guide.md) | Gold/Silver/Platinum analysis |
| [`macro-economics-guide.md`](references/macro-economics-guide.md) | Economic indicators interpretation |
| [`visualization-guide.md`](references/visualization-guide.md) | Chart generation options |
| [`market-apis.md`](references/market-apis.md) | Data sources and API usage |
| [`market-codes.md`](references/market-codes.md) | Ticker formats by market |

## Report Templates

| Template | Use For |
|----------|---------|
| [`analysis_report.md`](templates/analysis_report.md) | Single asset analysis |
| [`ipo_report.md`](templates/ipo_report.md) | IPO analysis |
| [`portfolio_report.md`](templates/portfolio_report.md) | Portfolio review |
| [`risk_report.md`](templates/risk_report.md) | Risk assessment |

---

## Dependencies

```bash
pip install -r requirements.txt
# Core: yfinance, pandas, numpy, requests, beautifulsoup4
# Visualization: matplotlib, mplfinance, plotly, kaleido
# Analysis: scipy, scikit-learn
# Macro: fredapi (requires FRED_API_KEY)
```

## Environment Variables

```bash
export FRED_API_KEY=your_api_key        # Required for macro data
export FUTU_HOST=127.0.0.1              # Optional: Futu OpenAPI
export FUTU_PORT=11111
export TIGER_ID=your_tiger_id           # Optional: Tiger Brokers
export IB_HOST=127.0.0.1               # Optional: Interactive Brokers
export IB_PORT=7497
```

## Data Limitations

- Stock data: ~15 min delay (Yahoo Finance)
- Crypto data: 1-2 min delay (CoinGecko)
- FRED API key required for macro data
- China data sources may have access restrictions
- Options data: US-only via Yahoo Finance

## Disclaimer

Analysis is for educational purposes only - not financial advice. Always conduct own research, consult licensed advisors, and understand investment risks.
