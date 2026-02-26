#!/usr/bin/env python3
"""
Bond Data Fetcher for Market Analysis
Fetches government bonds, corporate bonds, yield curves, and credit spreads.
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

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
try:
    from china_data_sources import get_china_source
except ImportError:
    get_china_source = None


class BondDataFetcher:
    """
    Fetcher for bond market data.

    Covers:
    - US Treasury yields
    - China government bonds
    - Yield curves
    - Credit spreads
    - Bond ETFs
    """

    # US Treasury yield tickers (Yahoo Finance)
    US_TREASURY_TICKERS = {
        '1m': '^IRX',      # 13-week T-Bill
        '3m': '^IRX',      # 3-month
        '6m': None,        # Not directly available
        '1y': None,
        '2y': '^FVX',      # Approximation
        '5y': '^FVX',      # 5-year
        '10y': '^TNX',     # 10-year
        '30y': '^TYX'      # 30-year
    }

    # Bond ETF tickers
    BOND_ETFS = {
        'treasury': ['TLT', 'IEF', 'SHY', 'BIL', 'GOVT'],
        'corporate': ['LQD', 'VCIT', 'VCSH'],
        'high_yield': ['HYG', 'JNK', 'SHYG'],
        'tips': ['TIP', 'VTIP', 'STIP'],
        'muni': ['MUB', 'VTEB', 'HYD'],
        'international': ['BNDX', 'EMB', 'VWOB']
    }

    def __init__(self):
        self.china_source = get_china_source() if get_china_source else None
        self.session = None

    def get_us_treasury_yields(self) -> Dict:
        """
        获取美国国债收益率

        Returns:
            各期限收益率数据
        """
        yields = {}

        for maturity, ticker in self.US_TREASURY_TICKERS.items():
            if ticker:
                try:
                    t = yf.Ticker(ticker)
                    hist = t.history(period='5d')
                    if not hist.empty:
                        current = hist['Close'].iloc[-1]
                        previous = hist['Close'].iloc[-2] if len(hist) > 1 else current

                        yields[maturity] = {
                            'yield': round(current, 3),
                            'change': round(current - previous, 3),
                            'date': hist.index[-1].strftime('%Y-%m-%d')
                        }
                except Exception as e:
                    continue

        yields['source'] = 'yahoo_finance'
        yields['timestamp'] = datetime.now().isoformat()

        return yields

    def get_yield_curve(self, country: str = 'US') -> Dict:
        """
        获取收益率曲线

        Args:
            country: 国家 ('US', 'CN')

        Returns:
            收益率曲线数据
        """
        if country == 'US':
            return self._get_us_yield_curve()
        elif country == 'CN':
            return self._get_china_yield_curve()
        else:
            return {'error': f'Unsupported country: {country}'}

    def _get_us_yield_curve(self) -> Dict:
        """获取美国收益率曲线"""
        maturities = ['1m', '3m', '6m', '1y', '2y', '3y', '5y', '7y', '10y', '20y', '30y']

        # Use FRED series if available, otherwise approximate
        curve_data = {
            'country': 'US',
            'currency': 'USD',
            'maturities': [],
            'yields': [],
            'date': datetime.now().strftime('%Y-%m-%d')
        }

        # Simplified: get key points from Yahoo Finance
        key_points = [
            ('3m', '^IRX'),
            ('5y', '^FVX'),
            ('10y', '^TNX'),
            ('30y', '^TYX')
        ]

        for maturity, ticker in key_points:
            try:
                t = yf.Ticker(ticker)
                hist = t.history(period='1d')
                if not hist.empty:
                    curve_data['maturities'].append(maturity)
                    curve_data['yields'].append(round(hist['Close'].iloc[-1], 3))
            except Exception:
                continue

        # Analyze curve shape
        if len(curve_data['yields']) >= 2:
            curve_data['shape'] = self._analyze_curve_shape(curve_data['yields'])

        curve_data['source'] = 'yahoo_finance'
        return curve_data

    def _get_china_yield_curve(self) -> Dict:
        """获取中国收益率曲线"""
        if self.china_source:
            yields = self.china_source.get_bond_yields()
            if yields:
                latest = yields[0] if yields else {}
                return {
                    'country': 'CN',
                    'currency': 'CNY',
                    'date': latest.get('date', ''),
                    'maturities': ['1y', '5y', '10y', '30y'],
                    'yields': [
                        latest.get('cn_1y'),
                        latest.get('cn_5y'),
                        latest.get('cn_10y'),
                        latest.get('cn_30y')
                    ],
                    'source': 'eastmoney'
                }

        return {'error': 'China yield data not available'}

    def _analyze_curve_shape(self, yields: List[float]) -> str:
        """分析收益率曲线形态"""
        if len(yields) < 2:
            return 'insufficient_data'

        # Calculate slope
        slope = yields[-1] - yields[0]

        if slope > 0.5:
            return 'steep_normal'
        elif slope > 0:
            return 'normal'
        elif slope > -0.3:
            return 'flat'
        else:
            return 'inverted'

    def get_credit_spreads(self) -> Dict:
        """
        获取信用利差

        Returns:
            各等级信用利差
        """
        spreads = {}

        # Use ETF prices as proxies
        try:
            # Investment grade vs Treasury
            lqd = yf.Ticker('LQD')  # IG Corporate
            ief = yf.Ticker('IEF')  # 7-10Y Treasury

            lqd_hist = lqd.history(period='1mo')
            ief_hist = ief.history(period='1mo')

            if not lqd_hist.empty and not ief_hist.empty:
                # Calculate yield difference (simplified)
                spreads['ig_spread'] = {
                    'description': 'Investment Grade Credit Spread (approximation)',
                    'note': 'Based on LQD vs IEF ETF comparison'
                }

            # High yield spread
            hyg = yf.Ticker('HYG')
            hyg_hist = hyg.history(period='1mo')

            if not hyg_hist.empty:
                spreads['hy_spread'] = {
                    'description': 'High Yield Credit Spread (approximation)',
                    'note': 'Based on HYG ETF'
                }

        except Exception as e:
            spreads['error'] = str(e)

        spreads['source'] = 'yahoo_finance'
        spreads['note'] = 'Credit spreads are approximations based on ETF data'

        return spreads

    def get_bond_etf_data(self, category: str = 'treasury') -> List[Dict]:
        """
        获取债券ETF数据

        Args:
            category: ETF类别 ('treasury', 'corporate', 'high_yield', 'tips', 'muni', 'international')

        Returns:
            ETF数据列表
        """
        tickers = self.BOND_ETFS.get(category, [])
        if not tickers:
            return []

        results = []
        for ticker in tickers:
            try:
                t = yf.Ticker(ticker)
                info = t.info
                hist = t.history(period='1mo')

                if hist.empty:
                    continue

                current_price = hist['Close'].iloc[-1]
                month_ago_price = hist['Close'].iloc[0]
                month_return = (current_price / month_ago_price - 1) * 100

                results.append({
                    'ticker': ticker,
                    'name': info.get('longName', ticker),
                    'price': round(current_price, 2),
                    'ytd_return': info.get('ytdReturn'),
                    '1m_return': round(month_return, 2),
                    'yield': info.get('yield'),
                    'expense_ratio': info.get('annualReportExpenseRatio'),
                    'aum': info.get('totalAssets'),
                    'avg_maturity': info.get('threeYearAverageReturn'),  # Placeholder
                    'source': 'yahoo_finance'
                })

            except Exception as e:
                print(f"Error fetching {ticker}: {e}", file=sys.stderr)
                continue

        return results

    def get_bond_comparison(self, tickers: List[str], period: str = '1y') -> Dict:
        """
        比较多个债券/ETF

        Args:
            tickers: 债券代码列表
            period: 比较期间

        Returns:
            比较数据
        """
        comparison = {
            'tickers': tickers,
            'period': period,
            'data': {}
        }

        for ticker in tickers:
            try:
                t = yf.Ticker(ticker)
                hist = t.history(period=period)

                if hist.empty:
                    continue

                returns = hist['Close'].pct_change().dropna()

                comparison['data'][ticker] = {
                    'start_price': round(hist['Close'].iloc[0], 2),
                    'end_price': round(hist['Close'].iloc[-1], 2),
                    'total_return': round((hist['Close'].iloc[-1] / hist['Close'].iloc[0] - 1) * 100, 2),
                    'volatility': round(returns.std() * np.sqrt(252) * 100, 2),
                    'max_drawdown': round(self._calculate_max_drawdown(hist['Close']) * 100, 2)
                }

            except Exception as e:
                comparison['data'][ticker] = {'error': str(e)}

        return comparison

    def _calculate_max_drawdown(self, prices: pd.Series) -> float:
        """计算最大回撤"""
        rolling_max = prices.expanding().max()
        drawdown = (prices - rolling_max) / rolling_max
        return drawdown.min()

    def get_duration_analysis(self, ticker: str) -> Dict:
        """
        获取久期分析（基于ETF特征）

        Args:
            ticker: ETF代码

        Returns:
            久期相关数据
        """
        try:
            t = yf.Ticker(ticker)
            info = t.info
            hist = t.history(period='1y')

            if hist.empty:
                return {'error': 'No data available'}

            # Estimate duration from price sensitivity
            # This is a simplified approximation
            returns = hist['Close'].pct_change().dropna()

            # Get treasury rate changes (simplified)
            tnx = yf.Ticker('^TNX')
            rate_hist = tnx.history(period='1y')

            if rate_hist.empty:
                return {'error': 'Rate data not available'}

            rate_changes = rate_hist['Close'].diff().dropna()

            # Align indices
            common_idx = returns.index.intersection(rate_changes.index)
            returns = returns[common_idx]
            rate_changes = rate_changes[common_idx]

            # Estimate duration (simplified)
            if len(returns) > 20 and rate_changes.std() > 0:
                # Regression to estimate duration
                correlation = returns.corr(rate_changes)
                estimated_duration = abs(returns.std() / rate_changes.std() * 100)

                return {
                    'ticker': ticker,
                    'name': info.get('longName', ticker),
                    'estimated_duration': round(estimated_duration, 2),
                    'rate_correlation': round(correlation, 4),
                    'interpretation': self._interpret_duration(estimated_duration),
                    'note': 'Duration is estimated from price/rate sensitivity',
                    'source': 'yahoo_finance'
                }

            return {'error': 'Insufficient data for duration calculation'}

        except Exception as e:
            return {'error': str(e)}

    def _interpret_duration(self, duration: float) -> str:
        """解读久期"""
        if duration < 3:
            return 'Short duration - Low interest rate sensitivity'
        elif duration < 7:
            return 'Medium duration - Moderate interest rate sensitivity'
        elif duration < 12:
            return 'Long duration - High interest rate sensitivity'
        else:
            return 'Very long duration - Very high interest rate sensitivity'


def main():
    parser = argparse.ArgumentParser(description="Fetch bond market data")
    parser.add_argument("ticker", nargs='?', help="Bond/ETF ticker")
    parser.add_argument("--yields", action="store_true",
                       help="Get US Treasury yields")
    parser.add_argument("--curve", action="store_true",
                       help="Get yield curve")
    parser.add_argument("--country", default="US", choices=["US", "CN"],
                       help="Country for yield curve")
    parser.add_argument("--spreads", action="store_true",
                       help="Get credit spreads")
    parser.add_argument("--etfs", action="store_true",
                       help="Get bond ETF data")
    parser.add_argument("--category", default="treasury",
                       choices=["treasury", "corporate", "high_yield", "tips", "muni", "international"],
                       help="ETF category")
    parser.add_argument("--compare", nargs='+',
                       help="Compare multiple bonds/ETFs")
    parser.add_argument("--duration", action="store_true",
                       help="Get duration analysis")
    parser.add_argument("--period", default="1y",
                       help="Period for comparison")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format")

    args = parser.parse_args()

    fetcher = BondDataFetcher()

    if args.yields:
        data = fetcher.get_us_treasury_yields()
    elif args.curve:
        data = fetcher.get_yield_curve(args.country)
    elif args.spreads:
        data = fetcher.get_credit_spreads()
    elif args.etfs:
        data = fetcher.get_bond_etf_data(args.category)
    elif args.compare:
        data = fetcher.get_bond_comparison(args.compare, args.period)
    elif args.duration and args.ticker:
        data = fetcher.get_duration_analysis(args.ticker)
    elif args.ticker:
        data = fetcher.get_bond_etf_data('treasury')
        data = [d for d in data if d['ticker'] == args.ticker.upper()]
        data = data[0] if data else {'error': 'Ticker not found'}
    else:
        data = fetcher.get_us_treasury_yields()

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2, default=str))
    else:
        if args.yields or (not args.curve and not args.etfs and not args.spreads):
            print("\n=== US Treasury Yields ===\n")
            for maturity, info in data.items():
                if isinstance(info, dict) and 'yield' in info:
                    print(f"{maturity}: {info['yield']}% ({info['change']:+.3f})")

        elif args.curve:
            print(f"\n=== {args.country} Yield Curve ===\n")
            if 'maturities' in data:
                for m, y in zip(data['maturities'], data['yields']):
                    print(f"{m}: {y}%")
                if 'shape' in data:
                    print(f"\nCurve Shape: {data['shape']}")

        elif args.etfs or isinstance(data, list):
            print(f"\n=== Bond ETFs ({args.category}) ===\n")
            for etf in data:
                if isinstance(etf, dict):
                    print(f"{etf.get('ticker', 'N/A')}: {etf.get('name', 'N/A')}")
                    print(f"  Price: ${etf.get('price', 'N/A')}")
                    print(f"  1M Return: {etf.get('1m_return', 'N/A')}%")
                    print()

        elif isinstance(data, dict):
            print("\n=== Bond Data ===\n")
            for k, v in data.items():
                print(f"{k}: {v}")


if __name__ == "__main__":
    main()
