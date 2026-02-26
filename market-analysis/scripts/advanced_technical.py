#!/usr/bin/env python3
"""
Advanced Technical Analysis Module
Provides pattern recognition, Fibonacci analysis, pivot points, and support/resistance.
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install pandas numpy")
    sys.exit(1)

try:
    import yfinance as yf
except ImportError:
    yf = None


class AdvancedTechnicalAnalyzer:
    """
    Advanced Technical Analysis Engine

    Features:
    - Chart pattern recognition
    - Fibonacci retracement/extension
    - Pivot points (Standard, Fibonacci, Camarilla)
    - Support/Resistance detection
    - Ichimoku Cloud
    """

    def __init__(self):
        pass

    def calculate_fibonacci_levels(self, high: float, low: float,
                                   trend: str = 'up') -> Dict:
        """
        计算斐波那契回撤和扩展位

        Args:
            high: 最高价
            low: 最低价
            trend: 趋势方向 ('up', 'down')

        Returns:
            斐波那契水平
        """
        diff = high - low

        # Fibonacci ratios
        ratios = {
            '0.0': 0.0,
            '23.6': 0.236,
            '38.2': 0.382,
            '50.0': 0.5,
            '61.8': 0.618,
            '78.6': 0.786,
            '100.0': 1.0,
            '127.2': 1.272,
            '161.8': 1.618,
            '261.8': 2.618
        }

        levels = {}

        if trend == 'up':
            # Retracement levels from high
            for name, ratio in ratios.items():
                if ratio <= 1.0:
                    levels[f'retracement_{name}'] = round(high - (diff * ratio), 2)
                else:
                    levels[f'extension_{name}'] = round(high + (diff * (ratio - 1)), 2)
        else:
            # Retracement levels from low
            for name, ratio in ratios.items():
                if ratio <= 1.0:
                    levels[f'retracement_{name}'] = round(low + (diff * ratio), 2)
                else:
                    levels[f'extension_{name}'] = round(low - (diff * (ratio - 1)), 2)

        return {
            'high': high,
            'low': low,
            'range': round(diff, 2),
            'trend': trend,
            'levels': levels,
            'key_levels': {
                '38.2% retracement': levels.get('retracement_38.2'),
                '50.0% retracement': levels.get('retracement_50.0'),
                '61.8% retracement': levels.get('retracement_61.8'),
                '161.8% extension': levels.get('extension_161.8')
            }
        }

    def calculate_pivot_points(self, high: float, low: float, close: float,
                               method: str = 'standard') -> Dict:
        """
        计算枢轴点

        Args:
            high: 最高价
            low: 最低价
            close: 收盘价
            method: 计算方法 ('standard', 'fibonacci', 'camarilla', 'woodie')

        Returns:
            枢轴点水平
        """
        if method == 'standard':
            return self._standard_pivots(high, low, close)
        elif method == 'fibonacci':
            return self._fibonacci_pivots(high, low, close)
        elif method == 'camarilla':
            return self._camarilla_pivots(high, low, close)
        elif method == 'woodie':
            return self._woodie_pivots(high, low, close)
        else:
            return {'error': f'Unknown method: {method}'}

    def _standard_pivots(self, high: float, low: float, close: float) -> Dict:
        """标准枢轴点"""
        pivot = (high + low + close) / 3
        range_hl = high - low

        return {
            'method': 'standard',
            'pivot': round(pivot, 2),
            'r1': round(2 * pivot - low, 2),
            'r2': round(pivot + range_hl, 2),
            'r3': round(high + 2 * (pivot - low), 2),
            's1': round(2 * pivot - high, 2),
            's2': round(pivot - range_hl, 2),
            's3': round(low - 2 * (high - pivot), 2)
        }

    def _fibonacci_pivots(self, high: float, low: float, close: float) -> Dict:
        """斐波那契枢轴点"""
        pivot = (high + low + close) / 3
        range_hl = high - low

        return {
            'method': 'fibonacci',
            'pivot': round(pivot, 2),
            'r1': round(pivot + 0.382 * range_hl, 2),
            'r2': round(pivot + 0.618 * range_hl, 2),
            'r3': round(pivot + 1.000 * range_hl, 2),
            's1': round(pivot - 0.382 * range_hl, 2),
            's2': round(pivot - 0.618 * range_hl, 2),
            's3': round(pivot - 1.000 * range_hl, 2)
        }

    def _camarilla_pivots(self, high: float, low: float, close: float) -> Dict:
        """卡玛利拉枢轴点"""
        range_hl = high - low

        return {
            'method': 'camarilla',
            'pivot': round((high + low + close) / 3, 2),
            'r1': round(close + range_hl * 1.1 / 12, 2),
            'r2': round(close + range_hl * 1.1 / 6, 2),
            'r3': round(close + range_hl * 1.1 / 4, 2),
            'r4': round(close + range_hl * 1.1 / 2, 2),
            's1': round(close - range_hl * 1.1 / 12, 2),
            's2': round(close - range_hl * 1.1 / 6, 2),
            's3': round(close - range_hl * 1.1 / 4, 2),
            's4': round(close - range_hl * 1.1 / 2, 2)
        }

    def _woodie_pivots(self, high: float, low: float, close: float) -> Dict:
        """伍迪枢轴点"""
        pivot = (high + low + 2 * close) / 4
        range_hl = high - low

        return {
            'method': 'woodie',
            'pivot': round(pivot, 2),
            'r1': round(2 * pivot - low, 2),
            'r2': round(pivot + range_hl, 2),
            's1': round(2 * pivot - high, 2),
            's2': round(pivot - range_hl, 2)
        }

    def find_support_resistance(self, prices: pd.Series, window: int = 20,
                                num_levels: int = 5) -> Dict:
        """
        识别支撑和阻力位

        Args:
            prices: 价格序列
            window: 查找窗口
            num_levels: 返回水平数量

        Returns:
            支撑阻力位
        """
        if len(prices) < window * 2:
            return {'error': 'Insufficient data'}

        # Find local minima (support) and maxima (resistance)
        supports = []
        resistances = []

        for i in range(window, len(prices) - window):
            # Local minimum
            if prices.iloc[i] == prices.iloc[i-window:i+window].min():
                supports.append(prices.iloc[i])

            # Local maximum
            if prices.iloc[i] == prices.iloc[i-window:i+window].max():
                resistances.append(prices.iloc[i])

        # Cluster nearby levels
        support_levels = self._cluster_levels(supports, num_levels)
        resistance_levels = self._cluster_levels(resistances, num_levels)

        current_price = prices.iloc[-1]

        return {
            'current_price': round(current_price, 2),
            'support_levels': [round(s, 2) for s in sorted(support_levels, reverse=True)],
            'resistance_levels': [round(r, 2) for r in sorted(resistance_levels)],
            'nearest_support': round(max([s for s in support_levels if s < current_price], default=0), 2),
            'nearest_resistance': round(min([r for r in resistance_levels if r > current_price], default=0), 2)
        }

    def _cluster_levels(self, levels: List[float], num_clusters: int) -> List[float]:
        """聚类价格水平"""
        if not levels:
            return []

        # Simple clustering by proximity
        levels = sorted(levels)
        clusters = []
        current_cluster = [levels[0]]

        threshold = (max(levels) - min(levels)) * 0.02  # 2% threshold

        for level in levels[1:]:
            if level - current_cluster[-1] < threshold:
                current_cluster.append(level)
            else:
                clusters.append(np.mean(current_cluster))
                current_cluster = [level]

        clusters.append(np.mean(current_cluster))

        # Return top clusters by frequency (simplified)
        return clusters[:num_clusters]

    def detect_patterns(self, data: pd.DataFrame) -> Dict:
        """
        检测图表形态

        Args:
            data: OHLCV数据

        Returns:
            检测到的形态
        """
        patterns = []

        # Double Top/Bottom detection
        dt_result = self._detect_double_top_bottom(data)
        if dt_result:
            patterns.append(dt_result)

        # Head and Shoulders detection
        hs_result = self._detect_head_shoulders(data)
        if hs_result:
            patterns.append(hs_result)

        # Triangle detection
        tri_result = self._detect_triangle(data)
        if tri_result:
            patterns.append(tri_result)

        # Candlestick patterns
        candle_patterns = self._detect_candlestick_patterns(data)
        patterns.extend(candle_patterns)

        return {
            'patterns_found': len(patterns),
            'patterns': patterns,
            'timestamp': datetime.now().isoformat()
        }

    def _detect_double_top_bottom(self, data: pd.DataFrame) -> Optional[Dict]:
        """检测双顶/双底"""
        if len(data) < 50:
            return None

        highs = data['High'].values
        lows = data['Low'].values

        # Simplified double top detection
        # Look for two peaks within 5% of each other
        recent_highs = []
        for i in range(10, len(highs) - 10):
            if highs[i] == max(highs[i-10:i+10]):
                recent_highs.append((i, highs[i]))

        if len(recent_highs) >= 2:
            for i in range(len(recent_highs) - 1):
                for j in range(i + 1, len(recent_highs)):
                    idx1, h1 = recent_highs[i]
                    idx2, h2 = recent_highs[j]

                    if abs(h1 - h2) / h1 < 0.03:  # Within 3%
                        if idx2 - idx1 > 20:  # At least 20 bars apart
                            return {
                                'pattern': 'Double Top',
                                'type': 'bearish',
                                'peak1': round(h1, 2),
                                'peak2': round(h2, 2),
                                'confidence': 'medium'
                            }

        return None

    def _detect_head_shoulders(self, data: pd.DataFrame) -> Optional[Dict]:
        """检测头肩顶/底"""
        # Simplified - would need more sophisticated analysis
        return None

    def _detect_triangle(self, data: pd.DataFrame) -> Optional[Dict]:
        """检测三角形态"""
        if len(data) < 30:
            return None

        recent = data.tail(30)

        # Check for converging highs and lows
        highs = recent['High'].values
        lows = recent['Low'].values

        # Linear regression on highs and lows
        x = np.arange(len(highs))

        high_slope = np.polyfit(x, highs, 1)[0]
        low_slope = np.polyfit(x, lows, 1)[0]

        if high_slope < 0 and low_slope > 0:
            return {
                'pattern': 'Symmetrical Triangle',
                'type': 'neutral',
                'high_slope': round(high_slope, 4),
                'low_slope': round(low_slope, 4),
                'confidence': 'medium'
            }
        elif high_slope < 0 and abs(low_slope) < 0.01:
            return {
                'pattern': 'Descending Triangle',
                'type': 'bearish',
                'confidence': 'medium'
            }
        elif abs(high_slope) < 0.01 and low_slope > 0:
            return {
                'pattern': 'Ascending Triangle',
                'type': 'bullish',
                'confidence': 'medium'
            }

        return None

    def _detect_candlestick_patterns(self, data: pd.DataFrame) -> List[Dict]:
        """检测K线形态"""
        patterns = []

        if len(data) < 3:
            return patterns

        # Last 3 candles
        c1 = data.iloc[-3]  # Oldest
        c2 = data.iloc[-2]
        c3 = data.iloc[-1]  # Most recent

        # Doji detection
        body3 = abs(c3['Close'] - c3['Open'])
        range3 = c3['High'] - c3['Low']

        if range3 > 0 and body3 / range3 < 0.1:
            patterns.append({
                'pattern': 'Doji',
                'type': 'neutral',
                'bar': -1,
                'confidence': 'high'
            })

        # Hammer/Hanging Man
        upper_shadow = c3['High'] - max(c3['Open'], c3['Close'])
        lower_shadow = min(c3['Open'], c3['Close']) - c3['Low']

        if lower_shadow > body3 * 2 and upper_shadow < body3 * 0.5:
            # Determine if hammer or hanging man based on trend
            if c3['Close'] < data['Close'].iloc[-10:-1].mean():
                patterns.append({
                    'pattern': 'Hammer',
                    'type': 'bullish',
                    'bar': -1,
                    'confidence': 'medium'
                })

        # Engulfing patterns
        if c2['Close'] < c2['Open'] and c3['Close'] > c3['Open']:
            if c3['Open'] < c2['Close'] and c3['Close'] > c2['Open']:
                patterns.append({
                    'pattern': 'Bullish Engulfing',
                    'type': 'bullish',
                    'bar': -1,
                    'confidence': 'high'
                })

        if c2['Close'] > c2['Open'] and c3['Close'] < c3['Open']:
            if c3['Open'] > c2['Close'] and c3['Close'] < c2['Open']:
                patterns.append({
                    'pattern': 'Bearish Engulfing',
                    'type': 'bearish',
                    'bar': -1,
                    'confidence': 'high'
                })

        return patterns

    def calculate_ichimoku(self, data: pd.DataFrame) -> Dict:
        """
        计算一目均衡表

        Args:
            data: OHLCV数据

        Returns:
            一目均衡表指标
        """
        if len(data) < 52:
            return {'error': 'Insufficient data (need 52+ bars)'}

        high = data['High']
        low = data['Low']
        close = data['Close']

        # Tenkan-sen (Conversion Line): (9-period high + 9-period low) / 2
        tenkan = (high.rolling(9).max() + low.rolling(9).min()) / 2

        # Kijun-sen (Base Line): (26-period high + 26-period low) / 2
        kijun = (high.rolling(26).max() + low.rolling(26).min()) / 2

        # Senkou Span A (Leading Span A): (Tenkan + Kijun) / 2, plotted 26 periods ahead
        senkou_a = ((tenkan + kijun) / 2).shift(26)

        # Senkou Span B (Leading Span B): (52-period high + 52-period low) / 2, plotted 26 periods ahead
        senkou_b = ((high.rolling(52).max() + low.rolling(52).min()) / 2).shift(26)

        # Chikou Span (Lagging Span): Close plotted 26 periods behind
        chikou = close.shift(-26)

        current_price = close.iloc[-1]
        current_tenkan = tenkan.iloc[-1]
        current_kijun = kijun.iloc[-1]
        current_senkou_a = senkou_a.iloc[-27] if len(senkou_a) > 27 else None
        current_senkou_b = senkou_b.iloc[-27] if len(senkou_b) > 27 else None

        # Determine cloud color and trend
        cloud_color = 'green' if current_senkou_a and current_senkou_b and current_senkou_a > current_senkou_b else 'red'

        # Signal analysis
        signals = []

        if current_price > current_tenkan and current_tenkan > current_kijun:
            signals.append('Bullish: Price above Tenkan above Kijun')
        elif current_price < current_tenkan and current_tenkan < current_kijun:
            signals.append('Bearish: Price below Tenkan below Kijun')

        if current_senkou_a and current_senkou_b:
            cloud_top = max(current_senkou_a, current_senkou_b)
            cloud_bottom = min(current_senkou_a, current_senkou_b)

            if current_price > cloud_top:
                signals.append('Price above cloud (bullish)')
            elif current_price < cloud_bottom:
                signals.append('Price below cloud (bearish)')
            else:
                signals.append('Price inside cloud (consolidation)')

        return {
            'current_price': round(current_price, 2),
            'tenkan_sen': round(current_tenkan, 2),
            'kijun_sen': round(current_kijun, 2),
            'senkou_span_a': round(current_senkou_a, 2) if current_senkou_a else None,
            'senkou_span_b': round(current_senkou_b, 2) if current_senkou_b else None,
            'cloud_color': cloud_color,
            'signals': signals,
            'overall_trend': 'bullish' if len([s for s in signals if 'bullish' in s.lower()]) > len([s for s in signals if 'bearish' in s.lower()]) else 'bearish'
        }


def main():
    parser = argparse.ArgumentParser(description="Advanced Technical Analysis")
    parser.add_argument("ticker", nargs='?', help="Stock ticker")
    parser.add_argument("--fibonacci", action="store_true", help="Calculate Fibonacci levels")
    parser.add_argument("--high", type=float, help="High price for Fibonacci")
    parser.add_argument("--low", type=float, help="Low price for Fibonacci")
    parser.add_argument("--trend", choices=["up", "down"], default="up", help="Trend direction")
    parser.add_argument("--pivots", action="store_true", help="Calculate pivot points")
    parser.add_argument("--pivot-method", default="standard",
                       choices=["standard", "fibonacci", "camarilla", "woodie"])
    parser.add_argument("--patterns", action="store_true", help="Detect chart patterns")
    parser.add_argument("--support-resistance", action="store_true", help="Find S/R levels")
    parser.add_argument("--ichimoku", action="store_true", help="Calculate Ichimoku")
    parser.add_argument("--period", default="6mo", help="Data period")
    parser.add_argument("--output", choices=["json", "text"], default="text")

    args = parser.parse_args()

    analyzer = AdvancedTechnicalAnalyzer()

    if args.fibonacci:
        if not args.high or not args.low:
            print("Error: --high and --low required for Fibonacci")
            sys.exit(1)
        data = analyzer.calculate_fibonacci_levels(args.high, args.low, args.trend)

    elif args.pivots:
        if not args.ticker and (not args.high or not args.low):
            print("Error: --ticker or (--high and --low) required")
            sys.exit(1)

        if args.ticker and yf:
            t = yf.Ticker(args.ticker)
            hist = t.history(period='2d')
            if not hist.empty:
                yesterday = hist.iloc[-2] if len(hist) > 1 else hist.iloc[-1]
                data = analyzer.calculate_pivot_points(
                    yesterday['High'], yesterday['Low'], yesterday['Close'],
                    args.pivot_method
                )
            else:
                data = {'error': 'No data'}
        else:
            data = {'error': 'Ticker required'}

    elif args.ticker and yf:
        t = yf.Ticker(args.ticker)
        hist = t.history(period=args.period)

        if args.patterns:
            data = analyzer.detect_patterns(hist)
        elif args.support_resistance:
            data = analyzer.find_support_resistance(hist['Close'])
        elif args.ichimoku:
            data = analyzer.calculate_ichimoku(hist)
        else:
            # Default: show all
            data = {
                'patterns': analyzer.detect_patterns(hist),
                'support_resistance': analyzer.find_support_resistance(hist['Close']),
                'ichimoku': analyzer.calculate_ichimoku(hist)
            }
    else:
        print("Error: --ticker required")
        sys.exit(1)

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2, default=str))
    else:
        print(f"\n=== Advanced Technical Analysis ===\n")
        for k, v in data.items():
            if isinstance(v, dict):
                print(f"\n{k}:")
                for k2, v2 in v.items():
                    print(f"  {k2}: {v2}")
            elif isinstance(v, list):
                print(f"\n{k}:")
                for item in v:
                    print(f"  - {item}")
            else:
                print(f"{k}: {v}")


if __name__ == "__main__":
    main()
