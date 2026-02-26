# Technical Indicators Reference

## Moving Averages

### Simple Moving Average (SMA)

**Calculation**: Average of closing prices over N periods

```
SMA = (Price₁ + Price₂ + ... + Priceₙ) / N
```

**Common Periods**:
- SMA(20): Short-term trend
- SMA(50): Medium-term trend
- SMA(200): Long-term trend

**Interpretation**:
- **Bullish**: Price above SMA, SMA trending up
- **Bearish**: Price below SMA, SMA trending down
- **Golden Cross**: SMA(50) crosses above SMA(200) - Strong buy signal
- **Death Cross**: SMA(50) crosses below SMA(200) - Strong sell signal

**Use Case**: Identify trend direction and support/resistance levels

---

### Exponential Moving Average (EMA)

**Calculation**: Weighted average giving more weight to recent prices

```
EMA = (Price × Multiplier) + (EMA_previous × (1 - Multiplier))
Multiplier = 2 / (Period + 1)
```

**Common Periods**:
- EMA(12), EMA(26): Used in MACD calculation
- EMA(20): Short-term trend, more responsive than SMA(20)

**Interpretation**:
- Reacts faster to price changes than SMA
- Better for volatile markets
- Use same signals as SMA

---

## Momentum Indicators

### Relative Strength Index (RSI)

**Calculation**:

```
RSI = 100 - (100 / (1 + RS))
RS = Average Gain / Average Loss (over 14 periods)
```

**Range**: 0 to 100

**Interpretation**:
- **RSI > 70**: Overbought - Potential sell signal
- **RSI < 30**: Oversold - Potential buy signal
- **RSI 40-60**: Neutral zone
- **Divergence**: Price makes new high but RSI doesn't - Bearish
- **Divergence**: Price makes new low but RSI doesn't - Bullish

**Best Practices**:
- Don't trade solely on RSI
- Works better in ranging markets
- In strong trends, RSI can stay overbought/oversold for extended periods

---

### MACD (Moving Average Convergence Divergence)

**Calculation**:

```
MACD Line = EMA(12) - EMA(26)
Signal Line = EMA(9) of MACD Line
Histogram = MACD Line - Signal Line
```

**Interpretation**:
- **MACD > Signal**: Bullish momentum
- **MACD < Signal**: Bearish momentum
- **Histogram > 0**: Increasing bullish momentum
- **Histogram < 0**: Increasing bearish momentum
- **Zero Line Cross**: MACD crosses above/below zero - Trend change

**Signals**:
1. **Bullish Crossover**: MACD crosses above signal line - Buy
2. **Bearish Crossover**: MACD crosses below signal line - Sell
3. **Divergence**: Price vs MACD divergence suggests trend reversal

**Best For**: Identifying trend changes and momentum shifts

---

## Volatility Indicators

### Bollinger Bands

**Calculation**:

```
Middle Band = SMA(20)
Upper Band = SMA(20) + (2 × Standard Deviation)
Lower Band = SMA(20) - (2 × Standard Deviation)
```

**Parameters**:
- Period: 20 (default)
- Standard Deviations: 2 (default)

**Interpretation**:
- **Price near Upper Band**: Overbought conditions
- **Price near Lower Band**: Oversold conditions
- **Band Squeeze**: Low volatility - Potential breakout coming
- **Band Expansion**: High volatility - Strong trend
- **Walking the Bands**: Price consistently touching upper/lower band - Strong trend

**Trading Strategies**:
1. **Mean Reversion**: Buy at lower band, sell at upper band (ranging market)
2. **Breakout**: Buy when price breaks above upper band with volume (trending market)
3. **Bollinger Squeeze**: Trade breakout direction after squeeze

---

### Average True Range (ATR)

**Calculation**:

```
True Range = max(High - Low, |High - Close_prev|, |Low - Close_prev|)
ATR = SMA of True Range over 14 periods
```

**Interpretation**:
- Measures volatility, not direction
- High ATR: High volatility
- Low ATR: Low volatility
- Used for stop-loss placement: Stop = Entry ± (2 × ATR)

---

## Volume Indicators

### Volume Analysis

**Key Metrics**:
- **Current Volume vs Average**: Confirms price moves
- **Volume Trend**: Increasing volume confirms trend
- **Volume Spike**: Potential trend change or continuation

**Interpretation**:
- **High Volume + Price Up**: Strong buying pressure - Bullish
- **High Volume + Price Down**: Strong selling pressure - Bearish
- **Low Volume**: Weak trend, potential reversal
- **Volume Divergence**: Price up but volume down - Bearish

**Volume Patterns**:
1. **Accumulation**: Increasing volume on up days - Bullish
2. **Distribution**: Increasing volume on down days - Bearish
3. **Climax**: Extremely high volume - Potential reversal

---

## Trend Indicators

### ADX (Average Directional Index)

**Range**: 0 to 100

**Interpretation**:
- **ADX < 20**: Weak trend, ranging market
- **ADX 20-40**: Moderate trend
- **ADX > 40**: Strong trend
- **ADX > 50**: Very strong trend

**Note**: ADX shows trend strength, not direction. Use with +DI/-DI for direction.

---

### Parabolic SAR

**Interpretation**:
- Dots below price: Uptrend - Hold long positions
- Dots above price: Downtrend - Hold short positions
- Dot flip: Potential trend reversal

**Best For**: Trending markets, setting trailing stops

---

## Support and Resistance

### Fibonacci Retracement

**Levels**: 23.6%, 38.2%, 50%, 61.8%, 78.6%

**Usage**:
1. Identify significant high and low
2. Draw Fibonacci levels
3. Look for price reactions at these levels

**Key Level**: 61.8% (Golden Ratio) - Strong support/resistance

---

### Pivot Points

**Calculation**:

```
Pivot Point (P) = (High + Low + Close) / 3
Resistance 1 (R1) = (2 × P) - Low
Support 1 (S1) = (2 × P) - High
Resistance 2 (R2) = P + (High - Low)
Support 2 (S2) = P - (High - Low)
```

**Usage**: Intraday support and resistance levels

---

## Combining Indicators

### Best Combinations

1. **Trend + Momentum**
   - SMA(50/200) + RSI
   - Confirms trend and entry timing

2. **Trend + Volatility**
   - EMA + Bollinger Bands
   - Identifies trend and trading range

3. **Momentum + Volume**
   - MACD + Volume Analysis
   - Confirms momentum with conviction

4. **Multiple Timeframes**
   - Daily SMA(200) for trend
   - 4-hour MACD for entries
   - 1-hour RSI for timing

### Indicator Conflicts

When indicators disagree:
- **RSI oversold but MACD bearish**: Wait for MACD to turn
- **Price above SMA but declining MACD**: Potential trend weakening
- **Solution**: Use higher timeframe as tie-breaker

---

## Common Mistakes

1. **Using Too Many Indicators**: Leads to analysis paralysis
2. **Ignoring Price Action**: Indicators lag price
3. **Not Adjusting Parameters**: Default settings don't fit all assets
4. **Trading Against Trend**: RSI oversold in downtrend can go lower
5. **Ignoring Context**: Market conditions affect indicator reliability

---

## Indicator Selection by Market Type

### Trending Market
- Best: MACD, EMA, ADX
- Avoid: Mean reversion strategies

### Ranging Market
- Best: RSI, Bollinger Bands, Stochastic
- Avoid: Trend-following indicators

### Volatile Market
- Best: ATR, Bollinger Bands
- Use wider stops, larger profit targets

### Low Volatility
- Best: Breakout indicators (Bollinger Squeeze)
- Wait for volatility expansion

---

## Quick Reference Table

| Indicator | Type | Best For | Timeframe |
|-----------|------|----------|-----------|
| SMA(200) | Trend | Long-term direction | Daily+ |
| EMA(20) | Trend | Short-term entries | Hourly+ |
| RSI(14) | Momentum | Overbought/oversold | Any |
| MACD | Momentum | Trend changes | Daily |
| Bollinger Bands | Volatility | Range/breakout | Daily |
| Volume | Confirmation | Validating moves | Any |
| ADX | Trend Strength | Trend quality | Daily |
| Fibonacci | Support/Resistance | Retracement targets | Any |

---

## Resources for Further Learning

1. **Technical Analysis of Financial Markets** by John Murphy
2. **Trading for a Living** by Alexander Elder
3. **TradingView**: Free charting platform with all indicators
4. **Investopedia**: Detailed indicator explanations
