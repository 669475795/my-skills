# Macroeconomic Indicators Guide

## Key Economic Indicators

### GDP (Gross Domestic Product)
- **Frequency**: Quarterly
- **Source**: BEA (US), NBS (China)
- **Importance**: Overall economic health

| GDP Growth | Interpretation |
|------------|----------------|
| > 3% | Strong expansion |
| 2-3% | Healthy growth |
| 0-2% | Slow growth |
| < 0% | Contraction/Recession |

### Inflation Indicators

#### CPI (Consumer Price Index)
- **Frequency**: Monthly
- **FRED Series**: CPIAUCSL
- **Target**: Fed targets ~2% annually

| CPI YoY | Interpretation |
|---------|----------------|
| > 4% | High inflation |
| 2-3% | Target range |
| < 2% | Disinflation risk |
| < 0% | Deflation |

#### Core CPI
- Excludes food and energy
- More stable, preferred by Fed
- FRED Series: CPILFESL

#### PCE (Personal Consumption Expenditure)
- Fed's preferred inflation measure
- FRED Series: PCEPI
- Core PCE excludes food/energy

### Employment

#### Unemployment Rate
- **Frequency**: Monthly (First Friday)
- **FRED Series**: UNRATE
- Natural rate estimate: 4-5%

| Unemployment | Interpretation |
|--------------|----------------|
| < 4% | Tight labor market |
| 4-5% | Full employment |
| 5-7% | Elevated |
| > 7% | High unemployment |

#### Nonfarm Payrolls
- Monthly job gains/losses
- FRED Series: PAYEMS
- Healthy: 150-250K per month

#### Initial Jobless Claims
- Weekly new unemployment filings
- FRED Series: ICSA
- Leading indicator

### Interest Rates

#### Federal Funds Rate
- Fed's primary policy tool
- FRED Series: FEDFUNDS
- Affects all borrowing rates

#### Treasury Yields
| Maturity | FRED Series | Use |
|----------|-------------|-----|
| 3-Month | DTB3 | Money market proxy |
| 2-Year | DGS2 | Fed expectations |
| 10-Year | DGS10 | Mortgage rates benchmark |
| 30-Year | DGS30 | Long-term expectations |

### Manufacturing & Business

#### ISM Manufacturing PMI
- > 50: Expansion
- < 50: Contraction
- 50: Neutral

#### Industrial Production
- FRED Series: INDPRO
- Manufacturing output measure

#### Capacity Utilization
- FRED Series: TCU
- Inflation pressure indicator

### Consumer

#### Retail Sales
- FRED Series: RSAFS
- Consumer spending health

#### Consumer Confidence
- Conference Board and UMich surveys
- Leading indicator of spending

### Housing

#### Housing Starts
- FRED Series: HOUST
- Leading indicator

#### Existing Home Sales
- Lagging indicator
- Wealth effect implications

## Economic Calendar

### High-Impact Events
| Event | Frequency | Typical Release |
|-------|-----------|-----------------|
| FOMC Decision | 8x/year | Wednesday 2pm ET |
| Jobs Report | Monthly | First Friday 8:30am ET |
| CPI | Monthly | ~10th of month |
| GDP | Quarterly | End of month |
| PCE | Monthly | End of month |

### Fed Meeting Schedule
- 8 scheduled meetings per year
- Unscheduled possible in crisis
- Minutes released 3 weeks after

## Economic Cycle Phases

### Expansion
- Rising GDP
- Falling unemployment
- Rising corporate profits
- **Best sectors**: Cyclicals, small caps

### Peak
- Full employment
- Rising inflation
- Tight credit
- **Best sectors**: Energy, materials

### Contraction
- Falling GDP
- Rising unemployment
- Falling profits
- **Best sectors**: Defensives, utilities

### Trough
- Stabilizing indicators
- Fed stimulus
- Early recovery signs
- **Best sectors**: Financials, industrials

## CLI Usage

```bash
# Get specific indicator
python fetch_macro_data.py fed_funds_rate

# Interest rates overview
python fetch_macro_data.py --rates

# Inflation data
python fetch_macro_data.py --inflation

# Employment data
python fetch_macro_data.py --employment

# China macro data
python fetch_macro_data.py --china

# Currency data
python fetch_macro_data.py --currency

# Economic summary
python fetch_macro_data.py --summary

# List available indicators
python fetch_macro_data.py --list
```

## Data Sources

### Free Sources
| Source | Coverage | Access |
|--------|----------|--------|
| FRED | US macro | API (free key) |
| 东方财富 | China | Web/API |
| BLS | Employment | Web |
| BEA | GDP, Trade | Web |

### Getting FRED API Key
1. Visit https://fred.stlouisfed.org
2. Create account
3. Request API key
4. Set environment variable: `FRED_API_KEY`

## Market Implications

### Rate Hike Environment
- Bond prices fall
- Bank stocks may benefit
- Growth stocks pressured
- Dollar strengthens

### Rate Cut Environment
- Bond prices rise
- Growth stocks benefit
- Dollar weakens
- Commodities may rise

### High Inflation
- TIPS outperform nominal bonds
- Commodities benefit
- Real assets preferred
- Avoid long-duration bonds

### Recession Signals
- Inverted yield curve
- Rising initial claims
- Falling leading indicators
- Defensive positioning warranted
