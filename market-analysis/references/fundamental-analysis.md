# Fundamental Analysis Reference

## Table of Contents
1. [Valuation Frameworks](#valuation-frameworks)
2. [DCF Model](#dcf-model)
3. [Earnings Analysis](#earnings-analysis)
4. [Quality Metrics](#quality-metrics)
5. [Sector-Specific Metrics](#sector-specific-metrics)
6. [A-Share Special Factors](#a-share-special-factors)
7. [Red Flags](#red-flags)

---

## Valuation Frameworks

### Relative Valuation (Comparable Analysis)

**Step 1**: Identify peer group (same industry, similar size)
**Step 2**: Calculate key multiples for peers
**Step 3**: Compare target company vs peer median

| Multiple | Formula | When to Use |
|---------|---------|-------------|
| P/E | Price / EPS | Profitable companies |
| Forward P/E | Price / Next Year EPS | Growth stocks |
| P/S | Market Cap / Revenue | Loss-making growth |
| P/B | Price / Book Value | Banks, asset-heavy |
| EV/EBITDA | Enterprise Value / EBITDA | Capital-intensive |
| PEG | P/E / Growth Rate | Growth vs value balance |
| EV/Sales | Enterprise Value / Revenue | SaaS, high-growth |

**Interpretation guidance:**
- Premium to peers: justified if higher growth, margins, or moat
- Discount to peers: investigate why (risk? temporary headwind? value trap?)
- PEG < 1: growth not priced in (potentially undervalued)

### Absolute Valuation Summary

| Method | Best For | Sensitivity |
|--------|---------|-------------|
| DCF | Stable cash flows | Very high (WACC, growth) |
| Dividend Discount | Dividend payers | High |
| Asset-based | Banks, REITs | Moderate |
| Earnings Power | Cyclicals | Moderate |

---

## DCF Model

### Quick DCF Template

```
Intrinsic Value = Σ(FCF_t / (1+WACC)^t) + Terminal Value / (1+WACC)^n

Terminal Value = FCF_n × (1 + g) / (WACC - g)
```

**Where:**
- FCF = Free Cash Flow = Operating Cash Flow - CapEx
- WACC = Weighted Average Cost of Capital
- g = Terminal growth rate (typically 2-3%, GDP growth)
- n = Forecast period (usually 5-10 years)

### WACC Estimation

```
WACC = (E/V × Re) + (D/V × Rd × (1 - Tax Rate))
```

| Component | Typical Range |
|-----------|--------------|
| Risk-free rate | 10Y Treasury yield |
| Equity risk premium | 4-6% (US), 6-8% (EM) |
| Beta (tech growth) | 1.2-1.8 |
| Beta (utilities) | 0.4-0.7 |
| Resulting WACC (US large cap) | 8-12% |

### Sensitivity Table (always include)

Vary WACC (±1%) and terminal growth (±0.5%) to show value range:

```
           Terminal Growth Rate
           1.5%    2.0%    2.5%
WACC 9%   $XX     $XX     $XX
WACC 10%  $XX     $XX     $XX
WACC 11%  $XX     $XX     $XX
```

### DCF Red Flags
- Terminal value > 80% of total value → too sensitive to assumptions
- Negative FCF requiring debt financing → higher risk
- Assumptions significantly better than historical performance

---

## Earnings Analysis

### Earnings Beat/Miss Framework

**Beat = Actual EPS > Consensus Estimate**

| Scenario | Typical Price Reaction | Action |
|---------|----------------------|--------|
| Large beat (>10%) + raised guidance | Strong rally +5-10% | Consider momentum entry |
| Beat + maintained guidance | Modest rally +2-5% | Reassess thesis |
| In-line + raised guidance | Rally +3-7% | Positive signal |
| Miss + cut guidance | Selloff -10-20% | Re-evaluate thesis |
| Miss + maintained guidance | Mixed -3-8% | Watch next quarter |

### Earnings Quality Checklist

- [ ] Revenue growth organic (not just acquisitions)?
- [ ] Margins expanding or contracting?
- [ ] EPS beat driven by buybacks or real earnings?
- [ ] Cash flow from operations matches net income?
- [ ] Working capital changes (receivables building = warning)?
- [ ] Guidance raised, maintained, or cut?
- [ ] Management tone: confident or hedging?

### Key Earnings Metrics to Extract

```
Revenue:          $X.XB  (vs est. $X.XB, +/-X%)
EPS (adj.):       $X.XX  (vs est. $X.XX, +/-X%)
Gross Margin:     XX%    (vs prior year XX%, Δ +/-Xbp)
Operating Margin: XX%    (vs prior year XX%, Δ +/-Xbp)
FCF:              $X.XB  (FCF margin: XX%)
Next Q Guidance:  Revenue $X.X-X.XB  (vs est. $X.XB)
```

### Earnings Calendar Usage

Before earnings:
1. Note consensus EPS and revenue estimates
2. Check options implied move (tells you market expectation of swing)
3. Identify 2-3 key metrics the market is focused on
4. Do NOT initiate large positions into earnings (binary event risk)

After earnings:
1. Read the actual release before the call
2. Listen for guidance language changes
3. Check if conference call tone matches the numbers

---

## Quality Metrics

### Profitability Quality

| Metric | Formula | Good |
|--------|---------|------|
| Gross Margin | Gross Profit / Revenue | >40% (tech), >20% (retail) |
| Operating Margin | EBIT / Revenue | >15% (good), >25% (excellent) |
| Net Margin | Net Income / Revenue | Context-dependent |
| ROE | Net Income / Equity | >15% |
| ROIC | NOPAT / Invested Capital | >WACC (value creation) |
| FCF Conversion | FCF / Net Income | >80% (high quality) |

### Balance Sheet Health

| Metric | Formula | Warning |
|--------|---------|---------|
| Debt/Equity | Total Debt / Equity | >2.0× (most sectors) |
| Net Debt/EBITDA | Net Debt / EBITDA | >3.0× risky, >5.0× distressed |
| Interest Coverage | EBIT / Interest Expense | <3.0× = concern |
| Current Ratio | Current Assets / Current Liabilities | <1.0 = liquidity risk |
| Altman Z-Score | Composite | <1.8 = distress zone |

### Growth Quality

- **Organic growth** > acquisition-driven (more sustainable)
- **Recurring revenue** > transactional (more predictable)
- **Expanding TAM** + market share gains (best combination)
- Revenue growth should exceed cost growth (operating leverage)

---

## Sector-Specific Metrics

### Technology / SaaS
| Metric | Definition | Good |
|--------|-----------|------|
| ARR / MRR | Annual/Monthly Recurring Revenue | Growing >20% YoY |
| Net Revenue Retention | Revenue from existing customers next year | >110% excellent |
| CAC Payback | Months to recover customer acquisition cost | <18 months |
| Rule of 40 | Revenue growth % + FCF margin % | >40 |
| LTV/CAC | Customer lifetime value / acquisition cost | >3× |

### Banks / Financials
| Metric | Good |
|--------|------|
| Net Interest Margin (NIM) | >3% (US banks) |
| Efficiency Ratio | <60% (lower better) |
| CET1 Ratio | >10% |
| NPL Ratio | <2% |
| ROE | >12% |

### Energy
| Metric | Notes |
|--------|-------|
| Reserve Replacement Ratio | >100% (finding new reserves) |
| Finding & Development Cost | $/boe |
| Break-even Oil Price | Viability at various prices |
| Debt/EBITDA | <2× for investment grade |

### Real Estate / REITs
| Metric | Notes |
|--------|-------|
| FFO (Funds From Operations) | Core earnings metric (use instead of EPS) |
| AFFO | Adjusted FFO, more accurate |
| Cap Rate | NOI / Property Value |
| Occupancy Rate | >90% healthy |
| Debt/Total Assets | <45% conservative |

### Pharmaceuticals / Biotech
| Metric | Notes |
|--------|-------|
| Pipeline depth | Phase I/II/III assets |
| Patent cliff exposure | Revenue at risk from generic competition |
| FDA approval probability | Phase II→III: ~30%, Phase III→Approval: ~60% |
| Cash runway | Months until next capital raise needed |

---

## A-Share Special Factors

### A-Share Valuation Adjustments

**Premium factors** (justify higher valuations):
- Policy-supported sectors (新能源, 半导体, AI)
- MSCI / index inclusion candidates
- State-owned enterprise reform beneficiaries

**Discount factors** (justify lower valuations):
- VIE structure risk (overseas-listed China)
- Regulatory uncertainty
- Weak corporate governance signals

### A-Share Specific Metrics

| Metric | Description |
|--------|-------------|
| 商誉 (Goodwill) | High goodwill from acquisitions = impairment risk |
| 解禁压力 | Lock-up expiry dates (major selling pressure event) |
| 股东减持 | Insider selling plans (bearish signal) |
| 业绩承诺 | Performance pledges (missed = goodwill writedown) |
| 北向资金 | Northbound capital flow (foreign investor sentiment) |
| 融资余额 | Margin financing balance (leverage sentiment) |

### A-Share Earnings Seasons
- **Q1 results**: April 30 deadline
- **Interim (H1)**: August 31 deadline
- **Q3 results**: October 31 deadline
- **Full year**: April 30 following year

**Key signal**: Companies with negative preliminary results (业绩预警) released before deadline are high-risk.

---

## Red Flags Checklist

### Accounting Red Flags
- [ ] Revenue growth >> cash flow from operations growth
- [ ] Large or growing accounts receivable relative to revenue
- [ ] Frequent "one-time" charges (rarely truly one-time)
- [ ] Revenue recognized aggressively (channel stuffing, bill-and-hold)
- [ ] Auditor change without explanation
- [ ] Related-party transactions at non-market terms
- [ ] Restated financials

### Business Red Flags
- [ ] CEO/CFO departure unexpectedly
- [ ] Multiple insider selling on same day
- [ ] Guidance lowered repeatedly ("kitchen-sink quarter" patterns)
- [ ] Core customers or major contracts lost
- [ ] Regulatory investigation opened
- [ ] Debt covenant waivers requested

### A-Share Specific Red Flags
- [ ] 大股东质押比例 >80% (controlling shareholder pledged >80% of shares)
- [ ] 商誉占净资产比例 >50%
- [ ] 审计意见非标准 (non-standard audit opinion)
- [ ] 连续三年扣非净利润下降
