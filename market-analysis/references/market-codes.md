# Stock Ticker and Symbol Formats

## US Stocks

### Format
- **Ticker only**, no suffix needed
- 1-5 characters, all uppercase
- Examples: `AAPL`, `TSLA`, `MSFT`, `GOOGL`, `BRK.B`

### Exchanges
- **NYSE**: New York Stock Exchange
- **NASDAQ**: NASDAQ Stock Market
- **AMEX**: American Stock Exchange

### Special Cases
- **Class shares**: `BRK.A` (Class A), `BRK.B` (Class B)
- **Preferred stock**: `BAC-PL` (Bank of America Preferred L)
- **Warrants**: `TSLAW` (Tesla Warrant)
- **When-issued**: `AAPL.WI`

### Common US Tickers

| Ticker | Company |
|--------|---------|
| AAPL | Apple Inc. |
| MSFT | Microsoft Corporation |
| GOOGL | Alphabet Inc. (Class A) |
| AMZN | Amazon.com Inc. |
| TSLA | Tesla Inc. |
| META | Meta Platforms Inc. |
| NVDA | NVIDIA Corporation |
| JPM | JPMorgan Chase & Co. |
| V | Visa Inc. |
| WMT | Walmart Inc. |

---

## Hong Kong Stocks (HKEX)

### Format
- **5-digit number + `.HK` suffix**
- Leading zeros required
- Examples: `00700.HK`, `09988.HK`, `01299.HK`

### H-Shares vs Red Chips
- **H-Shares**: Chinese companies listed in HK (e.g., `00939.HK` - China Construction Bank)
- **Red Chips**: HK-incorporated, mainland-controlled (e.g., `00270.HK` - Guangdong Investment)

### Common HK Tickers

| Ticker | Company | Type |
|--------|---------|------|
| 00700.HK | Tencent Holdings | Local |
| 09988.HK | Alibaba Group | Secondary listing |
| 00941.HK | China Mobile | H-Share |
| 01299.HK | AIA Group | Local |
| 00005.HK | HSBC Holdings | Local |
| 03690.HK | Meituan | Local |
| 09618.HK | JD.com | Secondary listing |
| 01810.HK | Xiaomi Corporation | Local |
| 00939.HK | China Construction Bank | H-Share |
| 02318.HK | Ping An Insurance | H-Share |

### Ticker Number Ranges
- **00001-00999**: Older listings
- **01000-09999**: Newer listings
- **80000-89999**: GEM (Growth Enterprise Market)

---

## China A-Shares

### Format
- **6-digit number + exchange suffix**
- **Shanghai**: `.SS` suffix (e.g., `600519.SS`)
- **Shenzhen**: `.SZ` suffix (e.g., `000001.SZ`)

### Shanghai Stock Exchange (SSE)
- **Main Board**: 600000-603999
- **B-Shares** (foreign): 900000-900999
- **STAR Market** (tech): 688000-689999

### Shenzhen Stock Exchange (SZSE)
- **Main Board**: 000001-001999
- **SME Board**: 002000-004999
- **ChiNext** (Growth): 300000-301999
- **B-Shares** (foreign): 200000-200999

### Common A-Share Tickers

| Ticker | Company | Exchange |
|--------|---------|----------|
| 600519.SS | Kweichow Moutai | Shanghai |
| 601398.SS | Industrial and Commercial Bank of China | Shanghai |
| 600036.SS | China Merchants Bank | Shanghai |
| 601888.SS | China International Travel Service | Shanghai |
| 000001.SZ | Ping An Bank | Shenzhen |
| 000858.SZ | Wuliangye | Shenzhen |
| 000333.SZ | Midea Group | Shenzhen |
| 002594.SZ | BYD | Shenzhen |
| 300750.SZ | Contemporary Amperex Technology | Shenzhen (ChiNext) |
| 688981.SS | Zhongxin Fluoride | Shanghai (STAR) |

---

## Cryptocurrencies

### Format
- **Symbol + `-USD` suffix** for Yahoo Finance
- All uppercase
- Examples: `BTC-USD`, `ETH-USD`, `BNB-USD`

### Major Cryptocurrencies

| Symbol | Full Name | Ticker |
|--------|-----------|--------|
| BTC | Bitcoin | BTC-USD |
| ETH | Ethereum | ETH-USD |
| BNB | Binance Coin | BNB-USD |
| XRP | Ripple | XRP-USD |
| ADA | Cardano | ADA-USD |
| DOGE | Dogecoin | DOGE-USD |
| SOL | Solana | SOL-USD |
| MATIC | Polygon | MATIC-USD |
| DOT | Polkadot | DOT-USD |
| LTC | Litecoin | LTC-USD |
| AVAX | Avalanche | AVAX-USD |
| LINK | Chainlink | LINK-USD |
| UNI | Uniswap | UNI-USD |
| ATOM | Cosmos | ATOM-USD |
| XLM | Stellar | XLM-USD |

### Stablecoins
| Symbol | Full Name | Ticker |
|--------|-----------|--------|
| USDT | Tether | USDT-USD |
| USDC | USD Coin | USDC-USD |
| BUSD | Binance USD | BUSD-USD |
| DAI | Dai | DAI-USD |

### Other Trading Pairs
- **BTC pairs**: `ETH-BTC`, `BNB-BTC`
- **EUR pairs**: `BTC-EUR`, `ETH-EUR`
- **GBP pairs**: `BTC-GBP`, `ETH-GBP`

---

## Other International Markets

### UK (London Stock Exchange)
- **Format**: Ticker + `.L` suffix
- **Examples**: `HSBA.L` (HSBC), `BP.L` (BP), `VOD.L` (Vodafone)

### Japan (Tokyo Stock Exchange)
- **Format**: 4-digit number + `.T` suffix
- **Examples**: `7203.T` (Toyota), `9984.T` (SoftBank), `6758.T` (Sony)

### Germany (Frankfurt)
- **Format**: Ticker + `.DE` suffix
- **Examples**: `VOW3.DE` (Volkswagen), `SAP.DE` (SAP), `SIE.DE` (Siemens)

### India (NSE/BSE)
- **NSE**: Ticker + `.NS` suffix (e.g., `RELIANCE.NS`)
- **BSE**: Ticker + `.BO` suffix (e.g., `RELIANCE.BO`)

### Canada (Toronto)
- **Format**: Ticker + `.TO` suffix
- **Examples**: `SHOP.TO` (Shopify), `TD.TO` (TD Bank)

### Australia (ASX)
- **Format**: Ticker + `.AX` suffix
- **Examples**: `CBA.AX` (Commonwealth Bank), `BHP.AX` (BHP)

---

## ETFs and Index Funds

### US ETFs
| Ticker | Fund Name |
|--------|-----------|
| SPY | SPDR S&P 500 ETF |
| QQQ | Invesco QQQ (NASDAQ-100) |
| DIA | SPDR Dow Jones Industrial Average |
| IWM | iShares Russell 2000 |
| VTI | Vanguard Total Stock Market |
| VOO | Vanguard S&P 500 |
| VEA | Vanguard FTSE Developed Markets |
| VWO | Vanguard FTSE Emerging Markets |
| AGG | iShares Core US Aggregate Bond |
| GLD | SPDR Gold Trust |

### Sector ETFs
| Ticker | Sector |
|--------|--------|
| XLK | Technology |
| XLF | Financials |
| XLV | Healthcare |
| XLE | Energy |
| XLI | Industrials |
| XLY | Consumer Discretionary |
| XLP | Consumer Staples |
| XLRE | Real Estate |
| XLB | Materials |
| XLU | Utilities |

---

## Market Indices

### US Indices
| Symbol | Index Name |
|--------|------------|
| ^GSPC | S&P 500 |
| ^DJI | Dow Jones Industrial Average |
| ^IXIC | NASDAQ Composite |
| ^RUT | Russell 2000 |
| ^VIX | CBOE Volatility Index |

### International Indices
| Symbol | Index Name |
|--------|------------|
| ^HSI | Hang Seng Index (Hong Kong) |
| 000001.SS | SSE Composite Index (Shanghai) |
| ^N225 | Nikkei 225 (Japan) |
| ^FTSE | FTSE 100 (UK) |
| ^GDAXI | DAX (Germany) |

---

## Validation Rules

### Checking Ticker Format

```python
import re

def validate_ticker(ticker):
    patterns = {
        "US": r"^[A-Z]{1,5}(\.[A-Z])?$",
        "HK": r"^\d{5}\.HK$",
        "CN_SH": r"^\d{6}\.SS$",
        "CN_SZ": r"^\d{6}\.SZ$",
        "CRYPTO": r"^[A-Z]{2,10}-USD$",
    }

    for market, pattern in patterns.items():
        if re.match(pattern, ticker):
            return market
    return None

# Examples
print(validate_ticker("AAPL"))      # US
print(validate_ticker("00700.HK"))  # HK
print(validate_ticker("600519.SS")) # CN_SH
print(validate_ticker("BTC-USD"))   # CRYPTO
```

---

## Common Errors and Solutions

### Error: No data available

**Cause**: Incorrect ticker format

**Solutions**:
1. **HK stocks**: Ensure 5 digits with leading zeros + `.HK`
   - ❌ `700.HK`
   - ✅ `00700.HK`

2. **China A-shares**: Ensure 6 digits + correct suffix
   - ❌ `600519`
   - ✅ `600519.SS`

3. **Crypto**: Ensure `-USD` suffix
   - ❌ `BTC`
   - ✅ `BTC-USD`

### Error: Symbol not found

**Solutions**:
1. Verify ticker on official exchange website
2. Check for delisting or symbol changes
3. Ensure market is supported by data source
4. Check for typos (common: `GOOGL` vs `GOOG`)

---

## Quick Reference: Format Examples

| Market | Format | Example |
|--------|--------|---------|
| US | TICKER | AAPL |
| Hong Kong | 00000.HK | 00700.HK |
| Shanghai | 000000.SS | 600519.SS |
| Shenzhen | 000000.SZ | 000001.SZ |
| Crypto | XXX-USD | BTC-USD |
| UK | TICKER.L | HSBA.L |
| Japan | 0000.T | 7203.T |
| Germany | TICKER.DE | SAP.DE |
| Canada | TICKER.TO | SHOP.TO |

---

## Options Symbols

### US Options (OCC Format)

**Format**: `ROOT + EXPIRY + TYPE + STRIKE`

**Components**:
- **Root**: Underlying ticker (1-6 chars)
- **Expiry**: YYMMDD format
- **Type**: C (Call) or P (Put)
- **Strike**: 8 digits (price × 1000)

**Examples**:
| Symbol | Meaning |
|--------|---------|
| AAPL240119C00185000 | AAPL Jan 19 2024 $185 Call |
| TSLA240216P00200000 | TSLA Feb 16 2024 $200 Put |
| SPY240315C00450000 | SPY Mar 15 2024 $450 Call |

### Yahoo Finance Options

**Format**: Ticker + Expiry + Type + Strike

**Examples**:
```python
import yfinance as yf
ticker = yf.Ticker("AAPL")

# Get available expiration dates
expirations = ticker.options
# ['2024-01-19', '2024-01-26', ...]

# Get option chain for specific date
chain = ticker.option_chain('2024-01-19')
calls = chain.calls
puts = chain.puts
```

### Options Data Fields

| Field | Description |
|-------|-------------|
| contractSymbol | Full OCC symbol |
| strike | Strike price |
| lastPrice | Last traded price |
| bid | Current bid |
| ask | Current ask |
| volume | Trading volume |
| openInterest | Open contracts |
| impliedVolatility | IV percentage |
| inTheMoney | Boolean ITM flag |

---

## Bond Symbols

### US Treasury Securities

**Format**: Varies by type

| Type | Format | Example |
|------|--------|---------|
| Treasury Bill | ^IRX (13-week) | ^IRX |
| 2-Year Note | DGS2 (FRED) | - |
| 5-Year Note | DGS5 (FRED) | - |
| 10-Year Note | ^TNX | ^TNX |
| 30-Year Bond | ^TYX | ^TYX |

### Treasury ETFs

| Symbol | Description | Duration |
|--------|-------------|----------|
| BIL | 1-3 Month T-Bill | Ultra-short |
| SHY | 1-3 Year Treasury | Short |
| IEI | 3-7 Year Treasury | Intermediate |
| IEF | 7-10 Year Treasury | Intermediate |
| TLH | 10-20 Year Treasury | Long |
| TLT | 20+ Year Treasury | Long |

### Corporate Bond ETFs

| Symbol | Description | Credit |
|--------|-------------|--------|
| LQD | iShares Investment Grade | IG |
| VCSH | Vanguard Short-term Corp | IG |
| VCIT | Vanguard Intermediate Corp | IG |
| HYG | iShares High Yield | HY |
| JNK | SPDR High Yield | HY |
| SHYG | iShares 0-5Y High Yield | HY |

### TIPS (Inflation Protected)

| Symbol | Description |
|--------|-------------|
| TIP | iShares TIPS Bond |
| SCHP | Schwab TIPS |
| VTIP | Vanguard Short-term TIPS |

### International Bonds

| Symbol | Description |
|--------|-------------|
| EMB | iShares Emerging Markets |
| BNDX | Vanguard International Bond |
| IGOV | iShares International Treasury |

### China Bonds (via EastMoney)

| Code | Description |
|------|-------------|
| CN10Y | China 10-Year Government Bond |
| CN5Y | China 5-Year Government Bond |
| CN2Y | China 2-Year Government Bond |

---

## Commodity & Precious Metal Symbols

### Precious Metals Futures

| Symbol | Description | Exchange |
|--------|-------------|----------|
| GC=F | Gold Futures | COMEX |
| SI=F | Silver Futures | COMEX |
| PL=F | Platinum Futures | NYMEX |
| PA=F | Palladium Futures | NYMEX |

### Precious Metal ETFs

| Symbol | Description | Type |
|--------|-------------|------|
| GLD | SPDR Gold Trust | Physical |
| IAU | iShares Gold Trust | Physical |
| SLV | iShares Silver Trust | Physical |
| PPLT | Physical Platinum | Physical |
| PALL | Physical Palladium | Physical |
| GDX | Gold Miners ETF | Equity |
| GDXJ | Junior Gold Miners | Equity |
| SIL | Silver Miners ETF | Equity |

### Energy Futures

| Symbol | Description |
|--------|-------------|
| CL=F | Crude Oil (WTI) |
| BZ=F | Brent Crude |
| NG=F | Natural Gas |
| RB=F | Gasoline |
| HO=F | Heating Oil |

### Agricultural Futures

| Symbol | Description |
|--------|-------------|
| ZC=F | Corn |
| ZS=F | Soybeans |
| ZW=F | Wheat |
| KC=F | Coffee |
| SB=F | Sugar |

### Shanghai Gold Exchange (via EastMoney)

| Code | Description |
|------|-------------|
| Au99.99 | Gold Spot |
| Au(T+D) | Gold Deferred |
| Ag(T+D) | Silver Deferred |

---

## Volatility & Sentiment Indices

### VIX & Volatility

| Symbol | Description |
|--------|-------------|
| ^VIX | CBOE Volatility Index |
| ^VXN | NASDAQ Volatility |
| ^VVIX | VIX of VIX |
| VIXY | VIX Short-term Futures ETF |
| UVXY | Ultra VIX Short-term |
| SVXY | Short VIX Short-term |

### Fear & Greed Components

| Indicator | Source |
|-----------|--------|
| VIX Level | ^VIX |
| Put/Call Ratio | CBOE |
| Advance/Decline | NYSE |
| New Highs/Lows | NYSE |
| Safe Haven Demand | Bond vs Stock flows |
| Junk Bond Spread | HYG vs LQD |
| Market Momentum | S&P vs 125-day MA |

---

## Currency Symbols

### Major Forex Pairs

| Symbol | Description |
|--------|-------------|
| EURUSD=X | Euro/US Dollar |
| USDJPY=X | US Dollar/Japanese Yen |
| GBPUSD=X | British Pound/US Dollar |
| USDCNH=X | US Dollar/Chinese Yuan (Offshore) |
| USDCNY=X | US Dollar/Chinese Yuan (Onshore) |
| USDHKD=X | US Dollar/Hong Kong Dollar |

### Currency ETFs

| Symbol | Description |
|--------|-------------|
| UUP | US Dollar Index Bullish |
| UDN | US Dollar Index Bearish |
| FXE | Euro Trust |
| FXY | Japanese Yen Trust |
| FXB | British Pound Trust |

---

## IPO Ticker Conventions

### Pre-IPO (US)

- Ticker assigned after SEC approval
- Trading begins on listing date
- Symbol shown in S-1 filing

### A-Share IPO

| Board | Code Range | Suffix |
|-------|------------|--------|
| Shanghai Main | 600XXX, 601XXX | .SS |
| Shanghai STAR | 688XXX | .SS |
| Shenzhen Main | 000XXX, 001XXX | .SZ |
| Shenzhen SME | 002XXX | .SZ |
| ChiNext | 300XXX, 301XXX | .SZ |

### Hong Kong IPO

| Type | Code Range | Suffix |
|------|------------|--------|
| Main Board | 00001-09999 | .HK |
| GEM | 08001-08999 | .HK |

---

## Resources

- **US**: [NYSE](https://www.nyse.com), [NASDAQ](https://www.nasdaq.com)
- **Hong Kong**: [HKEX](https://www.hkex.com.hk)
- **China**: [SSE](http://www.sse.com.cn), [SZSE](http://www.szse.cn)
- **Crypto**: [CoinMarketCap](https://coinmarketcap.com), [CoinGecko](https://www.coingecko.com)
- **Options**: [CBOE](https://www.cboe.com), [OCC](https://www.theocc.com)
- **Bonds**: [Treasury Direct](https://www.treasurydirect.gov), [FRED](https://fred.stlouisfed.org)
- **Commodities**: [CME Group](https://www.cmegroup.com)
- **Ticker Search**: [Yahoo Finance](https://finance.yahoo.com), [TradingView](https://www.tradingview.com)
