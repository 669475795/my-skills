# IPO Analysis Report: {{COMPANY_NAME}}

**Stock Code**: {{STOCK_CODE}}
**Market**: {{MARKET}}
**Report Date**: {{DATE}}

---

## IPO Overview

| Field | Details |
|-------|---------|
| Company Name | {{COMPANY_NAME}} |
| Stock Code | {{STOCK_CODE}} |
| Exchange | {{EXCHANGE}} |
| Industry | {{INDUSTRY}} |
| Issue Price | {{ISSUE_PRICE}} |
| Issue Price Range | {{PRICE_RANGE}} |
| Shares Offered | {{SHARES_OFFERED}} |
| Funds Raised | {{FUNDS_RAISED}} |
| Market Cap at IPO | {{MARKET_CAP_IPO}} |

---

## Key Dates

| Event | Date | Status |
|-------|------|--------|
| Prospectus Filed | {{PROSPECTUS_DATE}} | {{PROSPECTUS_STATUS}} |
| Subscription Start | {{SUB_START}} | {{SUB_START_STATUS}} |
| Subscription End | {{SUB_END}} | {{SUB_END_STATUS}} |
| Allotment Date | {{ALLOTMENT_DATE}} | {{ALLOTMENT_STATUS}} |
| Listing Date | {{LISTING_DATE}} | {{LISTING_STATUS}} |
| Lock-up Expiry | {{LOCKUP_EXPIRY}} | - |

---

## Subscription Information

### Subscription Status
| Metric | Value |
|--------|-------|
| Public Subscription Rate | {{PUBLIC_SUB_RATE}}x |
| Institutional Subscription | {{INST_SUB_RATE}}x |
| Total Applications | {{TOTAL_APPLICATIONS}} |
| Application Amount | {{APPLICATION_AMOUNT}} |
| Expected Allotment Ratio | {{ALLOTMENT_RATIO}} |

### Lot Information (A-Share/HK)
| Field | Value |
|-------|-------|
| Lot Size | {{LOT_SIZE}} shares |
| Min Investment | {{MIN_INVESTMENT}} |
| Subscription Fee | {{SUB_FEE}} |

---

## IPO Scoring Model

### Overall Score: {{OVERALL_SCORE}}/100

| Factor | Weight | Score | Weighted |
|--------|--------|-------|----------|
| Valuation vs Industry | 30% | {{VAL_SCORE}}/100 | {{VAL_WEIGHTED}} |
| Subscription Demand | 20% | {{SUB_SCORE}}/100 | {{SUB_WEIGHTED}} |
| Market Sentiment | 15% | {{SENT_SCORE}}/100 | {{SENT_WEIGHTED}} |
| Underwriter Quality | 10% | {{UW_SCORE}}/100 | {{UW_WEIGHTED}} |
| Financials | 25% | {{FIN_SCORE}}/100 | {{FIN_WEIGHTED}} |

### Score Interpretation
| Score Range | Rating | Recommendation |
|-------------|--------|----------------|
| 80-100 | Excellent | Strong Subscribe |
| 60-79 | Good | Subscribe |
| 40-59 | Average | Neutral |
| 20-39 | Below Average | Avoid |
| 0-19 | Poor | Strong Avoid |

**Current Rating**: {{RATING}}

---

## Valuation Analysis

### Issue Valuation
| Metric | IPO | Industry Avg | Premium/Discount |
|--------|-----|--------------|------------------|
| P/E Ratio | {{IPO_PE}} | {{IND_PE}} | {{PE_PREMIUM}}% |
| P/S Ratio | {{IPO_PS}} | {{IND_PS}} | {{PS_PREMIUM}}% |
| P/B Ratio | {{IPO_PB}} | {{IND_PB}} | {{PB_PREMIUM}}% |
| EV/Revenue | {{IPO_EV_REV}} | {{IND_EV_REV}} | {{EV_PREMIUM}}% |

### Comparable Companies
| Company | Ticker | Market Cap | P/E | P/S |
|---------|--------|------------|-----|-----|
{{#COMPARABLES}}
| {{COMP_NAME}} | {{COMP_TICKER}} | {{COMP_MCAP}} | {{COMP_PE}} | {{COMP_PS}} |
{{/COMPARABLES}}

### Valuation Conclusion
{{VALUATION_CONCLUSION}}

---

## Financial Analysis

### Revenue & Growth
| Metric | FY-2 | FY-1 | Latest | YoY Growth |
|--------|------|------|--------|------------|
| Revenue | {{REV_FY2}} | {{REV_FY1}} | {{REV_LATEST}} | {{REV_GROWTH}}% |
| Gross Profit | {{GP_FY2}} | {{GP_FY1}} | {{GP_LATEST}} | {{GP_GROWTH}}% |
| Net Income | {{NI_FY2}} | {{NI_FY1}} | {{NI_LATEST}} | {{NI_GROWTH}}% |

### Profitability Margins
| Metric | FY-2 | FY-1 | Latest |
|--------|------|------|--------|
| Gross Margin | {{GM_FY2}}% | {{GM_FY1}}% | {{GM_LATEST}}% |
| Operating Margin | {{OM_FY2}}% | {{OM_FY1}}% | {{OM_LATEST}}% |
| Net Margin | {{NM_FY2}}% | {{NM_FY1}}% | {{NM_LATEST}}% |
| ROE | {{ROE_FY2}}% | {{ROE_FY1}}% | {{ROE_LATEST}}% |

### Balance Sheet Highlights
| Metric | Value |
|--------|-------|
| Total Assets | {{TOTAL_ASSETS}} |
| Total Liabilities | {{TOTAL_LIABILITIES}} |
| Shareholders Equity | {{EQUITY}} |
| Debt/Equity Ratio | {{DEBT_EQUITY}} |
| Current Ratio | {{CURRENT_RATIO}} |
| Cash & Equivalents | {{CASH}} |

---

## Use of Proceeds

| Purpose | Amount | Percentage |
|---------|--------|------------|
{{#PROCEEDS}}
| {{PROCEED_PURPOSE}} | {{PROCEED_AMOUNT}} | {{PROCEED_PCT}}% |
{{/PROCEEDS}}
| **Total** | {{TOTAL_PROCEEDS}} | 100% |

---

## Underwriter/Sponsor Analysis

### Lead Underwriter(s)
| Name | Role | Track Record |
|------|------|--------------|
{{#UNDERWRITERS}}
| {{UW_NAME}} | {{UW_ROLE}} | {{UW_TRACK}} |
{{/UNDERWRITERS}}

### Underwriter Performance (Last 20 IPOs)
| Metric | Value |
|--------|-------|
| Avg First Day Return | {{UW_AVG_RETURN}}% |
| Positive Return Rate | {{UW_POS_RATE}}% |
| Avg 30-Day Return | {{UW_30D_RETURN}}% |

---

## Cornerstone/Strategic Investors

{{#CORNERSTONE}}
| Investor | Investment | Lock-up Period |
|----------|------------|----------------|
| {{CS_NAME}} | {{CS_AMOUNT}} | {{CS_LOCKUP}} |
{{/CORNERSTONE}}

**Total Cornerstone Investment**: {{TOTAL_CORNERSTONE}}
**% of Offering**: {{CORNERSTONE_PCT}}%

---

## Risk Factors

### Key Risks
{{#RISKS}}
1. **{{RISK_TITLE}}**: {{RISK_DESCRIPTION}}
{{/RISKS}}

### Red Flags
{{#RED_FLAGS}}
- {{RED_FLAG}}
{{/RED_FLAGS}}

---

## Market Conditions

### Current Market Environment
| Indicator | Value | Status |
|-----------|-------|--------|
| Market Index ({{INDEX_NAME}}) | {{INDEX_VALUE}} | {{INDEX_TREND}} |
| Recent IPO Performance | {{RECENT_IPO_PERF}}% | {{IPO_MARKET_STATUS}} |
| Market Volatility | {{VOLATILITY}} | {{VOL_STATUS}} |
| Liquidity Conditions | {{LIQUIDITY}} | {{LIQ_STATUS}} |

### Sector Performance
| Sector | 1M Return | YTD Return |
|--------|-----------|------------|
| {{SECTOR}} | {{SECTOR_1M}}% | {{SECTOR_YTD}}% |

---

## First Day Return Prediction

### Predicted Range
| Scenario | Return | Price |
|----------|--------|-------|
| Bullish | {{PRED_BULL}}% | {{PRED_BULL_PRICE}} |
| Base Case | {{PRED_BASE}}% | {{PRED_BASE_PRICE}} |
| Bearish | {{PRED_BEAR}}% | {{PRED_BEAR_PRICE}} |

### Prediction Factors
{{PREDICTION_FACTORS}}

---

## Recommendation

### Summary
| Aspect | Assessment |
|--------|------------|
| **Overall Rating** | {{OVERALL_RATING}} |
| **Subscribe Recommendation** | {{SUBSCRIBE_REC}} |
| **Allocation Suggestion** | {{ALLOCATION_SUGGESTION}} |
| **Hold Period** | {{HOLD_PERIOD}} |

### Key Takeaways
{{#TAKEAWAYS}}
- {{TAKEAWAY}}
{{/TAKEAWAYS}}

### Action Items
{{#ACTIONS}}
1. {{ACTION}}
{{/ACTIONS}}

---

## Post-IPO Monitoring

### Key Dates to Watch
| Date | Event | Importance |
|------|-------|------------|
| {{LISTING_DATE}} | First Trading Day | High |
| {{LOCKUP_EXPIRY}} | Lock-up Expiry | High |
| {{FIRST_EARNINGS}} | First Earnings Report | High |

### Price Targets
| Timeframe | Target | Reasoning |
|-----------|--------|-----------|
| 1 Day | {{TARGET_1D}} | {{REASON_1D}} |
| 1 Week | {{TARGET_1W}} | {{REASON_1W}} |
| 1 Month | {{TARGET_1M}} | {{REASON_1M}} |

---

## Data Sources

- Prospectus: {{PROSPECTUS_SOURCE}}
- Financial Data: {{FINANCIAL_SOURCE}}
- Market Data: {{MARKET_SOURCE}}
- Industry Data: {{INDUSTRY_SOURCE}}

---

## Disclaimer

This IPO analysis is for informational purposes only and does not constitute a recommendation to subscribe, buy, or sell securities. IPO investments carry significant risks:

- IPO prices can be highly volatile
- Past IPO performance does not guarantee future results
- Lock-up expiry can cause significant price drops
- New companies have limited operating history
- Market conditions can change rapidly

**Always read the prospectus carefully before subscribing to any IPO. Consult a licensed financial advisor for personalized investment advice.**

**Report Generated**: {{TIMESTAMP}}
