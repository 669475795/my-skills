# Risk Assessment Report

**Portfolio/Position**: {{NAME}}
**Report Date**: {{DATE}}
**Assessment Period**: {{PERIOD}}

---

## Executive Summary

| Risk Category | Level | Score |
|---------------|-------|-------|
| Overall Risk | {{OVERALL_RISK_LEVEL}} | {{OVERALL_RISK_SCORE}}/100 |
| Market Risk | {{MARKET_RISK_LEVEL}} | {{MARKET_RISK_SCORE}}/100 |
| Liquidity Risk | {{LIQUIDITY_RISK_LEVEL}} | {{LIQUIDITY_RISK_SCORE}}/100 |
| Concentration Risk | {{CONC_RISK_LEVEL}} | {{CONC_RISK_SCORE}}/100 |
| Volatility Risk | {{VOL_RISK_LEVEL}} | {{VOL_RISK_SCORE}}/100 |

### Key Risk Alerts
{{#RISK_ALERTS}}
- **{{ALERT_SEVERITY}}**: {{ALERT_MESSAGE}}
{{/RISK_ALERTS}}

---

## Position Details

| Field | Value |
|-------|-------|
| Total Value | {{TOTAL_VALUE}} |
| Number of Positions | {{NUM_POSITIONS}} |
| Largest Position | {{LARGEST_POSITION}} ({{LARGEST_WEIGHT}}%) |
| Avg Position Size | {{AVG_POSITION_SIZE}} |

---

## Value at Risk (VaR) Analysis

### VaR Summary

| Method | 95% Confidence | 99% Confidence |
|--------|----------------|----------------|
| Historical VaR (1-day) | {{HIST_VAR_95_1D}}% | {{HIST_VAR_99_1D}}% |
| Parametric VaR (1-day) | {{PARA_VAR_95_1D}}% | {{PARA_VAR_99_1D}}% |
| Monte Carlo VaR (1-day) | {{MC_VAR_95_1D}}% | {{MC_VAR_99_1D}}% |

### Dollar VaR

| Confidence | 1-Day | 5-Day | 10-Day | 1-Month |
|------------|-------|-------|--------|---------|
| 95% | {{VAR_95_1D_DOLLAR}} | {{VAR_95_5D_DOLLAR}} | {{VAR_95_10D_DOLLAR}} | {{VAR_95_1M_DOLLAR}} |
| 99% | {{VAR_99_1D_DOLLAR}} | {{VAR_99_5D_DOLLAR}} | {{VAR_99_10D_DOLLAR}} | {{VAR_99_1M_DOLLAR}} |

### VaR Interpretation
- **95% 1-Day VaR of {{HIST_VAR_95_1D}}%** means:
  - 95% confident the portfolio won't lose more than {{VAR_95_1D_DOLLAR}} in one day
  - Expect to breach this limit ~13 times per year (5% of 252 trading days)

### Expected Shortfall (CVaR)

| Confidence | CVaR | Interpretation |
|------------|------|----------------|
| 95% | {{CVAR_95}}% | Average loss when VaR is exceeded |
| 99% | {{CVAR_99}}% | Tail risk measure |

---

## Volatility Analysis

### Historical Volatility

| Period | Volatility | Annualized |
|--------|------------|------------|
| 5-Day | {{VOL_5D}}% | {{VOL_5D_ANN}}% |
| 20-Day | {{VOL_20D}}% | {{VOL_20D_ANN}}% |
| 60-Day | {{VOL_60D}}% | {{VOL_60D_ANN}}% |
| 252-Day | {{VOL_252D}}% | {{VOL_252D}}% |

### Volatility Comparison

| Asset/Index | Volatility | vs Portfolio |
|-------------|------------|--------------|
| {{BENCHMARK}} | {{BENCH_VOL}}% | {{VOL_VS_BENCH}} |
| VIX | {{VIX_LEVEL}} | - |

### Volatility Trend
- Current vs 20-Day Avg: {{VOL_TREND_20D}}
- Current vs 60-Day Avg: {{VOL_TREND_60D}}
- Assessment: {{VOL_ASSESSMENT}}

---

## Drawdown Analysis

### Current Status

| Metric | Value |
|--------|-------|
| Current Drawdown | {{CURRENT_DD}}% |
| Peak Value | {{PEAK_VALUE}} |
| Peak Date | {{PEAK_DATE}} |
| Trough Value | {{TROUGH_VALUE}} |
| Trough Date | {{TROUGH_DATE}} |
| Current Value | {{CURRENT_VALUE}} |

### Historical Drawdowns

| Rank | Start | End | Depth | Duration | Recovery |
|------|-------|-----|-------|----------|----------|
{{#DRAWDOWNS}}
| {{RANK}} | {{START}} | {{END}} | {{DEPTH}}% | {{DURATION}} days | {{RECOVERY}} days |
{{/DRAWDOWNS}}

### Recovery Analysis

| Drawdown | Gain Required to Recover |
|----------|--------------------------|
| 10% | 11.1% |
| 20% | 25.0% |
| 30% | 42.9% |
| 50% | 100.0% |
| **Current ({{CURRENT_DD}}%)** | **{{RECOVERY_NEEDED}}%** |

---

## Beta & Market Sensitivity

### Beta Analysis

| Benchmark | Beta | Interpretation |
|-----------|------|----------------|
| S&P 500 | {{BETA_SPY}} | {{BETA_SPY_INTERP}} |
| NASDAQ | {{BETA_QQQ}} | {{BETA_QQQ_INTERP}} |
| Sector ETF | {{BETA_SECTOR}} | {{BETA_SECTOR_INTERP}} |

### Beta Risk Scenarios

| Market Move | Portfolio Impact |
|-------------|------------------|
| Market +10% | {{IMPACT_UP_10}}% |
| Market +5% | {{IMPACT_UP_5}}% |
| Market -5% | {{IMPACT_DOWN_5}}% |
| Market -10% | {{IMPACT_DOWN_10}}% |
| Market -20% | {{IMPACT_DOWN_20}}% |

---

## Concentration Risk

### Top Holdings Concentration

| Holdings | Weight |
|----------|--------|
| Top 1 | {{TOP_1}}% |
| Top 3 | {{TOP_3}}% |
| Top 5 | {{TOP_5}}% |
| Top 10 | {{TOP_10}}% |

**Concentration Risk Level**: {{CONC_LEVEL}}

### Sector Concentration

| Sector | Weight | Benchmark | Over/Under |
|--------|--------|-----------|------------|
{{#SECTORS}}
| {{SECTOR}} | {{WEIGHT}}% | {{BENCH_WEIGHT}}% | {{DIFF}}% |
{{/SECTORS}}

### Single Stock Risk
**Positions exceeding 10% weight**:
{{#LARGE_POSITIONS}}
- {{SYMBOL}}: {{WEIGHT}}% ({{RISK_NOTE}})
{{/LARGE_POSITIONS}}

---

## Liquidity Risk

### Liquidity Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Avg Daily Volume (ADV) | {{ADV}} | - |
| Days to Liquidate (100%) | {{DAYS_LIQ_100}} | {{LIQ_STATUS_100}} |
| Days to Liquidate (50%) | {{DAYS_LIQ_50}} | {{LIQ_STATUS_50}} |
| Illiquid Holdings (%) | {{ILLIQUID_PCT}}% | {{ILLIQUID_STATUS}} |

### Liquidity by Holding

| Symbol | Avg Volume | Position | Days to Exit |
|--------|------------|----------|--------------|
{{#LIQUIDITY_DETAIL}}
| {{SYMBOL}} | {{AVG_VOL}} | {{POSITION}} | {{DAYS_EXIT}} |
{{/LIQUIDITY_DETAIL}}

### Liquidity Score
**Score**: {{LIQUIDITY_SCORE}}/100
- Above 80: Highly liquid
- 60-80: Adequate liquidity
- 40-60: Moderate liquidity concerns
- Below 40: Significant liquidity risk

---

## Stress Testing

### Historical Scenarios

| Scenario | Period | Market | Portfolio | Difference |
|----------|--------|--------|-----------|------------|
| 2008 Financial Crisis | Sep-Nov 2008 | -46% | {{STRESS_2008}}% | {{DIFF_2008}}% |
| 2020 COVID Crash | Feb-Mar 2020 | -34% | {{STRESS_2020}}% | {{DIFF_2020}}% |
| 2022 Rate Shock | Jan-Jun 2022 | -23% | {{STRESS_2022}}% | {{DIFF_2022}}% |

### Hypothetical Scenarios

| Scenario | Assumptions | Impact |
|----------|-------------|--------|
| Market Crash | S&P -30% | {{HYPO_CRASH}}% |
| Rate Spike | +300bp rates | {{HYPO_RATES}}% |
| Volatility Surge | VIX to 80 | {{HYPO_VIX}}% |
| Dollar Surge | USD +15% | {{HYPO_USD}}% |
| Stagflation | High inflation + recession | {{HYPO_STAGFLATION}}% |

### Worst Case Analysis
**Extreme Scenario (99.9% VaR)**: {{EXTREME_VAR}}%
**Dollar Impact**: {{EXTREME_DOLLAR}}

---

## Correlation Risk

### Correlation Matrix

{{CORRELATION_MATRIX}}

### Correlation Statistics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Average Correlation | {{AVG_CORR}} | {{CORR_INTERP}} |
| Max Correlation | {{MAX_CORR}} | Between {{MAX_CORR_PAIR}} |
| Min Correlation | {{MIN_CORR}} | Between {{MIN_CORR_PAIR}} |

### Diversification Benefit
**Diversification Ratio**: {{DIV_RATIO}}
- Value > 1 indicates diversification benefit
- Current portfolio volatility: {{PORT_VOL}}%
- Weighted average volatility: {{WEIGHTED_VOL}}%
- Reduction from diversification: {{VOL_REDUCTION}}%

---

## Risk-Adjusted Metrics

| Metric | Value | Benchmark | Assessment |
|--------|-------|-----------|------------|
| Sharpe Ratio | {{SHARPE}} | {{BENCH_SHARPE}} | {{SHARPE_ASSESS}} |
| Sortino Ratio | {{SORTINO}} | {{BENCH_SORTINO}} | {{SORTINO_ASSESS}} |
| Calmar Ratio | {{CALMAR}} | {{BENCH_CALMAR}} | {{CALMAR_ASSESS}} |
| Information Ratio | {{INFO_RATIO}} | - | {{IR_ASSESS}} |
| Treynor Ratio | {{TREYNOR}} | - | {{TREYNOR_ASSESS}} |

---

## Position Sizing Analysis

### Current Position Sizes

| Symbol | Value | Risk (Vol) | Position Risk | Max Recommended |
|--------|-------|------------|---------------|-----------------|
{{#POSITION_SIZES}}
| {{SYMBOL}} | {{VALUE}} | {{VOLATILITY}}% | {{POS_RISK}} | {{MAX_REC}} |
{{/POSITION_SIZES}}

### Optimal Position Sizing (2% Risk Per Trade)

| Symbol | Current | Optimal | Action |
|--------|---------|---------|--------|
{{#OPTIMAL_SIZING}}
| {{SYMBOL}} | {{CURRENT}} | {{OPTIMAL}} | {{ACTION}} |
{{/OPTIMAL_SIZING}}

---

## Risk Limits & Compliance

### Risk Limit Status

| Limit | Threshold | Current | Status | Headroom |
|-------|-----------|---------|--------|----------|
| Max Position Size | {{LIMIT_POS}}% | {{CURRENT_POS}}% | {{STATUS_POS}} | {{HEAD_POS}}% |
| Max Sector Exposure | {{LIMIT_SECTOR}}% | {{CURRENT_SECTOR}}% | {{STATUS_SECTOR}} | {{HEAD_SECTOR}}% |
| Max Drawdown | {{LIMIT_DD}}% | {{CURRENT_DD}}% | {{STATUS_DD}} | {{HEAD_DD}}% |
| Daily Loss Limit | {{LIMIT_DAILY}}% | {{CURRENT_DAILY}}% | {{STATUS_DAILY}} | {{HEAD_DAILY}}% |
| VaR Limit | {{LIMIT_VAR}}% | {{CURRENT_VAR}}% | {{STATUS_VAR}} | {{HEAD_VAR}}% |

### Limit Breaches
{{#BREACHES}}
- **{{BREACH_DATE}}**: {{BREACH_DESC}} ({{BREACH_ACTION}})
{{/BREACHES}}

---

## Risk Mitigation Recommendations

### Immediate Actions
{{#IMMEDIATE_ACTIONS}}
1. **{{ACTION_TITLE}}**: {{ACTION_DESC}}
   - Priority: {{PRIORITY}}
   - Impact: {{IMPACT}}
{{/IMMEDIATE_ACTIONS}}

### Hedging Suggestions

| Risk Factor | Current Exposure | Hedge Instrument | Cost Est. |
|-------------|------------------|------------------|-----------|
{{#HEDGES}}
| {{RISK_FACTOR}} | {{EXPOSURE}} | {{INSTRUMENT}} | {{COST}} |
{{/HEDGES}}

### Portfolio Adjustments

| Action | Symbol | Amount | Rationale |
|--------|--------|--------|-----------|
{{#ADJUSTMENTS}}
| {{ACTION}} | {{SYMBOL}} | {{AMOUNT}} | {{RATIONALE}} |
{{/ADJUSTMENTS}}

---

## Monitoring & Alerts

### Alert Thresholds

| Metric | Warning | Critical | Current |
|--------|---------|----------|---------|
| Daily Loss | {{WARN_DAILY}}% | {{CRIT_DAILY}}% | {{CURR_DAILY}}% |
| Drawdown | {{WARN_DD}}% | {{CRIT_DD}}% | {{CURR_DD}}% |
| VaR Breach | {{WARN_VAR}}% | {{CRIT_VAR}}% | {{CURR_VAR}}% |
| Volatility | {{WARN_VOL}}% | {{CRIT_VOL}}% | {{CURR_VOL}}% |

### Active Alerts
{{#ACTIVE_ALERTS}}
- [{{ALERT_TIME}}] **{{ALERT_LEVEL}}**: {{ALERT_MSG}}
{{/ACTIVE_ALERTS}}

---

## Appendix

### Methodology
- VaR calculated using {{VAR_METHOD}} method
- Lookback period: {{LOOKBACK}} trading days
- Confidence intervals: 95% and 99%
- Risk-free rate: {{RF_RATE}}%

### Assumptions & Limitations
- Historical data may not predict future performance
- Correlation assumptions may break down in crisis
- VaR underestimates tail risk
- Liquidity assumptions based on average conditions

### Data Sources
- Price Data: {{PRICE_SOURCE}}
- Volatility Data: {{VOL_SOURCE}}
- Benchmark: {{BENCHMARK}}

---

## Disclaimer

This risk assessment is for informational purposes only and does not constitute financial advice. Risk metrics are based on historical data and mathematical models that have inherent limitations. Actual losses may exceed calculated risk measures, especially during extreme market conditions.

**Report Generated**: {{TIMESTAMP}}
