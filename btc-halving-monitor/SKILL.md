---
name: btc-halving-monitor
description: >
  BTC halving cycle monitor with on-chain analysis and investment signals.
  Tracks halving countdown (block height to estimated date), miner pressure
  (Hash Ribbon, difficulty adjustments, revenue), historical cycle comparison,
  and generates spot/contract investment advice with stop-loss levels.

  Use when:
  - User asks about BTC halving date, countdown, next halving, block reward
  - User asks about miner pressure, hash rate, Hash Ribbon, difficulty
  - User asks about BTC cycle position, historical comparison, halving patterns
  - User wants BTC investment advice based on halving cycle indicators
  - User mentions keywords: halving, hash rate, miner, block reward, cycle analysis
  - User asks in Chinese: 减半, 哈希率, 矿工, 区块奖励, 周期分析, BTC建议
---

# BTC Halving Cycle Monitor

On-chain analysis tool with 4 modules: halving countdown, miner pressure, historical cycle comparison, and investment signal engine.

## Quick Start

Run the full analysis:

```bash
python scripts/btc_monitor.py
```

Run individual modules:

```bash
python scripts/btc_monitor.py countdown   # Halving countdown only
python scripts/btc_monitor.py miner       # Miner pressure only
python scripts/btc_monitor.py cycle       # Historical comparison only
python scripts/btc_monitor.py signal      # Full analysis + investment advice
```

## Module Routing

Match user intent to the right module:

| User Intent | Module | Command |
|---|---|---|
| "BTC下次减半什么时候" / halving date | Countdown | `countdown` |
| "矿工压力/哈希率怎么样" / hash rate | Miner Pressure | `miner` |
| "现在处于周期什么位置" / cycle position | Cycle Analysis | `cycle` |
| "该买吗/合约建议" / investment advice | Signal Engine | `signal` or `full` |
| General BTC halving analysis | Full Report | `full` (default) |

## Interpreting Results

### Hash Ribbon Signals
- **BUY SIGNAL (crossover up)**: 30d MA crossed above 60d MA  - miner capitulation ended, historically strong long-term entry
- **SELL WARNING (crossover down)**: 30d MA crossed below 60d MA  - miners shutting down, caution

### Composite Score Range
Score ranges from -7 to +6.5. Interpretation:

| Score | Outlook | Spot Action | Contract Action |
|---|---|---|---|
| 3.5+ | Strongly Bullish | Aggressive accumulation | Long 5-8x |
| 1.5 to 3.5 | Bullish | Steady DCA | Long 3-5x |
| 0 to 1.5 | Neutral-Bullish | Light DCA | Small long 2-3x or avoid |
| -1.5 to 0 | Neutral-Bearish | Hold only | Avoid contracts |
| < -1.5 | Bearish | Reduce exposure | Short 3-5x |

### Key Caveats to Communicate to User
1. This is on-chain data analysis, NOT financial advice
2. Past halving cycles have diminishing returns  - never extrapolate directly
3. Hash rate drops can be caused by non-economic factors (regulation, natural disasters)
4. Always pair with macro context (interest rates, liquidity, regulatory environment)

## Data Sources

All APIs are free, no authentication required:
- **mempool.space**: Block height, hash rate, difficulty adjustments
- **CoinGecko**: BTC/USD price

For deeper historical context, read [references/halving_history.md](references/halving_history.md) which contains cycle phase maps, risk tiers, and miner economics breakdown.
