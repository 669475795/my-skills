#!/usr/bin/env python3
"""
Sentiment Analysis Module for Market Analysis
Provides fear/greed index, VIX analysis, put/call ratio, and market breadth.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

try:
    import yfinance as yf
    import pandas as pd
    import numpy as np
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install yfinance pandas numpy")
    sys.exit(1)


class SentimentAnalyzer:
    """
    Market Sentiment Analysis Engine

    Features:
    - Fear & Greed Index calculation
    - VIX analysis
    - Put/Call ratio
    - Market breadth indicators
    - Sector rotation analysis
    """

    def __init__(self):
        pass

    def get_fear_greed_index(self) -> Dict:
        """
        计算恐惧与贪婪指数

        Components:
        - VIX level
        - Market momentum
        - Stock price breadth
        - Put/Call ratio
        - Junk bond demand
        - Safe haven demand

        Returns:
            恐惧贪婪指数
        """
        components = {}

        # 1. VIX (Fear Index)
        vix_score = self._get_vix_component()
        components['vix'] = vix_score

        # 2. Market Momentum (S&P 500 vs 125-day MA)
        momentum_score = self._get_momentum_component()
        components['momentum'] = momentum_score

        # 3. Stock Price Strength (52-week highs vs lows)
        strength_score = self._get_strength_component()
        components['price_strength'] = strength_score

        # 4. Put/Call Ratio
        pcr_score = self._get_pcr_component()
        components['put_call_ratio'] = pcr_score

        # 5. Safe Haven Demand (Bonds vs Stocks)
        haven_score = self._get_safe_haven_component()
        components['safe_haven_demand'] = haven_score

        # Calculate composite index (0 = Extreme Fear, 100 = Extreme Greed)
        valid_scores = [v['score'] for v in components.values() if v.get('score') is not None]
        composite_score = np.mean(valid_scores) if valid_scores else 50

        return {
            'index': round(composite_score, 1),
            'classification': self._classify_sentiment(composite_score),
            'components': components,
            'timestamp': datetime.now().isoformat(),
            'interpretation': self._interpret_fear_greed(composite_score)
        }

    def _get_vix_component(self) -> Dict:
        """VIX组成部分"""
        try:
            vix = yf.Ticker('^VIX')
            hist = vix.history(period='1mo')

            if hist.empty:
                return {'score': None, 'error': 'No VIX data'}

            current = hist['Close'].iloc[-1]
            avg_50d = hist['Close'].mean()

            # Lower VIX = higher score (more greed)
            if current < 12:
                score = 95
            elif current < 15:
                score = 80
            elif current < 20:
                score = 60
            elif current < 25:
                score = 40
            elif current < 30:
                score = 20
            else:
                score = 5

            return {
                'score': score,
                'current_vix': round(current, 2),
                '30d_avg': round(avg_50d, 2),
                'interpretation': 'Low fear' if current < 20 else 'Elevated fear'
            }

        except Exception as e:
            return {'score': None, 'error': str(e)}

    def _get_momentum_component(self) -> Dict:
        """市场动量组成部分"""
        try:
            spy = yf.Ticker('SPY')
            hist = spy.history(period='6mo')

            if len(hist) < 125:
                return {'score': None, 'error': 'Insufficient data'}

            current = hist['Close'].iloc[-1]
            ma_125 = hist['Close'].rolling(125).mean().iloc[-1]

            # Higher price vs MA = more greed
            diff_pct = ((current / ma_125) - 1) * 100

            if diff_pct > 10:
                score = 95
            elif diff_pct > 5:
                score = 75
            elif diff_pct > 0:
                score = 55
            elif diff_pct > -5:
                score = 35
            else:
                score = 15

            return {
                'score': score,
                'current_price': round(current, 2),
                'ma_125': round(ma_125, 2),
                'diff_percent': round(diff_pct, 2),
                'interpretation': 'Bullish momentum' if diff_pct > 0 else 'Bearish momentum'
            }

        except Exception as e:
            return {'score': None, 'error': str(e)}

    def _get_strength_component(self) -> Dict:
        """股价强度组成部分"""
        # Simplified: use SPY 52-week position
        try:
            spy = yf.Ticker('SPY')
            hist = spy.history(period='1y')

            if len(hist) < 250:
                return {'score': None, 'error': 'Insufficient data'}

            current = hist['Close'].iloc[-1]
            high_52w = hist['High'].max()
            low_52w = hist['Low'].min()

            # Position within 52-week range
            range_position = (current - low_52w) / (high_52w - low_52w)
            score = range_position * 100

            return {
                'score': round(score, 1),
                'current': round(current, 2),
                '52w_high': round(high_52w, 2),
                '52w_low': round(low_52w, 2),
                'interpretation': 'Near highs' if score > 70 else 'Near lows' if score < 30 else 'Mid range'
            }

        except Exception as e:
            return {'score': None, 'error': str(e)}

    def _get_pcr_component(self) -> Dict:
        """看跌看涨比组成部分"""
        # Use CBOE data approximation
        try:
            # Get SPY options as proxy
            spy = yf.Ticker('SPY')
            expirations = spy.options

            if not expirations:
                return {'score': 50, 'note': 'Using default'}

            # Get nearest expiration
            opt = spy.option_chain(expirations[0])

            call_oi = opt.calls['openInterest'].sum()
            put_oi = opt.puts['openInterest'].sum()

            pcr = put_oi / call_oi if call_oi > 0 else 1

            # Lower PCR = more greed (more calls than puts)
            if pcr < 0.6:
                score = 90
            elif pcr < 0.8:
                score = 70
            elif pcr < 1.0:
                score = 50
            elif pcr < 1.2:
                score = 30
            else:
                score = 10

            return {
                'score': score,
                'put_call_ratio': round(pcr, 3),
                'call_oi': int(call_oi),
                'put_oi': int(put_oi),
                'interpretation': 'Bullish' if pcr < 0.8 else 'Bearish' if pcr > 1.0 else 'Neutral'
            }

        except Exception as e:
            return {'score': 50, 'error': str(e)}

    def _get_safe_haven_component(self) -> Dict:
        """避险需求组成部分"""
        try:
            # Compare TLT (bonds) vs SPY (stocks) performance
            tlt = yf.Ticker('TLT')
            spy = yf.Ticker('SPY')

            tlt_hist = tlt.history(period='1mo')
            spy_hist = spy.history(period='1mo')

            if tlt_hist.empty or spy_hist.empty:
                return {'score': 50, 'note': 'Insufficient data'}

            tlt_return = (tlt_hist['Close'].iloc[-1] / tlt_hist['Close'].iloc[0] - 1) * 100
            spy_return = (spy_hist['Close'].iloc[-1] / spy_hist['Close'].iloc[0] - 1) * 100

            # If stocks outperforming bonds = greed
            diff = spy_return - tlt_return

            if diff > 5:
                score = 85
            elif diff > 2:
                score = 70
            elif diff > -2:
                score = 50
            elif diff > -5:
                score = 30
            else:
                score = 15

            return {
                'score': score,
                'stock_return_1m': round(spy_return, 2),
                'bond_return_1m': round(tlt_return, 2),
                'interpretation': 'Risk-on' if diff > 2 else 'Risk-off' if diff < -2 else 'Neutral'
            }

        except Exception as e:
            return {'score': 50, 'error': str(e)}

    def _classify_sentiment(self, score: float) -> str:
        """分类市场情绪"""
        if score >= 75:
            return 'Extreme Greed'
        elif score >= 55:
            return 'Greed'
        elif score >= 45:
            return 'Neutral'
        elif score >= 25:
            return 'Fear'
        else:
            return 'Extreme Fear'

    def _interpret_fear_greed(self, score: float) -> str:
        """解读恐惧贪婪指数"""
        if score >= 75:
            return 'Market may be overextended. Consider defensive positioning.'
        elif score >= 55:
            return 'Optimism is high. Normal bull market conditions.'
        elif score >= 45:
            return 'Balanced sentiment. No strong directional bias.'
        elif score >= 25:
            return 'Elevated fear. Potential buying opportunities for long-term investors.'
        else:
            return 'Extreme fear. Historically good buying opportunities, but exercise caution.'

    def get_vix_analysis(self) -> Dict:
        """
        深度VIX分析

        Returns:
            VIX分析结果
        """
        try:
            vix = yf.Ticker('^VIX')
            hist = vix.history(period='1y')

            if hist.empty:
                return {'error': 'No VIX data'}

            current = hist['Close'].iloc[-1]

            # Calculate percentile
            percentile = (hist['Close'] < current).sum() / len(hist) * 100

            # Calculate term structure if available
            vix3m = yf.Ticker('^VIX3M')
            vix3m_hist = vix3m.history(period='5d')

            term_structure = None
            if not vix3m_hist.empty:
                vix3m_current = vix3m_hist['Close'].iloc[-1]
                term_structure = {
                    'vix_1m': round(current, 2),
                    'vix_3m': round(vix3m_current, 2),
                    'contango': vix3m_current > current,
                    'spread': round(vix3m_current - current, 2)
                }

            return {
                'current_vix': round(current, 2),
                'percentile_1y': round(percentile, 1),
                'statistics': {
                    '1y_mean': round(hist['Close'].mean(), 2),
                    '1y_median': round(hist['Close'].median(), 2),
                    '1y_high': round(hist['High'].max(), 2),
                    '1y_low': round(hist['Low'].min(), 2),
                    'std_dev': round(hist['Close'].std(), 2)
                },
                'term_structure': term_structure,
                'level_interpretation': self._interpret_vix_level(current),
                'historical_context': self._vix_historical_context(current)
            }

        except Exception as e:
            return {'error': str(e)}

    def _interpret_vix_level(self, vix: float) -> str:
        """解读VIX水平"""
        if vix < 12:
            return 'Extremely low - Complacency'
        elif vix < 15:
            return 'Low - Calm markets'
        elif vix < 20:
            return 'Normal range'
        elif vix < 25:
            return 'Elevated - Increasing uncertainty'
        elif vix < 30:
            return 'High - Significant fear'
        elif vix < 40:
            return 'Very high - Major stress'
        else:
            return 'Extreme - Crisis levels'

    def _vix_historical_context(self, vix: float) -> str:
        """VIX历史背景"""
        if vix < 15:
            return 'Below long-term average. Historically, low VIX periods precede increased volatility.'
        elif vix < 25:
            return 'Near historical average. Normal market uncertainty.'
        else:
            return 'Above average. Historically, elevated VIX eventually mean-reverts lower.'

    def get_market_breadth(self) -> Dict:
        """
        获取市场宽度指标

        Returns:
            市场宽度数据
        """
        # Use major indices as proxy
        indices = {
            'S&P 500': 'SPY',
            'Dow Jones': 'DIA',
            'NASDAQ 100': 'QQQ',
            'Russell 2000': 'IWM'
        }

        breadth = {}

        for name, ticker in indices.items():
            try:
                t = yf.Ticker(ticker)
                hist = t.history(period='1mo')

                if not hist.empty:
                    current = hist['Close'].iloc[-1]
                    ma_20 = hist['Close'].rolling(20).mean().iloc[-1]
                    month_return = (current / hist['Close'].iloc[0] - 1) * 100

                    breadth[name] = {
                        'current': round(current, 2),
                        'above_ma20': current > ma_20,
                        'month_return': round(month_return, 2)
                    }
            except Exception:
                continue

        # Calculate breadth score
        above_ma_count = sum(1 for v in breadth.values() if v.get('above_ma20', False))
        breadth_score = above_ma_count / len(breadth) * 100 if breadth else 50

        return {
            'indices': breadth,
            'breadth_score': round(breadth_score, 1),
            'interpretation': 'Broad participation' if breadth_score > 75 else 'Narrow leadership' if breadth_score < 25 else 'Mixed'
        }

    def get_sector_rotation(self) -> Dict:
        """
        获取板块轮动分析

        Returns:
            板块轮动数据
        """
        sectors = {
            'Technology': 'XLK',
            'Healthcare': 'XLV',
            'Financials': 'XLF',
            'Consumer Discretionary': 'XLY',
            'Consumer Staples': 'XLP',
            'Energy': 'XLE',
            'Utilities': 'XLU',
            'Real Estate': 'XLRE',
            'Materials': 'XLB',
            'Industrials': 'XLI',
            'Communication': 'XLC'
        }

        sector_data = []

        for name, ticker in sectors.items():
            try:
                t = yf.Ticker(ticker)
                hist = t.history(period='1mo')

                if not hist.empty:
                    month_return = (hist['Close'].iloc[-1] / hist['Close'].iloc[0] - 1) * 100
                    sector_data.append({
                        'sector': name,
                        'ticker': ticker,
                        'month_return': round(month_return, 2)
                    })
            except Exception:
                continue

        # Sort by performance
        sector_data.sort(key=lambda x: x['month_return'], reverse=True)

        # Analyze rotation pattern
        leaders = [s['sector'] for s in sector_data[:3]]
        laggards = [s['sector'] for s in sector_data[-3:]]

        cycle_phase = self._identify_cycle_phase(leaders, laggards)

        return {
            'sectors': sector_data,
            'leaders': leaders,
            'laggards': laggards,
            'cycle_phase': cycle_phase,
            'timestamp': datetime.now().isoformat()
        }

    def _identify_cycle_phase(self, leaders: List[str], laggards: List[str]) -> str:
        """识别周期阶段"""
        # Simplified cycle analysis
        defensive = {'Consumer Staples', 'Utilities', 'Healthcare'}
        cyclical = {'Consumer Discretionary', 'Financials', 'Industrials', 'Materials'}
        growth = {'Technology', 'Communication'}

        leaders_set = set(leaders)

        if leaders_set & defensive:
            return 'Late Cycle / Defensive - Rotating to defensive sectors'
        elif leaders_set & cyclical:
            return 'Early/Mid Cycle - Cyclical leadership'
        elif leaders_set & growth:
            return 'Growth Phase - Technology/Growth leading'
        else:
            return 'Mixed signals - No clear rotation pattern'


def main():
    parser = argparse.ArgumentParser(description="Market Sentiment Analysis")
    parser.add_argument("action", nargs='?', choices=["fear-greed", "vix", "breadth", "sectors", "all"],
                       default="fear-greed", help="Analysis type")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format")

    args = parser.parse_args()

    analyzer = SentimentAnalyzer()

    if args.action == "fear-greed":
        data = analyzer.get_fear_greed_index()
    elif args.action == "vix":
        data = analyzer.get_vix_analysis()
    elif args.action == "breadth":
        data = analyzer.get_market_breadth()
    elif args.action == "sectors":
        data = analyzer.get_sector_rotation()
    elif args.action == "all":
        data = {
            'fear_greed': analyzer.get_fear_greed_index(),
            'vix': analyzer.get_vix_analysis(),
            'breadth': analyzer.get_market_breadth(),
            'sectors': analyzer.get_sector_rotation()
        }

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2, default=str))
    else:
        if args.action == "fear-greed":
            print("\n=== Fear & Greed Index ===\n")
            print(f"Index: {data.get('index', 'N/A')}")
            print(f"Classification: {data.get('classification', 'N/A')}")
            print(f"\n{data.get('interpretation', '')}")

            print("\nComponents:")
            for name, info in data.get('components', {}).items():
                if isinstance(info, dict):
                    print(f"  {name}: {info.get('score', 'N/A')} - {info.get('interpretation', '')}")

        elif args.action == "vix":
            print("\n=== VIX Analysis ===\n")
            print(f"Current VIX: {data.get('current_vix', 'N/A')}")
            print(f"1Y Percentile: {data.get('percentile_1y', 'N/A')}%")
            print(f"\n{data.get('level_interpretation', '')}")

        elif args.action == "sectors":
            print("\n=== Sector Rotation ===\n")
            for sector in data.get('sectors', [])[:5]:
                print(f"{sector['sector']}: {sector['month_return']:+.2f}%")
            print(f"\nCycle Phase: {data.get('cycle_phase', 'N/A')}")

        else:
            print(json.dumps(data, indent=2, default=str))


if __name__ == "__main__":
    main()
