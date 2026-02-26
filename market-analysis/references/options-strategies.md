# Options Strategies Guide

## Fundamentals

### Option Pricing Factors
1. **Underlying Price (S)**: Current stock price
2. **Strike Price (K)**: Exercise price
3. **Time to Expiration (T)**: Time value decay
4. **Volatility (σ)**: Expected price movement
5. **Interest Rate (r)**: Risk-free rate
6. **Dividends**: Reduces call value, increases put value

### The Greeks

| Greek | Measures | Range | Interpretation |
|-------|----------|-------|----------------|
| Delta | Price sensitivity | 0 to ±1 | $1 stock move → $delta option move |
| Gamma | Delta sensitivity | 0+ | Higher near ATM |
| Theta | Time decay | Negative | Daily option value loss |
| Vega | Volatility sensitivity | 0+ | 1% IV change → $vega option change |
| Rho | Interest rate sensitivity | Varies | Usually small impact |

## Strategy Selection Guide

### Bullish Strategies
| Strategy | Max Profit | Max Loss | Break-even |
|----------|-----------|----------|------------|
| Long Call | Unlimited | Premium | Strike + Premium |
| Bull Call Spread | Width - Debit | Debit | Lower + Debit |
| Cash-Secured Put | Premium | Strike - Premium | Strike - Premium |

### Bearish Strategies
| Strategy | Max Profit | Max Loss | Break-even |
|----------|-----------|----------|------------|
| Long Put | Strike - Premium | Premium | Strike - Premium |
| Bear Put Spread | Width - Debit | Debit | Higher - Debit |
| Covered Call | Premium + (Strike - Stock) | Stock - Premium | Stock - Premium |

### Neutral Strategies
| Strategy | Best When | Max Profit | Max Loss |
|----------|-----------|-----------|----------|
| Iron Condor | Low volatility | Credit | Width - Credit |
| Iron Butterfly | Pin to strike | Credit | Width - Credit |
| Calendar Spread | Time decay | Variable | Debit |

### Volatile Strategies
| Strategy | Best When | Max Profit | Max Loss |
|----------|-----------|-----------|----------|
| Long Straddle | Big move expected | Unlimited | Premium |
| Long Strangle | Cheaper than straddle | Unlimited | Premium |
| Backspread | Directional + Vol | Unlimited | Width - Credit |

## Strategy Details

### Covered Call
```
Setup: Long 100 shares + Short 1 OTM call
Sentiment: Neutral to slightly bullish
Use when: Willing to sell at strike, want income
Risk: Stock decline not protected

Example:
- Own 100 AAPL at $150
- Sell 1 $160 call for $3
- Max profit: $13 ($10 gain + $3 premium)
- Breakeven: $147 ($150 - $3)
```

### Iron Condor
```
Setup:
- Buy 1 OTM put (protection)
- Sell 1 put closer to money
- Sell 1 call closer to money
- Buy 1 OTM call (protection)

Sentiment: Neutral, expecting range-bound
Use when: IV is high, expect consolidation
Risk: Limited to width - credit

Example (Stock at $100):
- Buy $85 put
- Sell $90 put
- Sell $110 call
- Buy $115 call
Total credit: $2.00
Max profit: $2.00
Max loss: $3.00 ($5 width - $2 credit)
```

### Bull Call Spread
```
Setup: Long lower strike call + Short higher strike call
Sentiment: Moderately bullish
Use when: Want defined risk, capped upside OK

Example:
- Buy $100 call for $5
- Sell $110 call for $2
- Net debit: $3
- Max profit: $7 ($10 - $3)
- Max loss: $3 (debit)
- Breakeven: $103
```

## Implied Volatility Analysis

### IV Percentile
- **0-20%**: Low IV - Consider buying strategies
- **20-50%**: Normal IV - Strategy dependent
- **50-80%**: Elevated IV - Consider selling strategies
- **80-100%**: High IV - Premium selling attractive

### IV Crush
After earnings/events, IV typically drops sharply.
- Avoid buying options before events
- Selling premium can capture IV crush

## CLI Usage

```bash
# Black-Scholes pricing
python options_analysis.py price --spot 100 --strike 105 --time 0.25 --vol 0.20 --type call

# Calculate IV
python options_analysis.py iv --spot 100 --strike 105 --time 0.25 --market-price 3.50

# Strategy templates
python options_analysis.py templates

# Greeks calculation
python options_analysis.py greeks --spot 100 --strike 100 --time 0.1 --vol 0.25
```

## Risk Management

### Position Sizing
- Risk no more than 2-5% per trade
- Account for worst-case (max loss)
- Diversify across expirations

### Adjustment Rules
1. **Roll**: Move to different strike/expiration
2. **Close partial**: Take profits on winning legs
3. **Add protection**: Buy hedging options
4. **Close entirely**: Accept loss, preserve capital

### Exit Guidelines
- Set profit target (50-75% of max profit)
- Have stop-loss level
- Don't hold through expiration unnecessarily
- Close before earnings if unplanned
