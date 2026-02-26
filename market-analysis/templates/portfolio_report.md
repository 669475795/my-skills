# Portfolio Analysis Report

**Portfolio Name**: {{PORTFOLIO_NAME}}
**Report Date**: {{DATE}}
**Reporting Period**: {{PERIOD_START}} to {{PERIOD_END}}

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Total Value** | {{TOTAL_VALUE}} |
| **Period Return** | {{PERIOD_RETURN}}% |
| **Benchmark Return** | {{BENCHMARK_RETURN}}% |
| **Alpha** | {{ALPHA}}% |
| **Risk Level** | {{RISK_LEVEL}} |
| **Sharpe Ratio** | {{SHARPE}} |

### Performance Highlights
- {{HIGHLIGHT_1}}
- {{HIGHLIGHT_2}}
- {{HIGHLIGHT_3}}

---

## Portfolio Composition

### Asset Allocation

| Asset Class | Value | Weight | Target | Deviation |
|-------------|-------|--------|--------|-----------|
{{#ASSET_CLASSES}}
| {{ASSET_CLASS}} | {{CLASS_VALUE}} | {{CLASS_WEIGHT}}% | {{CLASS_TARGET}}% | {{CLASS_DEV}}% |
{{/ASSET_CLASSES}}
| **Total** | {{TOTAL_VALUE}} | 100% | 100% | - |

### Holdings Detail

| Symbol | Name | Shares | Price | Value | Weight | Return |
|--------|------|--------|-------|-------|--------|--------|
{{#HOLDINGS}}
| {{SYMBOL}} | {{NAME}} | {{SHARES}} | {{PRICE}} | {{VALUE}} | {{WEIGHT}}% | {{RETURN}}% |
{{/HOLDINGS}}
| **Total** | - | - | - | {{TOTAL_VALUE}} | 100% | {{TOTAL_RETURN}}% |

### Sector Allocation

| Sector | Weight | Benchmark | Over/Under |
|--------|--------|-----------|------------|
{{#SECTORS}}
| {{SECTOR}} | {{SECTOR_WEIGHT}}% | {{SECTOR_BENCH}}% | {{SECTOR_DIFF}}% |
{{/SECTORS}}

### Geographic Allocation

| Region | Weight |
|--------|--------|
{{#REGIONS}}
| {{REGION}} | {{REGION_WEIGHT}}% |
{{/REGIONS}}

---

## Performance Analysis

### Returns Summary

| Period | Portfolio | Benchmark | Alpha |
|--------|-----------|-----------|-------|
| 1 Day | {{RET_1D}}% | {{BENCH_1D}}% | {{ALPHA_1D}}% |
| 1 Week | {{RET_1W}}% | {{BENCH_1W}}% | {{ALPHA_1W}}% |
| 1 Month | {{RET_1M}}% | {{BENCH_1M}}% | {{ALPHA_1M}}% |
| 3 Months | {{RET_3M}}% | {{BENCH_3M}}% | {{ALPHA_3M}}% |
| 6 Months | {{RET_6M}}% | {{BENCH_6M}}% | {{ALPHA_6M}}% |
| YTD | {{RET_YTD}}% | {{BENCH_YTD}}% | {{ALPHA_YTD}}% |
| 1 Year | {{RET_1Y}}% | {{BENCH_1Y}}% | {{ALPHA_1Y}}% |
| Since Inception | {{RET_INCEP}}% | {{BENCH_INCEP}}% | {{ALPHA_INCEP}}% |

### Monthly Returns

| Month | Portfolio | Benchmark | Alpha |
|-------|-----------|-----------|-------|
{{#MONTHLY_RETURNS}}
| {{MONTH}} | {{PORT_RET}}% | {{BENCH_RET}}% | {{MONTH_ALPHA}}% |
{{/MONTHLY_RETURNS}}

### Best/Worst Performers

**Top Performers**
| Symbol | Name | Return | Contribution |
|--------|------|--------|--------------|
{{#TOP_PERFORMERS}}
| {{SYMBOL}} | {{NAME}} | {{RETURN}}% | {{CONTRIB}}% |
{{/TOP_PERFORMERS}}

**Bottom Performers**
| Symbol | Name | Return | Contribution |
|--------|------|--------|--------------|
{{#BOTTOM_PERFORMERS}}
| {{SYMBOL}} | {{NAME}} | {{RETURN}}% | {{CONTRIB}}% |
{{/BOTTOM_PERFORMERS}}

---

## Risk Analysis

### Risk Metrics

| Metric | Portfolio | Benchmark |
|--------|-----------|-----------|
| Annualized Volatility | {{PORT_VOL}}% | {{BENCH_VOL}}% |
| Beta | {{BETA}} | 1.00 |
| Sharpe Ratio | {{SHARPE}} | {{BENCH_SHARPE}} |
| Sortino Ratio | {{SORTINO}} | {{BENCH_SORTINO}} |
| Calmar Ratio | {{CALMAR}} | {{BENCH_CALMAR}} |
| Information Ratio | {{INFO_RATIO}} | - |
| Tracking Error | {{TRACKING_ERROR}}% | - |

### Drawdown Analysis

| Metric | Value |
|--------|-------|
| Current Drawdown | {{CURRENT_DD}}% |
| Maximum Drawdown | {{MAX_DD}}% |
| Max DD Start Date | {{MAX_DD_START}} |
| Max DD End Date | {{MAX_DD_END}} |
| Recovery Date | {{MAX_DD_RECOVERY}} |
| Average Drawdown | {{AVG_DD}}% |
| Drawdown Duration | {{DD_DURATION}} days |

### Value at Risk (VaR)

| Confidence | 1-Day VaR | 10-Day VaR | Dollar Amount |
|------------|-----------|------------|---------------|
| 95% | {{VAR_95_1D}}% | {{VAR_95_10D}}% | {{VAR_95_DOLLAR}} |
| 99% | {{VAR_99_1D}}% | {{VAR_99_10D}}% | {{VAR_99_DOLLAR}} |

**Expected Shortfall (CVaR 95%)**: {{CVAR_95}}%

### Stress Testing

| Scenario | Impact |
|----------|--------|
| Market Crash (-20%) | {{STRESS_CRASH}}% |
| Rate Shock (+200bp) | {{STRESS_RATE}}% |
| Volatility Spike (VIX 80) | {{STRESS_VIX}}% |
| 2008 Financial Crisis | {{STRESS_2008}}% |
| 2020 COVID Crash | {{STRESS_2020}}% |

---

## Correlation Analysis

### Correlation Matrix

{{CORRELATION_MATRIX}}

### Diversification Score
**Score**: {{DIVERSIFICATION_SCORE}}/100

| Factor | Assessment |
|--------|------------|
| Number of Holdings | {{NUM_HOLDINGS}} |
| Sector Diversification | {{SECTOR_DIVERSITY}} |
| Geographic Diversification | {{GEO_DIVERSITY}} |
| Correlation Avg | {{CORR_AVG}} |

---

## Performance Attribution

### Attribution Summary

| Source | Contribution |
|--------|--------------|
| Asset Allocation | {{ATTR_ALLOCATION}}% |
| Security Selection | {{ATTR_SELECTION}}% |
| Interaction Effect | {{ATTR_INTERACTION}}% |
| **Total Alpha** | {{TOTAL_ALPHA}}% |

### Sector Attribution

| Sector | Weight Diff | Return Diff | Contribution |
|--------|-------------|-------------|--------------|
{{#SECTOR_ATTR}}
| {{SECTOR}} | {{WEIGHT_DIFF}}% | {{RET_DIFF}}% | {{CONTRIBUTION}}% |
{{/SECTOR_ATTR}}

---

## Transactions

### Recent Trades

| Date | Action | Symbol | Shares | Price | Value | Reason |
|------|--------|--------|--------|-------|-------|--------|
{{#TRANSACTIONS}}
| {{DATE}} | {{ACTION}} | {{SYMBOL}} | {{SHARES}} | {{PRICE}} | {{VALUE}} | {{REASON}} |
{{/TRANSACTIONS}}

### Turnover Analysis
| Metric | Value |
|--------|-------|
| Portfolio Turnover | {{TURNOVER}}% |
| Buy Value | {{BUY_VALUE}} |
| Sell Value | {{SELL_VALUE}} |
| Net Flow | {{NET_FLOW}} |

---

## Income Analysis

### Dividend Summary

| Metric | Value |
|--------|-------|
| Total Dividends Received | {{TOTAL_DIVIDENDS}} |
| Dividend Yield (Portfolio) | {{DIV_YIELD}}% |
| Dividend Growth (YoY) | {{DIV_GROWTH}}% |

### Dividend by Holding

| Symbol | Dividend/Share | Total Received | Yield |
|--------|----------------|----------------|-------|
{{#DIVIDEND_DETAIL}}
| {{SYMBOL}} | {{DIV_PER_SHARE}} | {{TOTAL_DIV}} | {{YIELD}}% |
{{/DIVIDEND_DETAIL}}

---

## Rebalancing Analysis

### Current vs Target Allocation

| Asset/Sector | Current | Target | Action Needed |
|--------------|---------|--------|---------------|
{{#REBALANCE}}
| {{ASSET}} | {{CURRENT}}% | {{TARGET}}% | {{ACTION}} |
{{/REBALANCE}}

### Recommended Trades for Rebalancing

| Action | Symbol | Shares | Est. Value | Reason |
|--------|--------|--------|------------|--------|
{{#REBAL_TRADES}}
| {{ACTION}} | {{SYMBOL}} | {{SHARES}} | {{VALUE}} | {{REASON}} |
{{/REBAL_TRADES}}

**Estimated Transaction Costs**: {{REBAL_COSTS}}

---

## Tax Considerations

### Realized Gains/Losses

| Category | Amount | Tax Rate | Est. Tax |
|----------|--------|----------|----------|
| Short-term Gains | {{ST_GAINS}} | {{ST_RATE}}% | {{ST_TAX}} |
| Short-term Losses | {{ST_LOSSES}} | - | - |
| Long-term Gains | {{LT_GAINS}} | {{LT_RATE}}% | {{LT_TAX}} |
| Long-term Losses | {{LT_LOSSES}} | - | - |
| **Net** | {{NET_GAINS}} | - | {{NET_TAX}} |

### Tax Loss Harvesting Opportunities

| Symbol | Unrealized Loss | Days Held | Potential Tax Savings |
|--------|-----------------|-----------|----------------------|
{{#TAX_HARVEST}}
| {{SYMBOL}} | {{LOSS}} | {{DAYS}} | {{SAVINGS}} |
{{/TAX_HARVEST}}

---

## Recommendations

### Action Items
{{#RECOMMENDATIONS}}
1. **{{REC_TITLE}}**: {{REC_DETAIL}}
{{/RECOMMENDATIONS}}

### Portfolio Optimization Suggestions
- {{OPT_1}}
- {{OPT_2}}
- {{OPT_3}}

### Risk Alerts
{{#ALERTS}}
- **{{ALERT_LEVEL}}**: {{ALERT_MESSAGE}}
{{/ALERTS}}

---

## Benchmark Comparison

**Benchmark**: {{BENCHMARK_NAME}} ({{BENCHMARK_TICKER}})

| Metric | Portfolio | Benchmark | Difference |
|--------|-----------|-----------|------------|
| Return | {{PORT_RET}}% | {{BENCH_RET}}% | {{RET_DIFF}}% |
| Volatility | {{PORT_VOL}}% | {{BENCH_VOL}}% | {{VOL_DIFF}}% |
| Sharpe | {{PORT_SHARPE}} | {{BENCH_SHARPE}} | {{SHARPE_DIFF}} |
| Max Drawdown | {{PORT_DD}}% | {{BENCH_DD}}% | {{DD_DIFF}}% |

---

## Appendix

### Methodology
- Returns calculated using time-weighted methodology
- Risk metrics based on {{RISK_LOOKBACK}} trading days
- Benchmark: {{BENCHMARK_NAME}}
- Currency: {{CURRENCY}}

### Data Sources
- Price Data: {{PRICE_SOURCE}}
- Benchmark Data: {{BENCHMARK_SOURCE}}
- Risk-free Rate: {{RF_RATE}}% ({{RF_SOURCE}})

---

## Disclaimer

This portfolio analysis is for informational purposes only and does not constitute financial advice. Past performance does not guarantee future results. Investment values can fluctuate, and investors may lose some or all of their principal.

**Report Generated**: {{TIMESTAMP}}
