# Market Data APIs and Sources

## Primary Data Source: Yahoo Finance (yfinance)

**Library**: `yfinance` (Python)
**License**: Apache 2.0
**Data**: Free, delayed ~15 minutes
**Coverage**: Global stocks, cryptocurrencies, forex, commodities

### Installation

```bash
pip install yfinance pandas numpy
```

### Supported Markets

1. **US Stocks**: NYSE, NASDAQ, AMEX
   - Format: `AAPL`, `TSLA`, `MSFT`
   - No suffix needed

2. **Hong Kong Stocks**: HKEX
   - Format: `00700.HK`, `09988.HK`
   - Add `.HK` suffix

3. **China A-Shares**
   - Shanghai: `600519.SS` (add `.SS` suffix)
   - Shenzhen: `000001.SZ` (add `.SZ` suffix)

4. **Cryptocurrencies**
   - Format: `BTC-USD`, `ETH-USD`
   - Always use `-USD` suffix

### Data Available

- **Historical prices**: OHLCV (Open, High, Low, Close, Volume)
- **Current quotes**: Real-time (delayed 15 min)
- **Fundamentals**: P/E, P/B, market cap, earnings, dividends
- **Corporate actions**: Splits, dividends
- **Options data**: Available for US stocks
- **Analyst ratings**: Consensus recommendations

### Rate Limits

- No official rate limit
- Recommended: Max 2000 requests/hour
- Add delays between bulk requests: `time.sleep(0.5)`

### Example Usage

```python
import yfinance as yf

# Single stock
ticker = yf.Ticker("AAPL")
hist = ticker.history(period="1mo")
info = ticker.info

# Multiple stocks
data = yf.download("AAPL MSFT GOOGL", period="1mo")

# Cryptocurrency
btc = yf.Ticker("BTC-USD")
btc_hist = btc.history(period="1y")
```

## Alternative Data Sources

### 1. Alpha Vantage

**Website**: https://www.alphavantage.co
**API Key**: Required (free tier available)
**Free Tier**: 5 requests/minute, 500 requests/day
**Coverage**: Global stocks, forex, crypto, technical indicators

**Pros**:
- Official API with documentation
- More reliable than scraping
- Includes pre-calculated technical indicators

**Cons**:
- Strict rate limits
- Requires API key registration

```python
# Example
import requests

API_KEY = "YOUR_API_KEY"
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey={API_KEY}"
response = requests.get(url)
data = response.json()
```

### 2. CoinGecko (Crypto)

**Website**: https://www.coingecko.com/api
**API Key**: Not required for free tier
**Free Tier**: 10-50 calls/minute
**Coverage**: 10,000+ cryptocurrencies

**Pros**:
- No API key needed
- Comprehensive crypto data
- Market sentiment metrics

**Cons**:
- Crypto only
- Rate limited

```python
import requests

url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": "bitcoin,ethereum",
    "vs_currencies": "usd",
    "include_24hr_change": "true"
}
response = requests.get(url, params=params)
```

### 3. Twelve Data

**Website**: https://twelvedata.com
**API Key**: Required
**Free Tier**: 800 requests/day
**Coverage**: Stocks, forex, crypto, ETFs

**Pros**:
- Real-time data available
- WebSocket support
- Good documentation

**Cons**:
- Requires registration
- Limited free tier

## Data Quality Notes

### Yahoo Finance Quirks

1. **Delayed Data**: 15-minute delay during market hours
2. **Missing Data**: Some international stocks have gaps
3. **Adjusted Prices**: Default returns split-adjusted prices
4. **Weekend Data**: No data for weekends/holidays
5. **Pre/Post Market**: Limited pre-market and after-hours data

### Handling Missing Data

```python
import pandas as pd

# Forward fill missing values
df.fillna(method='ffill', inplace=True)

# Drop rows with missing data
df.dropna(inplace=True)

# Interpolate
df.interpolate(method='linear', inplace=True)
```

## Best Practices

1. **Cache Data**: Save fetched data to avoid redundant API calls
2. **Error Handling**: Always check for empty DataFrames
3. **Retry Logic**: Implement exponential backoff for failed requests
4. **Respect Rate Limits**: Add delays between requests
5. **Data Validation**: Verify data integrity before analysis
6. **Time Zones**: Be aware of market time zones (EST for US, HKT for HK)

## Market Hours

| Market | Trading Hours (Local Time) | UTC Offset |
|--------|----------------------------|------------|
| NYSE/NASDAQ | 9:30 AM - 4:00 PM EST | UTC-5/-4 |
| HKEX | 9:30 AM - 4:00 PM HKT | UTC+8 |
| SSE/SZSE | 9:30 AM - 3:00 PM CST | UTC+8 |
| Crypto | 24/7 | N/A |

## Error Codes and Troubleshooting

### Common Errors

1. **Empty DataFrame**
   - Cause: Invalid ticker or no data for period
   - Solution: Verify ticker format, check market hours

2. **Connection Errors**
   - Cause: Network issues or Yahoo Finance downtime
   - Solution: Implement retry logic with exponential backoff

3. **Key Errors in `info`**
   - Cause: Metric not available for this stock
   - Solution: Use `.get()` with default values

4. **Rate Limiting (429)**
   - Cause: Too many requests
   - Solution: Add delays, implement caching

### Debug Tips

```python
# Check if data is available
if hist.empty:
    print("No data available")

# Verify ticker exists
try:
    info = ticker.info
    if not info:
        print("Invalid ticker")
except:
    print("Failed to fetch data")

# Check data freshness
last_update = hist.index[-1]
print(f"Last data point: {last_update}")
```

## Legal and Compliance

- **Terms of Service**: Review Yahoo Finance ToS before commercial use
- **Data Usage**: Free for personal use, commercial use may require license
- **Redistribution**: Do not redistribute raw data feeds
- **Attribution**: Credit data source when publishing analysis
- **Disclaimer**: Always include investment disclaimer in public analysis

---

## Chinese Market Data Sources

### 1. EastMoney (东方财富)

**Website**: https://www.eastmoney.com
**API Key**: Not required
**Coverage**: A-shares, HK stocks, funds, IPO data

**Capabilities**:
- Real-time quotes (slight delay)
- IPO calendar and subscription data
- Fund flow analysis (北向资金)
- Financial reports
- News and announcements

**Endpoints**:
```python
# Stock quote
quote_url = "http://push2.eastmoney.com/api/qt/stock/get"

# IPO calendar
ipo_url = "http://data.eastmoney.com/xg/xg/default.html"

# Fund flow
flow_url = "http://push2.eastmoney.com/api/qt/stock/fflow/kline/get"
```

**Rate Limits**: ~100 requests/minute recommended

### 2. Sina Finance (新浪财经)

**Website**: https://finance.sina.com.cn
**API Key**: Not required
**Coverage**: A-shares, HK stocks, US stocks, forex, crypto

**Capabilities**:
- Real-time quotes
- Historical data
- Options data
- News feed

**Quote API**:
```python
# Real-time quote
url = "http://hq.sinajs.cn/list=sh600519,sz000001"

# Hong Kong
url = "http://hq.sinajs.cn/list=hk00700"

# US stocks
url = "http://hq.sinajs.cn/list=gb_aapl"
```

**Rate Limits**: ~60 requests/minute

### 3. CNInfo (巨潮资讯)

**Website**: http://www.cninfo.com.cn
**API Key**: Not required
**Coverage**: A-share announcements, prospectuses, financial reports

**Capabilities**:
- Official announcements
- IPO prospectuses
- Annual/quarterly reports
- Board resolutions

**Use Cases**:
- IPO due diligence
- Regulatory filings
- Corporate actions

---

## Macroeconomic Data Sources

### FRED (Federal Reserve Economic Data)

**Website**: https://fred.stlouisfed.org
**API Key**: Required (free)
**Coverage**: US economic indicators

**Key Series**:
| Series ID | Description |
|-----------|-------------|
| FEDFUNDS | Federal Funds Rate |
| CPIAUCSL | Consumer Price Index |
| UNRATE | Unemployment Rate |
| GDP | Gross Domestic Product |
| DGS10 | 10-Year Treasury Yield |
| DGS2 | 2-Year Treasury Yield |

**Python Usage**:
```python
from fredapi import Fred
fred = Fred(api_key='YOUR_API_KEY')
data = fred.get_series('FEDFUNDS')
```

**Rate Limits**: 120 requests/minute

### China Macro Data

**EastMoney Macro**:
- GDP, CPI, PMI
- PBoC rates
- Money supply (M1, M2)

**NBS (National Bureau of Statistics)**:
- Official government data
- Monthly economic indicators

---

## Options Data Sources

### Yahoo Finance Options

**Coverage**: US stocks options only
**Data Available**:
- Option chains by expiration
- Strikes, bids, asks
- Open interest, volume
- Implied volatility

**Python Usage**:
```python
import yfinance as yf
ticker = yf.Ticker("AAPL")
options = ticker.options  # List of expiration dates
chain = ticker.option_chain("2024-01-19")
calls = chain.calls
puts = chain.puts
```

### CBOE (Chicago Board Options Exchange)

**Website**: https://www.cboe.com
**Coverage**: VIX, major indices
**Use**: VIX data, options volume

---

## Bond Data Sources

### Treasury Direct

**Website**: https://www.treasurydirect.gov
**Coverage**: US Treasury securities

### FRED Bond Data

| Series | Description |
|--------|-------------|
| DGS1 | 1-Year Treasury |
| DGS2 | 2-Year Treasury |
| DGS5 | 5-Year Treasury |
| DGS10 | 10-Year Treasury |
| DGS30 | 30-Year Treasury |
| BAMLC0A0CM | Investment Grade Spread |
| BAMLH0A0HYM2 | High Yield Spread |

---

## Precious Metals Data

### Yahoo Finance Commodities

| Symbol | Description |
|--------|-------------|
| GC=F | Gold Futures |
| SI=F | Silver Futures |
| PL=F | Platinum Futures |
| PA=F | Palladium Futures |

### ETF Proxies

| Symbol | Description |
|--------|-------------|
| GLD | SPDR Gold Trust |
| SLV | iShares Silver Trust |
| IAU | iShares Gold Trust |
| PPLT | Physical Platinum Shares |

### Shanghai Gold Exchange (via EastMoney)

**Coverage**: Au99.99, Au(T+D), Silver
**Use**: Chinese gold prices

---

## IPO Data Sources

### US IPO

**SEC EDGAR**: https://www.sec.gov/edgar
- S-1 filings
- Prospectuses
- Registration statements

**NASDAQ IPO Calendar**: https://www.nasdaq.com/market-activity/ipos

### Hong Kong IPO

**HKEX Disclosure**: https://www.hkexnews.hk
- Prospectuses
- Announcements
- Allotment results

### A-Share IPO

**EastMoney IPO Center**: http://data.eastmoney.com/xg/xg/default.html
- Subscription calendar
- Winning numbers
- Issue prices

**CNInfo**: http://www.cninfo.com.cn
- Official prospectuses

---

## Rate Limiting Best Practices

### Token Bucket Implementation

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
def fetch_with_retry(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

### Recommended Delays

| Source | Delay Between Requests |
|--------|------------------------|
| Yahoo Finance | 0.5s |
| EastMoney | 0.6s |
| Sina Finance | 1.0s |
| FRED API | 0.5s |
| CoinGecko | 1.0s |

---

## Caching Strategy

### TTL by Data Type

| Data Type | TTL | Reason |
|-----------|-----|--------|
| Real-time quotes | 1-5 min | Frequent updates |
| Daily OHLCV | 1 hour | Stable after close |
| Fundamentals | 24 hours | Quarterly updates |
| Economic data | 1 hour | Monthly/quarterly |
| IPO calendar | 30 min | Time-sensitive |
| News | 15 min | Fresh content |

### File Cache Structure

```
cache/
├── quotes/
│   └── {ticker}_{timestamp}.json
├── historical/
│   └── {ticker}_{period}.parquet
├── fundamentals/
│   └── {ticker}_info.json
└── macro/
    └── {series_id}.json
```
