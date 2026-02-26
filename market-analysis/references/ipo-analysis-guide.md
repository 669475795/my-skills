# IPO Analysis Guide

## Markets Overview

### A-Share (China Mainland)
- **Exchanges**: Shanghai (SSE), Shenzhen (SZSE)
- **Boards**: Main Board, STAR Market (688xxx), ChiNext (300xxx)
- **Data Sources**: 东方财富, 巨潮资讯
- **Key Features**: Lottery system, price limits on first day

### Hong Kong (HKEX)
- **Types**: Main Board, GEM
- **Data Sources**: HKEX Disclosure, 东方财富
- **Key Features**: 孖展 (margin) financing, dark market trading

### US (NASDAQ/NYSE)
- **Filing**: SEC EDGAR (S-1 filing)
- **Data Sources**: NASDAQ IPO Calendar, SEC
- **Key Features**: No price limits, direct listings possible

## IPO Scoring Model

### Factor Weights
| Factor | Weight | Description |
|--------|--------|-------------|
| PE vs Industry | 30% | Valuation comparison |
| Subscription Rate | 20% | Demand indicator |
| Market Sentiment | 15% | Overall market mood |
| Underwriter Quality | 10% | Track record |
| Financials | 25% | Growth, profitability |

### Score Interpretation
- **80+**: Strong buy signal
- **65-79**: Favorable conditions
- **50-64**: Neutral, consider other factors
- **35-49**: Below average prospects
- **<35**: Avoid

## Key Metrics

### A-Share IPO
```
中签率 (Lottery Rate): Lower = more oversubscribed
网上申购倍数: Online subscription multiple
发行市盈率: Issue P/E ratio
行业市盈率: Industry average P/E
募集资金: Funds raised
```

### Hong Kong IPO
```
认购倍数 (Subscription Multiple): Total demand/supply
孖展认购: Margin-financed subscriptions
暗盘价格: Dark market pre-listing price
基石投资者: Cornerstone investors
保荐人: Sponsor
```

### US IPO
```
Issue Price Range: Expected pricing
Shares Offered: Float size
Use of Proceeds: Where money goes
Lock-up Period: Insider selling restriction
Underwriters: Lead banks
```

## Analysis Workflow

### 1. Pre-IPO Research
```bash
# Get upcoming IPOs
python fetch_ipo_data.py --market A-SHARE --upcoming

# Get IPO details
python fetch_ipo_data.py 301XXX.SZ --details

# Analyze prospectus
python fetch_ipo_data.py 301XXX.SZ --prospectus
```

### 2. Valuation Analysis
```bash
# Score the IPO
python ipo_analysis.py 301XXX.SZ --pe 30 --industry-pe 25 --score

# Compare to industry
python ipo_analysis.py 301XXX.SZ --compare --industry technology
```

### 3. Prediction
```bash
# Predict first day return
python ipo_analysis.py 301XXX.SZ --predict --subscription-rate 500
```

## Red Flags

### Warning Signs
1. **Valuation**: P/E significantly above industry
2. **Timing**: IPO during market downturn
3. **Underwriter**: Unknown or poor track record
4. **Financials**: Declining revenue, negative margins
5. **Use of Proceeds**: Vague or debt repayment focused
6. **Related Party**: Excessive related party transactions

### Due Diligence Checklist
- [ ] Read prospectus key sections
- [ ] Check underwriter history
- [ ] Compare valuation to peers
- [ ] Review financial trends
- [ ] Assess market conditions
- [ ] Check cornerstone investors (HK)
- [ ] Review lock-up terms

## Historical Patterns

### A-Share First Day Performance
- Pre-2014 reform: Often 44% limit hit
- Post-reform: More variable, still often strong
- STAR Market: High volatility, no price limits

### HK IPO Patterns
- Strong subscription → Usually positive first day
- Weak subscription → Risk of break issue
- 孖展 multiple > 100x often correlates with gains

### US IPO Patterns
- "Hot" IPOs often pop then fade
- Direct listings have mixed results
- SPAC performance highly variable

## Risk Management

### Position Sizing
- Never allocate >5% to single IPO
- Consider using lottery/allocation amounts
- Plan exit strategy before entry

### Exit Strategy
- Set profit targets (e.g., +20%, +50%)
- Have stop-loss level
- Consider partial exits at targets
