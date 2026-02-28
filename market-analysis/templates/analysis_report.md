# {{ASSET_NAME}} 分析报告

**日期**: {{DATE}} | **市场**: {{MARKET}} | **数据来源**: {{PRICE_SOURCE}} ({{DATA_DELAY}})

---

## 结论 ← 先看这里

```
判断:  [强烈看多 / 看多 / 中性 / 看空 / 强烈看空]
信号强度: [强 / 中 / 弱]  置信度: {{CONFIDENCE}}%
时间周期: {{TIME_HORIZON}}  风险等级: {{RISK_LEVEL}}
```

| 关键价位 | 价格 |
|---------|------|
| 当前价格 | {{CURRENT_PRICE}} |
| 目标价（主要） | {{TARGET_PRICE_1}} |
| 目标价（乐观） | {{TARGET_PRICE_2}} |
| 止损位 | {{STOP_LOSS}} |
| 支撑位 | {{SUPPORT_1}} |
| 阻力位 | {{RESISTANCE_1}} |
| 风险/回报比 | {{RISK_REWARD}} |

**判断依据（3句话核心逻辑）**:
{{CORE_REASONING}}

**仓位建议**: 保守 {{POSITION_CONSERVATIVE}}% | 适中 {{POSITION_MODERATE}}% | 激进 {{POSITION_AGGRESSIVE}}%

---

## 主要风险

1. **{{RISK_1_CATEGORY}}**: {{RISK_1_DESCRIPTION}}
2. **{{RISK_2_CATEGORY}}**: {{RISK_2_DESCRIPTION}}
3. **{{RISK_3_CATEGORY}}**: {{RISK_3_DESCRIPTION}}

---

## 技术分析

### 趋势

| 指标 | 数值 | 信号 |
|------|------|------|
| SMA(20) | {{SMA_20}} | {{SMA_20_SIGNAL}} |
| SMA(50) | {{SMA_50}} | {{SMA_50_SIGNAL}} |
| SMA(200) | {{SMA_200}} | {{SMA_200_SIGNAL}} |

### 动量 & 波动

| 指标 | 数值 | 信号 |
|------|------|------|
| RSI(14) | {{RSI_14}} | {{RSI_SIGNAL}} |
| MACD | {{MACD}} | {{MACD_SIGNAL}} |
| 布林带位置 | {{BB_POSITION}} | {{BB_SIGNAL}} |
| ATR(14) | {{ATR_14}} | — |

### 技术评分

| 周期 | 评分 | 解读 |
|------|------|------|
| 短期(1-4周) | {{SCORE_SHORT}}/10 | {{INTERP_SHORT}} |
| 中期(1-3月) | {{SCORE_MEDIUM}}/10 | {{INTERP_MEDIUM}} |
| 长期(3-12月) | {{SCORE_LONG}}/10 | {{INTERP_LONG}} |

---

## 基本面（股票适用）

| 指标 | 数值 | 行业均值 | 评价 |
|------|------|---------|------|
| P/E | {{PE_RATIO}} | {{PE_INDUSTRY_AVG}} | {{PE_ASSESSMENT}} |
| Forward P/E | {{FORWARD_PE}} | — | — |
| P/B | {{PB_RATIO}} | {{PB_INDUSTRY_AVG}} | {{PB_ASSESSMENT}} |
| EV/EBITDA | {{EV_EBITDA}} | — | — |
| ROE | {{ROE}} | — | — |
| 营收增速(YoY) | {{REVENUE_GROWTH}} | — | — |
| 净利率 | {{NET_MARGIN}} | — | — |
| 债务/权益 | {{DEBT_EQUITY}} | — | — |
| 股息率 | {{DIVIDEND_YIELD}} | — | — |

---

## 市场情绪

| 指标 | 数值 | 状态 |
|------|------|------|
| 恐贪指数 | {{FEAR_GREED}} | {{FEAR_GREED_STATUS}} |
| VIX | {{VIX}} | {{VIX_STATUS}} |
| 分析师共识 | {{CONSENSUS}} | 目标价: {{TARGET_AVG}} |

---

## 近期新闻 & 事件

{{#NEWS_ITEMS}}
- **{{NEWS_DATE}}** {{NEWS_HEADLINE}} — *{{NEWS_SENTIMENT}}*
{{/NEWS_ITEMS}}

**即将到来的事件**:
{{#EVENTS}}
- **{{EVENT_DATE}}**: {{EVENT_DESCRIPTION}}
{{/EVENTS}}

---

## 市场数据（参考）

| | 数值 |
|-|------|
| 52周高点 | {{WEEK52_HIGH}} |
| 52周低点 | {{WEEK52_LOW}} |
| 今日涨跌 | {{PRICE_CHANGE}} ({{PRICE_CHANGE_PCT}}%) |
| 成交量 vs 均量 | {{VOLUME_VS_AVG}} |
| 市值 | {{MARKET_CAP}} |
| Beta | {{BETA}} |
| VaR(95%, 1日) | {{VAR_95}} |

---

> **免责声明**: 本报告仅供参考，不构成投资建议。投资有风险，入市需谨慎。过往表现不代表未来收益。
> 数据更新时间: {{TIMESTAMP}}
