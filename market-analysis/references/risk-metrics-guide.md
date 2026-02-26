# Risk Metrics Guide

## Position Sizing

### Fixed Percentage Method
Risk a fixed percentage of capital per trade.

```
Position Size = (Account × Risk%) / (Entry - Stop Loss)
```

**Example:**
- Account: $100,000
- Risk per trade: 2% ($2,000)
- Entry: $50
- Stop loss: $45
- Position size: $2,000 / $5 = 400 shares

### Kelly Criterion
Optimal position size based on edge:

```
Kelly % = (Win Rate × Win/Loss Ratio - (1 - Win Rate)) / Win/Loss Ratio
```

**Example:**
- Win rate: 55%
- Win/loss ratio: 2:1
- Kelly: (0.55 × 2 - 0.45) / 2 = 32.5%

**Recommendation**: Use Half-Kelly (16.25%) for safety

## Value at Risk (VaR)

### Definition
Maximum expected loss at a given confidence level over a specific time period.

### Calculation Methods

#### 1. Historical VaR
Use actual historical returns to estimate percentile.
```
VaR (95%) = 5th percentile of historical returns
```

#### 2. Parametric VaR
Assume normal distribution:
```
VaR = μ - Z × σ
```
Where Z = 1.65 (95%) or 2.33 (99%)

#### 3. Monte Carlo VaR
Simulate thousands of scenarios, find percentile.

### VaR Interpretation
- **VaR (95%, 1-day) = 2%**:
  - 95% confident won't lose more than 2% in one day
  - 5% chance of larger loss
  - Expect to breach ~13 times per year

### VaR Limitations
- Assumes normal markets
- Doesn't measure tail risk
- Backward-looking

## Conditional VaR (CVaR / Expected Shortfall)

### Definition
Average loss when VaR is exceeded.

```
CVaR = E[Loss | Loss > VaR]
```

### Why Better Than VaR
- Measures tail risk
- Coherent risk measure
- More conservative

## Risk-Adjusted Return Metrics

### Sharpe Ratio
Return per unit of total risk:

```
Sharpe = (Return - Risk-free Rate) / Standard Deviation
```

| Sharpe | Interpretation |
|--------|----------------|
| < 0 | Negative excess return |
| 0-1 | Suboptimal |
| 1-2 | Good |
| 2-3 | Very good |
| > 3 | Excellent (verify data) |

### Sortino Ratio
Return per unit of downside risk:

```
Sortino = (Return - Risk-free Rate) / Downside Deviation
```

Better than Sharpe when returns are asymmetric.

### Calmar Ratio
Return relative to maximum drawdown:

```
Calmar = Annual Return / Maximum Drawdown
```

| Calmar | Interpretation |
|--------|----------------|
| < 0.5 | Poor |
| 0.5-1.0 | Acceptable |
| 1.0-2.0 | Good |
| > 2.0 | Excellent |

### Information Ratio
Excess return per unit of tracking error:

```
IR = (Portfolio Return - Benchmark Return) / Tracking Error
```

## Maximum Drawdown

### Definition
Largest peak-to-trough decline in portfolio value.

```
Drawdown = (Peak - Trough) / Peak
```

### Drawdown Recovery
| Drawdown | Gain Needed to Recover |
|----------|------------------------|
| 10% | 11.1% |
| 20% | 25% |
| 30% | 42.9% |
| 50% | 100% |
| 75% | 300% |

### Drawdown Analysis
- **Average Drawdown**: Typical decline
- **Max Drawdown**: Worst case
- **Drawdown Duration**: Time in drawdown
- **Recovery Time**: Time to new high

## Portfolio Risk

### Correlation
Measure of how assets move together:
- +1: Perfect positive correlation
- 0: No correlation
- -1: Perfect negative correlation

### Diversification Benefit
Lower correlation = Better diversification

```
Portfolio Vol < Weighted Average of Individual Vols (when corr < 1)
```

### Beta
Sensitivity to market movements:

```
Beta = Covariance(Asset, Market) / Variance(Market)
```

| Beta | Interpretation |
|------|----------------|
| > 1 | More volatile than market |
| 1 | Moves with market |
| < 1 | Less volatile than market |
| < 0 | Inverse relationship |

## Stress Testing

### Historical Scenarios
Test portfolio against past events:
- 2008 Financial Crisis
- 2020 COVID Crash
- 2022 Rate Shock

### Hypothetical Scenarios
- Market crash (-40%)
- Interest rate spike (+200bp)
- Volatility spike (VIX to 80)

### Stress Test Interpretation
Ensure portfolio can survive worst-case scenarios while meeting investment goals.

## CLI Usage

```bash
# Position sizing
python risk_management.py position --account 100000 --risk 0.02 --entry 50 --stop 45

# VaR calculation
python risk_management.py var --ticker AAPL --confidence 0.95

# Portfolio VaR
python risk_management.py var --tickers "AAPL,MSFT,GOOGL" --weights "0.4,0.3,0.3" --value 100000

# Risk metrics
python risk_management.py metrics --ticker SPY --period 2y

# Stress test
python risk_management.py stress --value 100000

# Kelly criterion
python risk_management.py kelly --win-rate 0.55 --win-loss-ratio 2.0
```

## Risk Management Rules

### Position Limits
- Max single position: 10% of portfolio
- Max sector exposure: 25%
- Max correlated positions: 30%

### Stop Loss Guidelines
- Technical: Below support level
- Percentage: 5-10% typical
- ATR-based: 2-3 × ATR

### Portfolio Limits
- Max leverage: Define based on risk tolerance
- Max drawdown trigger: Stop trading at threshold
- Daily loss limit: 2-3% of portfolio
