# Precious Metals Analysis Guide

## Overview

Precious metals (gold, silver, platinum, palladium) serve as:
- Safe haven assets during market uncertainty
- Inflation hedges
- Portfolio diversifiers
- Industrial commodities (silver, platinum, palladium)

## Key Symbols

| Metal | Futures | Spot | Primary ETF |
|-------|---------|------|-------------|
| Gold | GC=F | XAUUSD=X | GLD |
| Silver | SI=F | XAGUSD=X | SLV |
| Platinum | PL=F | - | PPLT |
| Palladium | PA=F | - | PALL |

## Gold/Silver Ratio

The gold/silver ratio measures how many ounces of silver equal one ounce of gold.

### Historical Context
- **Long-term average**: ~60-65
- **Historical range**: 15 (1980) to 125 (2020)
- **Current interpretation**:
  - Ratio > 80: Silver potentially undervalued
  - Ratio < 50: Gold potentially undervalued
  - Ratio 50-80: Normal range

### Trading Strategy
- **Mean reversion**: Trade the ratio's return to historical average
- **Relative value**: Go long undervalued metal, short overvalued

## Dollar Correlation

Gold typically has **negative correlation** with USD:
- Strong dollar → Lower gold prices
- Weak dollar → Higher gold prices

### Key Indicators
- DXY (Dollar Index): ^DX-Y.NYB
- When DXY rises, watch for gold weakness
- Correlation can break during flight-to-quality events

## Price Drivers

### Gold
1. **Real interest rates** (nominal rates - inflation)
2. **USD strength**
3. **Geopolitical uncertainty**
4. **Central bank purchases**
5. **ETF flows**

### Silver
1. **Gold price direction**
2. **Industrial demand (50% of consumption)**
3. **Solar panel production**
4. **Electronics manufacturing**

### Platinum/Palladium
1. **Auto industry catalytic converter demand**
2. **EV adoption trends (negative)**
3. **Mining supply disruptions**
4. **Substitution dynamics**

## Technical Analysis Tips

### Key Levels for Gold
- Psychological levels: $1800, $1900, $2000, $2100
- All-time high: Track for breakout/resistance
- 200-day moving average: Major trend indicator

### Seasonality
- Gold often strong in Q1 and Q4
- Summer months typically weaker
- Indian wedding season (Oct-Nov) supports demand

## CLI Usage

```bash
# Current gold price
python fetch_precious_metals.py gold

# All metals
python fetch_precious_metals.py all

# Gold/Silver ratio
python fetch_precious_metals.py --ratio

# Gold ETFs
python fetch_precious_metals.py --etfs gold

# Historical analysis
python fetch_precious_metals.py gold --history --period 2y

# USD correlation
python fetch_precious_metals.py --correlation gold
```

## Investment Considerations

### Allocation Guidelines
- Typical portfolio allocation: 5-15%
- Higher allocation during uncertainty
- Rebalance when allocation drifts >5%

### Physical vs Paper
- **Physical**: Storage costs, insurance, liquidity constraints
- **ETFs**: Liquid, low cost, counterparty risk
- **Futures**: Leverage, contango costs, rolling

### Tax Considerations (US)
- Collectibles tax rate (28%) for physical
- ETF taxation varies by structure
- Consult tax advisor for specifics
