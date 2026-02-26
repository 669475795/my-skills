# Visualization Guide

## Available Libraries

### Matplotlib
- Standard Python plotting
- Static images (PNG)
- Full control over appearance
- **Install**: `pip install matplotlib`

### Mplfinance
- Specialized for financial charts
- Professional candlestick charts
- Built-in technical indicators
- **Install**: `pip install mplfinance`

### Plotly
- Interactive HTML charts
- Zoom, pan, hover tooltips
- Web-friendly
- **Install**: `pip install plotly kaleido`

## Chart Types

### Candlestick Charts
Shows OHLC (Open, High, Low, Close) for each period.

```bash
python chart_generator.py AAPL --period 3mo --indicators sma,volume
```

**Components:**
- Body: Open to Close
- Wicks: High and Low
- Green/White: Close > Open (bullish)
- Red/Black: Close < Open (bearish)

### Line Charts
Simple price over time.

```bash
python chart_generator.py AAPL --indicators none
```

### Comparison Charts
Multiple assets normalized to same starting point.

```bash
python chart_generator.py --compare --tickers "AAPL,MSFT,GOOGL" --period 1y
```

### Heatmaps
Correlation visualization.

```bash
python chart_generator.py --heatmap --tickers "AAPL,MSFT,GOOGL,AMZN,META"
```

## Technical Indicators

### Available Indicators
| Indicator | Code | Description |
|-----------|------|-------------|
| SMA | `sma` | Simple Moving Average (20, 50 day) |
| EMA | `ema` | Exponential Moving Average (12, 26 day) |
| Bollinger Bands | `bb` | 20-day SMA ± 2 standard deviations |
| Volume | `volume` | Volume bars below price |

### Example Usage
```bash
# All indicators
python chart_generator.py AAPL --indicators sma,ema,bb,volume

# Just moving averages
python chart_generator.py AAPL --indicators sma,ema

# Price and volume only
python chart_generator.py AAPL --indicators volume
```

## Portfolio Charts

### Allocation Pie Chart
```bash
python portfolio_charts.py allocation --holdings '{"AAPL": 30, "MSFT": 25, "GOOGL": 20, "AMZN": 15, "Cash": 10}'
```

### Equity Curve
```bash
python portfolio_charts.py equity --tickers "AAPL,MSFT,GOOGL" --weights "0.4,0.3,0.3" --period 1y
```

### Risk-Return Scatter
```bash
python portfolio_charts.py risk-return --tickers "AAPL,MSFT,GOOGL,AMZN,TSLA"
```

### Rolling Metrics
```bash
python portfolio_charts.py rolling --tickers "SPY,TLT" --weights "0.6,0.4" --window 60
```

## Output Formats

### PNG (Static)
- Default format
- Good for reports
- Email-friendly

```bash
python chart_generator.py AAPL --format png
```

### HTML (Interactive)
- Requires Plotly
- Zoom, pan, hover
- Web embedding

```bash
python chart_generator.py AAPL --format html
```

## Customization

### Output Directory
```bash
python chart_generator.py AAPL --output-dir ./my_charts
```

### Chart Features
The generated charts include:
- Title with ticker symbol
- Y-axis price labels
- X-axis date labels
- Legend for indicators
- Grid lines
- Volume panel (if enabled)

## Best Practices

### Chart Selection
| Purpose | Recommended Chart |
|---------|-------------------|
| Price analysis | Candlestick |
| Trend analysis | Line with MAs |
| Comparison | Normalized line |
| Correlation | Heatmap |
| Allocation | Pie chart |
| Performance | Equity curve |

### Time Periods
| Analysis Type | Recommended Period |
|--------------|-------------------|
| Day trading | 1d-5d, 1-5 minute |
| Swing trading | 1mo-3mo, daily |
| Position trading | 6mo-1y, daily |
| Investing | 1y-5y, weekly |

### Indicator Combinations
| Style | Indicators |
|-------|------------|
| Trend following | SMA 50, 200 |
| Mean reversion | Bollinger Bands |
| Momentum | EMA 12, 26 + MACD |
| Volume analysis | Price + Volume |

## Troubleshooting

### Library Not Available
```
Error: matplotlib not available
```
**Solution**: `pip install matplotlib`

### No Data
```
Error: No data available for TICKER
```
**Solution**: Check ticker symbol format

### Export Issues
For HTML export with Plotly:
```bash
pip install plotly kaleido
```

## CLI Reference

### chart_generator.py
```bash
python chart_generator.py <ticker> [options]

Options:
  --period       Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y)
  --indicators   Comma-separated indicators (sma,ema,bb,volume)
  --format       Output format (png, html)
  --output-dir   Output directory
  --compare      Generate comparison chart
  --heatmap      Generate correlation heatmap
  --tickers      Multiple tickers for comparison
```

### portfolio_charts.py
```bash
python portfolio_charts.py <action> [options]

Actions:
  allocation    Pie chart of holdings
  equity        Equity curve with benchmark
  risk-return   Risk-return scatter plot
  rolling       Rolling metrics chart

Options:
  --tickers     Comma-separated tickers
  --weights     Comma-separated weights
  --holdings    JSON holdings dictionary
  --period      Data period
  --benchmark   Benchmark ticker (default: SPY)
```
