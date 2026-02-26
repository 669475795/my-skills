---
name: market-analysis
description: Financial market analysis for stocks, bonds, options, crypto, metals, and macroeconomic data. Use for investment analysis, technical/fundamental analysis, IPO evaluation, portfolio management, and market research.
---

# Market Analysis Skill

Analyze financial markets and provide data-driven investment insights for stocks, bonds, options, commodities, and cryptocurrencies across global markets.

## Supported Markets & Asset Classes

### Equities
- **US Stocks**: NYSE, NASDAQ (e.g., AAPL, TSLA, MSFT)
- **Hong Kong Stocks**: HKEX (e.g., 00700.HK, 09988.HK)
- **China A-Shares**: Shanghai/Shenzhen (e.g., 600519.SS, 000001.SZ)

### Fixed Income
- **US Treasuries**: Bills, Notes, Bonds
- **Corporate Bonds**: Investment Grade, High Yield
- **China Bonds**: Government, Corporate

### Derivatives
- **US Options**: Calls, Puts, Strategies
- **Futures**: Commodities, Indices

### Commodities
- **Precious Metals**: Gold, Silver, Platinum, Palladium
- **Energy**: Crude Oil, Natural Gas
- **Agricultural**: Corn, Wheat, Soybeans

### Cryptocurrencies
- **Major**: Bitcoin, Ethereum
- **Altcoins**: BNB, SOL, XRP, etc.

### Macroeconomic Data
- **US**: GDP, CPI, Employment, Fed Funds
- **China**: GDP, CPI, PMI, PBoC Rates

---

## Quick Start

### Basic Stock Analysis

```bash
# Fetch and analyze stock data
python scripts/fetch_stock_data.py AAPL --period 1y --metrics

# Technical analysis
python scripts/technical_analysis.py AAPL --indicators SMA,RSI,MACD
```

### IPO Analysis (NEW)

```bash
# A-Share IPO calendar
python scripts/fetch_ipo_data.py --market A-SHARE --upcoming

# Hong Kong IPO
python scripts/fetch_ipo_data.py --market HK --upcoming

# US IPO
python scripts/fetch_ipo_data.py --market US --upcoming

# IPO scoring and prediction
python scripts/ipo_analysis.py 301XXX.SZ --score --predict
```

### Precious Metals

```bash
# Gold price and analysis
python scripts/fetch_precious_metals.py gold --period 1y

# Gold/Silver ratio
python scripts/fetch_precious_metals.py --ratio

# All metals overview
python scripts/fetch_precious_metals.py --all
```

### Bond Analysis

```bash
# Yield curve
python scripts/bond_analysis.py curve

# Bond pricing
python scripts/bond_analysis.py price --face 1000 --coupon 0.05 --ytm 0.04 --years 10

# Duration analysis
python scripts/bond_analysis.py duration --face 1000 --coupon 0.05 --ytm 0.04 --years 10
```

### Options Analysis

```bash
# Option chain
python scripts/fetch_options.py AAPL --expiry 2024-01-19

# Greeks calculation
python scripts/options_analysis.py greeks --spot 185 --strike 190 --time 30 --vol 0.25 --rate 0.05

# Strategy analysis
python scripts/options_analysis.py strategy --type covered_call --spot 185 --positions "100,1"
```

### Risk Management

```bash
# Position sizing
python scripts/risk_management.py position --account 100000 --risk 0.02 --entry 50 --stop 45

# VaR calculation
python scripts/risk_management.py var --ticker AAPL --confidence 0.95

# Portfolio stress test
python scripts/risk_management.py stress --value 100000
```

### Macroeconomic Data

```bash
# US economic summary
python scripts/fetch_macro_data.py --summary

# Interest rates
python scripts/fetch_macro_data.py --rates

# Inflation data
python scripts/fetch_macro_data.py --inflation

# China macro
python scripts/fetch_macro_data.py --china
```

### Charts & Visualization

```bash
# Candlestick chart with indicators
python scripts/chart_generator.py AAPL --period 3mo --indicators sma,volume

# Comparison chart
python scripts/chart_generator.py --compare --tickers "AAPL,MSFT,GOOGL" --period 1y

# Correlation heatmap
python scripts/chart_generator.py --heatmap --tickers "AAPL,MSFT,GOOGL,AMZN,META"

# Portfolio allocation pie
python scripts/portfolio_charts.py allocation --holdings '{"AAPL": 30, "MSFT": 25, "GOOGL": 20}'
```

### Sentiment Analysis

```bash
# Fear & Greed Index
python scripts/sentiment_analysis.py fear-greed

# VIX analysis
python scripts/sentiment_analysis.py vix

# Put/Call ratio
python scripts/sentiment_analysis.py put-call --ticker SPY
```

### Paper Trading

```bash
# Connect to simulated broker
python scripts/broker_interface.py connect --broker simulated

# Place order
python scripts/paper_trading.py buy --symbol AAPL --quantity 100

# Check positions
python scripts/paper_trading.py positions

# Performance report
python scripts/paper_trading.py performance
```

---

## Module Reference

### Data Fetching

| Script | Purpose | Key Options |
|--------|---------|-------------|
| `fetch_stock_data.py` | Stock quotes & history | `--period`, `--metrics` |
| `fetch_crypto_data.py` | Crypto via Yahoo | `--period`, `--compare` |
| `fetch_crypto_realtime.py` | Crypto via CoinGecko | `--detailed`, `--chart` |
| `fetch_news.py` | Market news | `--sources`, `--type` |
| `fetch_ipo_data.py` | IPO calendar & data | `--market`, `--upcoming` |
| `fetch_precious_metals.py` | Gold, Silver, Platinum | `--ratio`, `--all` |
| `fetch_macro_data.py` | Economic indicators | `--rates`, `--inflation` |
| `fetch_bonds.py` | Bond yields & ETFs | `--curve`, `--spreads` |
| `fetch_options.py` | Option chains | `--expiry`, `--type` |

### Analysis Modules

| Script | Purpose | Key Options |
|--------|---------|-------------|
| `technical_analysis.py` | Standard indicators | `--indicators` |
| `advanced_technical.py` | Fibonacci, Pivots | `--fib`, `--pivots` |
| `ipo_analysis.py` | IPO scoring | `--score`, `--predict` |
| `options_analysis.py` | Greeks, strategies | `--greeks`, `--strategy` |
| `bond_analysis.py` | Duration, convexity | `--price`, `--duration` |
| `sentiment_analysis.py` | Fear/Greed, VIX | `--fear-greed`, `--vix` |
| `risk_management.py` | VaR, position sizing | `--var`, `--position` |
| `portfolio_analytics.py` | Backtest, optimize | `--backtest`, `--optimize` |

### Visualization

| Script | Purpose | Output |
|--------|---------|--------|
| `chart_generator.py` | Price charts | PNG, HTML |
| `portfolio_charts.py` | Portfolio visuals | PNG, HTML |

### Trading Interface

| Script | Purpose | Notes |
|--------|---------|-------|
| `broker_interface.py` | Broker abstraction | Simulated default |
| `paper_trading.py` | Paper trading | Risk controls |

### Infrastructure

| Script | Purpose |
|--------|---------|
| `cache_manager.py` | Data caching |
| `rate_limiter.py` | API rate limiting |
| `data_validator.py` | Data validation |
| `china_data_sources.py` | EastMoney, Sina, CNInfo |

---

## IPO Analysis (Detailed)

### Supported Markets

#### A-Share (China)
- **Data Source**: EastMoney, CNInfo
- **Features**: Subscription calendar, winning numbers, prospectus links
- **Scoring**: Industry PE comparison, subscription demand, financials

```bash
# Upcoming A-share IPOs
python scripts/fetch_ipo_data.py --market A-SHARE --upcoming

# Detailed IPO info
python scripts/fetch_ipo_data.py 301XXX.SZ --details

# Score and predict
python scripts/ipo_analysis.py 301XXX.SZ --score --predict
```

#### Hong Kong
- **Data Source**: HKEX Disclosure, EastMoney
- **Features**: Public/placement split, margin multiples, grey market
- **Scoring**: Sponsor track record, cornerstone investors

```bash
# Upcoming HK IPOs
python scripts/fetch_ipo_data.py --market HK --upcoming

# Subscription tracking
python scripts/fetch_ipo_data.py 09999.HK --subscription
```

#### US
- **Data Source**: SEC EDGAR, NASDAQ
- **Features**: S-1 filings, price range, lock-up dates
- **Scoring**: Underwriter quality, sector valuation

```bash
# Upcoming US IPOs
python scripts/fetch_ipo_data.py --market US --upcoming

# S-1 filing details
python scripts/fetch_ipo_data.py TICKER --s1-filing
```

### IPO Scoring Model

| Factor | Weight | Description |
|--------|--------|-------------|
| Valuation vs Industry | 30% | PE/PS compared to peers |
| Subscription Demand | 20% | Oversubscription ratio |
| Market Sentiment | 15% | Fear/Greed, sector momentum |
| Underwriter Quality | 10% | Historical performance |
| Financials | 25% | Revenue growth, margins, ROE |

---

## Options Analysis (Detailed)

### Greeks Calculation

```bash
# Calculate all Greeks
python scripts/options_analysis.py greeks \
  --spot 185 \
  --strike 190 \
  --time 30 \
  --vol 0.25 \
  --rate 0.05 \
  --type call
```

| Greek | Measures |
|-------|----------|
| Delta | Price sensitivity |
| Gamma | Delta change rate |
| Theta | Time decay |
| Vega | Volatility sensitivity |
| Rho | Interest rate sensitivity |

### Strategy Templates

```bash
# Covered call
python scripts/options_analysis.py strategy --type covered_call --spot 185

# Iron condor
python scripts/options_analysis.py strategy --type iron_condor --spot 185

# Bull call spread
python scripts/options_analysis.py strategy --type bull_call_spread --spot 185
```

Available strategies: `covered_call`, `protective_put`, `bull_call_spread`, `bear_put_spread`, `iron_condor`, `straddle`, `strangle`, `butterfly`

---

## Risk Management (Detailed)

### Position Sizing

```bash
# Fixed percentage method
python scripts/risk_management.py position \
  --account 100000 \
  --risk 0.02 \
  --entry 50 \
  --stop 45
```

### Value at Risk (VaR)

```bash
# Single asset VaR
python scripts/risk_management.py var --ticker AAPL --confidence 0.95

# Portfolio VaR
python scripts/risk_management.py var \
  --tickers "AAPL,MSFT,GOOGL" \
  --weights "0.4,0.3,0.3" \
  --value 100000
```

Methods: Historical, Parametric, Monte Carlo

### Stress Testing

```bash
# Historical scenarios
python scripts/risk_management.py stress --value 100000

# Scenarios tested:
# - 2008 Financial Crisis
# - 2020 COVID Crash
# - Market -20%
# - VIX spike to 80
```

### Kelly Criterion

```bash
python scripts/risk_management.py kelly --win-rate 0.55 --win-loss-ratio 2.0
```

---

## Bond Analysis (Detailed)

### Yield Curve

```bash
# Current yield curve
python scripts/bond_analysis.py curve

# Spread analysis (2Y-10Y)
python scripts/bond_analysis.py spread
```

### Bond Pricing

```bash
# Price a bond
python scripts/bond_analysis.py price \
  --face 1000 \
  --coupon 0.05 \
  --ytm 0.04 \
  --years 10
```

### Duration & Convexity

```bash
python scripts/bond_analysis.py duration \
  --face 1000 \
  --coupon 0.05 \
  --ytm 0.04 \
  --years 10
```

---

## Precious Metals (Detailed)

### Gold Analysis

```bash
# Current gold price
python scripts/fetch_precious_metals.py gold

# Historical chart
python scripts/fetch_precious_metals.py gold --period 1y --chart

# Gold vs USD correlation
python scripts/fetch_precious_metals.py gold --correlation
```

### Gold/Silver Ratio

```bash
python scripts/fetch_precious_metals.py --ratio

# Interpretation:
# > 80: Silver undervalued (consider silver)
# < 50: Gold undervalued (consider gold)
# 50-80: Normal range
```

### All Metals

```bash
python scripts/fetch_precious_metals.py --all
# Returns: Gold, Silver, Platinum, Palladium prices and changes
```

---

## Macroeconomic Data (Detailed)

### US Economic Indicators

```bash
# Summary dashboard
python scripts/fetch_macro_data.py --summary

# Interest rates (Fed Funds, Treasury yields)
python scripts/fetch_macro_data.py --rates

# Inflation (CPI, Core CPI, PCE)
python scripts/fetch_macro_data.py --inflation

# Employment (Unemployment, Payrolls, Claims)
python scripts/fetch_macro_data.py --employment
```

### China Macro

```bash
python scripts/fetch_macro_data.py --china
# GDP, CPI, PMI, PBoC rates
```

### Key FRED Series

| Series | Description |
|--------|-------------|
| FEDFUNDS | Federal Funds Rate |
| DGS10 | 10-Year Treasury |
| CPIAUCSL | Consumer Price Index |
| UNRATE | Unemployment Rate |
| GDP | Gross Domestic Product |

---

## Visualization (Detailed)

### Candlestick Charts

```bash
python scripts/chart_generator.py AAPL \
  --period 3mo \
  --indicators sma,ema,bb,volume \
  --format png
```

### Comparison Charts

```bash
python scripts/chart_generator.py --compare \
  --tickers "AAPL,MSFT,GOOGL" \
  --period 1y
```

### Portfolio Charts

```bash
# Allocation pie
python scripts/portfolio_charts.py allocation \
  --holdings '{"AAPL": 30, "MSFT": 25, "GOOGL": 20, "Cash": 25}'

# Equity curve
python scripts/portfolio_charts.py equity \
  --tickers "AAPL,MSFT,GOOGL" \
  --weights "0.4,0.3,0.3" \
  --period 1y

# Risk-return scatter
python scripts/portfolio_charts.py risk-return \
  --tickers "AAPL,MSFT,GOOGL,AMZN,TSLA"
```

---

## Paper Trading (Detailed)

### Setup

```bash
# Connect to simulated broker (default)
python scripts/broker_interface.py connect --broker simulated

# Check account
python scripts/broker_interface.py account
```

### Trading

```bash
# Buy
python scripts/paper_trading.py buy --symbol AAPL --quantity 100

# Sell
python scripts/paper_trading.py sell --symbol AAPL --quantity 50

# Check positions
python scripts/paper_trading.py positions

# Close trade
python scripts/paper_trading.py close --trade-id ABC123
```

### Risk Controls

| Parameter | Default | Description |
|-----------|---------|-------------|
| max_position_size | 10% | Max per position |
| max_portfolio_risk | 2% | Max total risk |
| max_drawdown | 15% | Stop trading trigger |
| daily_loss_limit | 3% | Daily max loss |
| max_open_positions | 10 | Position count limit |

---

## Reference Documentation

| Document | Description |
|----------|-------------|
| [market-apis.md](references/market-apis.md) | Data sources & API usage |
| [market-codes.md](references/market-codes.md) | Ticker formats (stocks, bonds, options) |
| [technical-indicators.md](references/technical-indicators.md) | Indicator explanations |
| [investment-frameworks.md](references/investment-frameworks.md) | Analysis methodologies |
| [ipo-analysis-guide.md](references/ipo-analysis-guide.md) | IPO analysis framework |
| [options-strategies.md](references/options-strategies.md) | Options strategy guide |
| [bond-analysis-guide.md](references/bond-analysis-guide.md) | Bond analysis guide |
| [precious-metals-guide.md](references/precious-metals-guide.md) | Precious metals guide |
| [macro-economics-guide.md](references/macro-economics-guide.md) | Economic indicators |
| [risk-metrics-guide.md](references/risk-metrics-guide.md) | Risk management |
| [visualization-guide.md](references/visualization-guide.md) | Chart generation |
| [broker-integration-guide.md](references/broker-integration-guide.md) | Trading interface |

---

## Report Templates

| Template | Purpose |
|----------|---------|
| [analysis_report.md](templates/analysis_report.md) | Standard stock analysis |
| [ipo_report.md](templates/ipo_report.md) | IPO analysis report |
| [portfolio_report.md](templates/portfolio_report.md) | Portfolio review |
| [risk_report.md](templates/risk_report.md) | Risk assessment |

---

## Dependencies

Install all dependencies:

```bash
pip install -r requirements.txt
```

### Core
- yfinance, pandas, numpy, requests, beautifulsoup4

### Visualization
- matplotlib, mplfinance, plotly, kaleido

### Analysis
- scipy, scikit-learn

### Data Sources
- fredapi (FRED API key required)

### Utilities
- cachetools, tenacity

---

## Environment Variables

```bash
# FRED API (required for macro data)
export FRED_API_KEY=your_api_key

# Optional: Premium data sources
export FUTU_HOST=127.0.0.1
export FUTU_PORT=11111
export TIGER_ID=your_tiger_id
export IB_HOST=127.0.0.1
export IB_PORT=7497
```

---

## Best Practices

1. **Always fetch real data**: Never make up prices or statistics
2. **Provide context**: Compare to historical trends and benchmarks
3. **Multi-timeframe analysis**: Look at short and long-term trends
4. **Risk disclosure**: Always include risks and disclaimers
5. **Source attribution**: Cite data sources
6. **Cache appropriately**: Use caching to avoid API rate limits
7. **Validate data**: Check for missing or stale data

---

## Limitations

- Stock data delayed ~15 minutes (Yahoo Finance)
- Crypto data 1-2 minute delay (CoinGecko)
- FRED API key required for macro data
- Some Chinese data sources may have access restrictions
- Options data US-only via Yahoo Finance
- Paper trading is simulated (no real execution)

---

## Important Disclaimer

**This skill provides educational analysis and should not be considered financial advice. Users should:**

- Conduct their own research
- Consult licensed financial advisors
- Understand investment risks
- Never invest more than they can afford to lose
- Be aware of market volatility and potential losses
- Verify all data before making decisions
