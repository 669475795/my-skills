# Bond Analysis Guide

## Bond Fundamentals

### Key Terms
- **Face Value (Par)**: Amount paid at maturity (typically $1000)
- **Coupon Rate**: Annual interest rate on face value
- **Yield to Maturity (YTM)**: Total return if held to maturity
- **Current Yield**: Annual coupon / Current price
- **Duration**: Interest rate sensitivity
- **Convexity**: Curvature of price/yield relationship

### Price-Yield Relationship
- Bond prices move **inversely** to yields
- When rates rise → Bond prices fall
- When rates fall → Bond prices rise

## Yield Curve Analysis

### Curve Shapes
| Shape | Description | Economic Signal |
|-------|-------------|-----------------|
| Normal | Long > Short rates | Healthy growth expected |
| Flat | Long ≈ Short rates | Uncertainty, transition |
| Inverted | Long < Short rates | Recession warning |
| Steep | Large spread | Recovery, inflation expectations |

### Key Spreads
- **2Y-10Y Spread**: Most watched recession indicator
- **3M-10Y Spread**: Fed's preferred indicator
- **Credit Spread**: Corporate vs Treasury (risk appetite)

### Inversion Signals
Historically, 2Y-10Y inversion has preceded recessions by 6-24 months.

## Duration Analysis

### Macaulay Duration
Weighted average time to receive cash flows.
- Longer duration = More interest rate sensitivity
- Zero-coupon bonds have duration = maturity

### Modified Duration
Price sensitivity to yield changes:
```
ΔPrice ≈ -Modified Duration × ΔYield × Price
```

### Duration Rules
1. Higher coupon → Lower duration
2. Longer maturity → Higher duration
3. Higher yield → Lower duration

### Duration Categories
| Duration | Category | Rate Sensitivity |
|----------|----------|------------------|
| < 3 years | Short | Low |
| 3-7 years | Intermediate | Moderate |
| > 7 years | Long | High |

## Convexity

### Why It Matters
- Duration is a linear approximation
- Convexity captures the curvature
- Positive convexity benefits investors:
  - Prices rise more when rates fall
  - Prices fall less when rates rise

### Convexity Adjustment
```
ΔPrice ≈ -Duration × ΔYield + 0.5 × Convexity × (ΔYield)²
```

## Credit Analysis

### Credit Ratings
| Rating | Grade | Description |
|--------|-------|-------------|
| AAA | Investment | Highest quality |
| AA | Investment | High quality |
| A | Investment | Upper medium |
| BBB | Investment | Medium (lowest IG) |
| BB | High Yield | Speculative |
| B | High Yield | Highly speculative |
| CCC and below | Junk | Substantial risk |

### Credit Spreads
- **Investment Grade**: 50-200 bps over Treasury
- **High Yield**: 300-800+ bps over Treasury
- Spread widening = Risk-off sentiment
- Spread tightening = Risk-on sentiment

## Bond ETFs

### Treasury ETFs
| Ticker | Duration | Exposure |
|--------|----------|----------|
| BIL | Ultra-short | 1-3 month T-bills |
| SHY | Short | 1-3 year Treasury |
| IEF | Intermediate | 7-10 year Treasury |
| TLT | Long | 20+ year Treasury |

### Corporate ETFs
| Ticker | Category |
|--------|----------|
| LQD | Investment Grade Corporate |
| HYG | High Yield Corporate |
| VCSH | Short-term Corporate |

### Other Bond ETFs
| Ticker | Category |
|--------|----------|
| TIP | TIPS (Inflation Protected) |
| MUB | Municipal Bonds |
| EMB | Emerging Market Bonds |

## CLI Usage

```bash
# Price a bond
python bond_analysis.py price --face 1000 --coupon 0.05 --ytm 0.04 --years 10

# Calculate YTM
python bond_analysis.py ytm --face 1000 --coupon 0.05 --price 1050 --years 10

# Duration analysis
python bond_analysis.py duration --face 1000 --coupon 0.05 --ytm 0.04 --years 10

# Yield curve analysis
python bond_analysis.py curve

# Price sensitivity
python bond_analysis.py sensitivity --coupon 0.05 --ytm 0.04 --years 10 --yield-change 0.01
```

## Investment Strategies

### Laddering
- Buy bonds with staggered maturities
- Reduces reinvestment risk
- Provides regular liquidity

### Barbell
- Concentrate in short and long maturities
- Skip intermediate maturities
- Benefits from curve steepening

### Bullet
- Concentrate around target maturity
- Match liabilities
- Less reinvestment flexibility

## Risk Factors

1. **Interest Rate Risk**: Price sensitivity to rate changes
2. **Credit Risk**: Issuer default possibility
3. **Reinvestment Risk**: Uncertainty of coupon reinvestment rates
4. **Inflation Risk**: Purchasing power erosion
5. **Liquidity Risk**: Difficulty selling at fair price
6. **Call Risk**: Early redemption by issuer
