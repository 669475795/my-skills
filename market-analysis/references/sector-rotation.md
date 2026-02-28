# Sector Rotation Analysis Reference

## Table of Contents
1. [Economic Cycle & Sector Map](#economic-cycle--sector-map)
2. [GICS Sectors Quick Reference](#gics-sectors-quick-reference)
3. [Rotation Signals](#rotation-signals)
4. [A-Share Sector Characteristics](#a-share-sector-characteristics)
5. [Sector Analysis Workflow](#sector-analysis-workflow)

---

## Economic Cycle & Sector Map

The economic cycle has four phases. Each phase historically favors different sectors.

```
        EXPANSION ──────────────→ PEAK
            ↑                       ↓
        TROUGH ←──────────── CONTRACTION
```

### Phase 1: Early Expansion (Recovery)
**Characteristics**: GDP turning up, rates low, unemployment high but falling
**Top sectors**:
- Financials (banks profit from steepening yield curve)
- Consumer Discretionary (pent-up demand)
- Industrials (early capex recovery)
- Real Estate (low rates support)

**Avoid**: Defensive sectors (expensive relative to cyclicals)

---

### Phase 2: Mid Expansion (Growth)
**Characteristics**: Strong GDP, employment recovering, rates rising gradually
**Top sectors**:
- Technology (earnings leverage)
- Materials (commodity demand)
- Industrials (strong capex)
- Communication Services

**Neutral**: Healthcare, Consumer Staples

---

### Phase 3: Late Expansion (Overheating)
**Characteristics**: High GDP, tight labor, inflation rising, rates hiking aggressively
**Top sectors**:
- Energy (inflation hedge, supply constraints)
- Materials (commodity prices high)
- Healthcare (defensive rotation beginning)
- Consumer Staples (pricing power)

**Avoid**: Rate-sensitive (Tech growth, REITs, Utilities)

---

### Phase 4: Contraction (Recession)
**Characteristics**: GDP falling, unemployment rising, rates flat/falling
**Top sectors**:
- Consumer Staples (non-cyclical demand)
- Healthcare (inelastic spending)
- Utilities (regulated, dividend stability)
- Treasuries / Gold (flight to safety)

**Avoid**: Cyclicals (Industrials, Materials, Consumer Discretionary)

---

## GICS Sectors Quick Reference

11 sectors tracked by S&P 500 / MSCI frameworks:

| # | Sector | US ETF | China ETF | Key Characteristics |
|---|--------|--------|-----------|---------------------|
| 1 | Technology | XLK | 512480.SS | High growth, rate-sensitive |
| 2 | Healthcare | XLV | 159929.SZ | Defensive, stable demand |
| 3 | Financials | XLF | 512070.SS | Yield curve sensitive |
| 4 | Consumer Discretionary | XLY | 159928.SZ | Cyclical, GDP sensitive |
| 5 | Consumer Staples | XLP | 512600.SS | Defensive, inflation pricing power |
| 6 | Industrials | XLI | 512800.SS | Late cycle, capex driven |
| 7 | Energy | XLE | 159987.SZ | Commodity prices, geopolitics |
| 8 | Materials | XLB | 512400.SS | Early/late cycle |
| 9 | Utilities | XLU | 159796.SZ | Defensive, rate-sensitive (inverse) |
| 10 | Real Estate | XLRE | 512200.SS | Rate-sensitive, income |
| 11 | Communication Services | XLC | 516160.SS | Mixed growth/defensive |

### Sector Relative Strength Calculation
```bash
# Fetch all sector ETFs for relative comparison
python scripts/fetch_stock_data.py XLK XLF XLE XLV XLP XLU XLB XLI XLRE XLC XLY --period 3mo

# Generate comparison chart
python scripts/chart_generator.py --compare --tickers "XLK,XLF,XLE,XLV,XLP" --period 3mo
```

---

## Rotation Signals

### Signal 1: Relative Strength Ranking
Rank sectors by 1-month and 3-month performance:
- **Double top performers** (both timeframes): Strong momentum, continue overweight
- **Short-term leader, long-term laggard**: Rotation just starting, monitor
- **Long-term leader, short-term laggard**: Rotation out, consider underweight

### Signal 2: Rate Environment Sector Implications

| Rate Environment | Favor | Avoid |
|-----------------|-------|-------|
| Rates rising fast | Energy, Financials, Materials | Utilities, REITs, Tech (high duration) |
| Rates falling | Utilities, REITs, Long-duration Tech | Banks (NIM compression) |
| Yield curve steepening | Financials (banks) | - |
| Yield curve inverting | Defensives, Healthcare, Staples | Cyclicals |

### Signal 3: Commodity Prices
| Commodity | Beneficiary Sector |
|-----------|-------------------|
| Oil rising | Energy, Materials |
| Gold rising | Materials (miners), Utilities (safe haven) |
| Copper rising | Materials, Industrials (early cycle signal) |
| Agricultural prices rising | Consumer Staples (cost pressure), Fertilizers (Materials) |

### Signal 4: Currency (USD)
| USD Direction | Favor | Headwind |
|-------------|-------|---------|
| USD strengthening | Domestic focus sectors (Utilities, Telecom) | Multinationals (Tech, Materials) |
| USD weakening | Multinationals, Commodities, EM exposure | Domestic defensives |

### Signal 5: Earnings Revision Breadth
Track which sectors have the highest proportion of upward EPS revisions:
- Rising revision breadth → likely sector leadership
- Falling revision breadth → likely sector underperformance

---

## A-Share Sector Characteristics

### Policy-Driven Sectors (中国特色)

A-share sectors are significantly influenced by government policy. Always check policy backdrop.

| Sector | Key Policy Drivers | Current Status (Check latest) |
|--------|-------------------|-------------------------------|
| 新能源 (NEV/Renewables) | Carbon neutrality 2060, NEV subsidies | Policy sensitive |
| 半导体 (Semiconductors) | 国产替代, 大基金 | Strategic priority, high subsidy |
| 军工 (Defense) | Military modernization, budget | Counter-cyclical, policy floor |
| 医疗器械 (Medical Devices) | 集采 (centralized procurement) | Headwind from pricing pressure |
| 房地产 (Real Estate) | 三条红线, LPR cuts | Policy support but structural headwind |
| 互联网 (Internet) | Platform regulation, data security | Regulatory risk |
| 消费 (Consumption) | 内循环, 促消费政策 | Policy support |

### A-Share Sector ETFs (China)
| Sector | ETF Code |
|--------|---------|
| 科技 | 515000.SS (科技ETF) |
| 消费 | 159928.SZ (消费ETF) |
| 医药 | 159929.SZ (医药ETF) |
| 新能源 | 159758.SZ (新能源ETF) |
| 半导体 | 512480.SS (半导体ETF) |
| 军工 | 512660.SS (军工ETF) |
| 券商 | 512000.SS (券商ETF) |
| 银行 | 512800.SS (银行ETF) |

### A-Share Rotation Patterns
1. **政策底 → 市场底**: Policy support announced → market starts to stabilize
2. **科技vs消费轮动**: In risk-on environments, tech leads; in uncertain environments, consumption defensive
3. **北向资金引导**: When foreign inflows (northbound) are concentrated in a sector, it often leads near-term
4. **两会期间**: National People's Congress period (March) often see policy sector pumps

---

## Sector Analysis Workflow

### Step 1: Determine Economic Phase
```bash
python scripts/fetch_macro_data.py --summary --rates --inflation
```
- GDP trend: Accelerating / Decelerating?
- Inflation: Rising / Falling?
- Yield curve: Steepening / Flattening / Inverted?
- → Map to Phase 1/2/3/4

### Step 2: Fetch Sector Performance
```bash
python scripts/fetch_stock_data.py XLK XLF XLE XLV XLP XLU XLB XLI XLRE XLC XLY --period 1mo --metrics
```

### Step 3: Rank by Relative Strength
- Sort by 1-month return
- Cross-check with 3-month return
- Identify leaders and laggards

### Step 4: Read Rotation Signals
- Apply Rate Environment matrix
- Apply USD direction
- Check commodity trends

### Step 5: Output Recommendation
```
板块配置建议 [日期]

经济周期阶段: [Phase] - [描述]
利率环境: [Rising/Falling/Stable]

超配板块 (Overweight):
1. [Sector] — 理由: [2 sentences]
2. [Sector] — 理由: [2 sentences]
3. [Sector] — 理由: [2 sentences]

低配板块 (Underweight):
1. [Sector] — 理由: [2 sentences]
2. [Sector] — 理由: [2 sentences]

关键风险: [What could change this rotation view]
```
