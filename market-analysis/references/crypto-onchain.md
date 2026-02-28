# Crypto On-Chain Analysis Reference

## Table of Contents
1. [On-Chain Metrics Overview](#on-chain-metrics-overview)
2. [Market Cycle Indicators](#market-cycle-indicators)
3. [Network Health Metrics](#network-health-metrics)
4. [DeFi Metrics](#defi-metrics)
5. [Derivatives & Leverage](#derivatives--leverage)
6. [Crypto Market Cycles](#crypto-market-cycles)
7. [Data Sources](#data-sources)

---

## On-Chain Metrics Overview

On-chain data comes directly from blockchain transactions — it cannot be faked and provides unique insight unavailable in traditional markets.

### Primary Valuation Metrics

#### MVRV Ratio (Market Value to Realized Value)
```
MVRV = Market Cap / Realized Cap
```
- **Realized Cap**: Sum of all coins × price at time of last move (cost basis)
- **MVRV < 1**: Market below cost basis → historically strong buy zone
- **MVRV 1-2**: Fair value zone
- **MVRV 2-3.5**: Elevated, approaching distribution zone
- **MVRV > 3.5**: Historically signals market tops (BTC)

#### NVT Ratio (Network Value to Transactions)
```
NVT = Market Cap / Daily Transaction Volume (USD)
```
- Similar to P/E ratio for crypto
- **NVT < 65**: Undervalued (high network usage relative to price)
- **NVT 65-95**: Fair value
- **NVT > 95**: Overvalued (price exceeding network utility)
- Use **NVT Signal** (90-day MA of volume) for smoother reading

#### SOPR (Spent Output Profit Ratio)
```
SOPR = Price sold / Price paid
```
- **SOPR > 1**: Average seller in profit → selling pressure possible
- **SOPR < 1**: Average seller at loss → capitulation phase
- **SOPR = 1**: Market equilibrium
- **Bull market signal**: SOPR bounces above 1 on dips (holders refuse to sell at loss)
- **Bear market signal**: SOPR fails to sustain above 1

---

## Market Cycle Indicators

### NUPL (Net Unrealized Profit/Loss)
```
NUPL = (Unrealized Profit - Unrealized Loss) / Market Cap
```

| NUPL Range | Phase | Color | Action |
|-----------|-------|-------|--------|
| < 0 | Capitulation | Black | Strong accumulation |
| 0 - 0.25 | Hope/Fear | Orange | Accumulation |
| 0.25 - 0.5 | Optimism | Yellow | Hold |
| 0.5 - 0.75 | Belief/Anxiety | Green | Reduce, take profit |
| > 0.75 | Euphoria/Greed | Blue | Significant distribution |

### Bitcoin Halving Cycle Context
- Use `btc-halving-monitor` skill for detailed halving analysis
- General pattern: accumulation pre-halving → bull run 12-18 months post-halving → bear market

### Realized Price Levels (BTC)
Key psychological levels derived from on-chain cost basis:
- **Realized Price**: Average cost basis of all holders (~$30K range historically)
- **200-week MA**: Long-term bull/bear dividing line
- **Mayer Multiple**: Price / 200-day MA
  - < 0.8: Historically cheap
  - > 2.4: Historically expensive

### Coin Days Destroyed (CDD)
Measures economic activity weighted by coin age:
- **High CDD**: Long-dormant coins moving → distribution potential
- **Low CDD during rally**: New coins driving price → less distribution pressure
- **CDD spike at market highs**: Classic distribution signal

---

## Network Health Metrics

### Active Addresses
- **Rising active addresses + rising price**: Organic demand (bullish)
- **Falling active addresses + rising price**: Price-driven speculation (less sustainable)
- Compare 30-day MA vs 90-day MA for trend

### Hash Rate (Bitcoin)
- **Rising hash rate**: Miner confidence, network security improving
- **Hash ribbon buy signal**: Short-term MA crosses above long-term MA after recovery from miner capitulation
- See `btc-halving-monitor` skill for detailed hash rate analysis

### Exchange Balances
```
Exchange Net Flow = Inflows - Outflows
```
- **Net inflow to exchanges**: Selling pressure likely (coins moving to sell)
- **Net outflow from exchanges**: Accumulation likely (coins moving to cold storage)
- **Declining exchange balance trend**: Structurally bullish (supply squeeze)

### Stablecoin Supply Ratio (SSR)
```
SSR = BTC Market Cap / Stablecoin Market Cap
```
- **Low SSR**: High stablecoin dry powder relative to BTC → potential buying power
- **High SSR**: Low dry powder → limited fuel for price rises

---

## DeFi Metrics

### Total Value Locked (TVL)
- **TVL rising**: Capital flowing into DeFi ecosystem (positive)
- **TVL falling**: Capital exiting, risk-off sentiment
- Compare TVL to protocol market cap: low TVL/FDV = overvalued protocol

### Key DeFi Metrics by Protocol Type

#### DEXes (Uniswap, Curve, etc.)
| Metric | Good Signal |
|--------|------------|
| Volume / TVL | >0.1 daily (capital efficiency) |
| Revenue (fees) | Sustainable fee generation |
| Unique users growth | Expanding user base |

#### Lending Protocols (Aave, Compound)
| Metric | Good Signal |
|--------|------------|
| Utilization Rate | 40-80% (too low = inefficient, too high = liquidity risk) |
| Borrow APY vs Supply APY spread | Healthy margin |
| Collateral health factor distribution | Most positions healthy |

#### Yield / Liquid Staking (Lido, Rocket Pool)
| Metric | Good Signal |
|--------|------------|
| Staking yield vs alternatives | Competitive |
| Validator count / decentralization | Growing, distributed |
| Liquid staking token peg | Near 1:1 to underlying |

### DeFi Red Flags
- Sudden TVL drop >30% in 24h
- Smart contract exploit (monitor Rekt.news)
- Stablecoin depeg >1%
- Protocol treasury concentrated (>50% in own token)

---

## Derivatives & Leverage

### Funding Rates (Perpetual Swaps)
```
Funding Rate = Periodic payment between longs and shorts
```
- **Positive funding**: Longs pay shorts → market leans long (speculative)
- **Negative funding**: Shorts pay longs → market leans short (potential squeeze)
- **Annualized > 50%**: Extreme leverage, high liquidation risk
- **Annualized 10-30%**: Moderate, sustainable bull market leverage

**Signal interpretation:**
- Strongly positive funding + price near high → contrarian short setup
- Negative funding + price stable/rising → shorts getting squeezed → bullish

### Open Interest (OI)
```
Rising OI + Rising Price = New money entering longs (bullish)
Rising OI + Falling Price = New money entering shorts (bearish)
Falling OI + Price Move = Deleveraging (forced liquidations)
```

### Liquidation Heatmap
- Large liquidation clusters above price → potential short squeeze targets
- Large liquidation clusters below price → potential long liquidation cascade levels
- Use Coinglass for liquidation data

### Long/Short Ratio
- **>60% longs**: Overleveraged long → potential flush down
- **>60% shorts**: Short squeeze setup → potential explosive move up
- Best signal when combined with funding rate direction

---

## Crypto Market Cycles

### Four Phases

```
1. ACCUMULATION (post-capitulation)
   Signs: Low MVRV (<1), negative funding, declining OI, fear sentiment
   Action: Gradual accumulation, averaging in

2. EXPANSION (early bull)
   Signs: MVRV 1-2, moderate funding, rising active addresses
   Action: Hold core, add on dips

3. EUPHORIA (late bull)
   Signs: MVRV >3, extreme positive funding, heavy retail inflow, media coverage
   Action: Systematic distribution, take profits

4. DISTRIBUTION / BEAR
   Signs: MVRV falling from high, large exchange inflows, capitulation events
   Action: Defensive, minimal exposure
```

### Altcoin Season Indicator
- **BTC Dominance falling + ETH rising**: ETH season beginning
- **ETH dominance rising + large-cap alts rising**: Broad crypto bull
- **Small-cap altcoins pumping**: Late cycle euphoria
- **BTC dominance rising during downturn**: Flight to safety

### Crypto-Specific Risk Events
| Event | Impact |
|-------|--------|
| Major exchange hack/collapse | Systemic sell-off |
| Regulatory crackdown | Jurisdiction-specific sell-off |
| Stablecoin depeg | Liquidity crisis |
| Bitcoin ETF approval/rejection | Large directional move |
| Macro risk-off (VIX spike) | Crypto sells off with equities |
| Halving | Supply shock, historically bullish 12-18 months after |

---

## Data Sources

| Data Type | Free Source | Premium Source |
|-----------|------------|----------------|
| On-chain metrics | Glassnode (limited), CryptoQuant free | Glassnode Pro |
| DeFi TVL | DeFiLlama (free) | - |
| Funding rates | Coinglass (free) | - |
| Liquidations | Coinglass (free) | - |
| Exchange flows | CryptoQuant free tier | CryptoQuant Pro |
| Price + OHLCV | CoinGecko, CoinMarketCap | - |
| Macro overlay | Same as traditional markets | - |

### Fetching Crypto Data
```bash
# Real-time price and market data
python scripts/fetch_crypto_realtime.py bitcoin --detailed

# Historical data
python scripts/fetch_crypto_data.py BTC-USD --period 180d

# Fear & Greed index (crypto-specific)
python scripts/sentiment_analysis.py fear-greed
```
