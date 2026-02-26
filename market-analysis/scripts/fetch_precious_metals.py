#!/usr/bin/env python3
"""
Precious Metals Data Fetcher for Market Analysis
Supports gold, silver, platinum, palladium prices from multiple sources.
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
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install yfinance pandas")
    sys.exit(1)

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
try:
    from cache_manager import get_cache, cached
    from rate_limiter import get_limiter, with_rate_limit
except ImportError:
    get_cache = None
    get_limiter = None


class PreciousMetalsFetcher:
    """
    Fetcher for precious metals data.

    Supported metals:
    - Gold (XAU)
    - Silver (XAG)
    - Platinum (XPT)
    - Palladium (XPD)
    """

    # Yahoo Finance ticker symbols
    METAL_SYMBOLS = {
        'gold': 'GC=F',       # Gold Futures
        'silver': 'SI=F',     # Silver Futures
        'platinum': 'PL=F',   # Platinum Futures
        'palladium': 'PA=F',  # Palladium Futures
        'gold_spot': 'XAUUSD=X',   # Gold Spot
        'silver_spot': 'XAGUSD=X', # Silver Spot
    }

    # ETF symbols
    METAL_ETFS = {
        'gold': ['GLD', 'IAU', 'SGOL', 'GLDM'],
        'silver': ['SLV', 'SIVR', 'PSLV'],
        'platinum': ['PPLT'],
        'palladium': ['PALL']
    }

    # Shanghai Gold Exchange codes (via eastmoney)
    SGE_CODES = {
        'au99.99': 'Au99.99',  # 现货黄金
        'au100g': 'Au100g',
        'ag99.9': 'Ag99.9',    # 现货白银
    }

    def __init__(self):
        self.cache = get_cache() if get_cache else None
        self.limiter = get_limiter() if get_limiter else None

    def get_metal_price(self, metal: str = 'gold', price_type: str = 'futures') -> Optional[Dict]:
        """
        获取贵金属价格

        Args:
            metal: 金属类型 ('gold', 'silver', 'platinum', 'palladium')
            price_type: 价格类型 ('futures', 'spot')

        Returns:
            价格数据
        """
        if price_type == 'spot' and metal in ['gold', 'silver']:
            symbol = self.METAL_SYMBOLS.get(f'{metal}_spot')
        else:
            symbol = self.METAL_SYMBOLS.get(metal)

        if not symbol:
            return {'error': f'Unknown metal: {metal}'}

        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period='5d')

            if hist.empty:
                return {'error': f'No data available for {metal}'}

            current_price = hist['Close'].iloc[-1]
            previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price

            change = current_price - previous_close
            change_pct = (change / previous_close) * 100 if previous_close else 0

            return {
                'metal': metal,
                'symbol': symbol,
                'price_type': price_type,
                'current_price': round(current_price, 2),
                'previous_close': round(previous_close, 2),
                'change': round(change, 2),
                'change_percent': round(change_pct, 2),
                'day_high': round(hist['High'].iloc[-1], 2),
                'day_low': round(hist['Low'].iloc[-1], 2),
                'volume': int(hist['Volume'].iloc[-1]) if hist['Volume'].iloc[-1] > 0 else None,
                'currency': 'USD',
                'unit': 'per troy ounce',
                'timestamp': datetime.now().isoformat(),
                'source': 'yahoo_finance'
            }

        except Exception as e:
            return {'error': f'Failed to fetch {metal} price: {str(e)}'}

    def get_all_metals(self) -> Dict[str, Dict]:
        """获取所有贵金属价格"""
        results = {}
        for metal in ['gold', 'silver', 'platinum', 'palladium']:
            results[metal] = self.get_metal_price(metal)
        return results

    def get_metal_history(self, metal: str = 'gold', period: str = '1y',
                         interval: str = '1d') -> Optional[Dict]:
        """
        获取贵金属历史数据

        Args:
            metal: 金属类型
            period: 时间段 ('1mo', '3mo', '6mo', '1y', '2y', '5y')
            interval: 数据间隔 ('1d', '1wk', '1mo')

        Returns:
            历史数据
        """
        symbol = self.METAL_SYMBOLS.get(metal)
        if not symbol:
            return {'error': f'Unknown metal: {metal}'}

        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, interval=interval)

            if hist.empty:
                return {'error': f'No historical data for {metal}'}

            # Calculate statistics
            prices = hist['Close']
            returns = prices.pct_change().dropna()

            return {
                'metal': metal,
                'symbol': symbol,
                'period': period,
                'interval': interval,
                'data_points': len(hist),
                'start_date': hist.index[0].strftime('%Y-%m-%d'),
                'end_date': hist.index[-1].strftime('%Y-%m-%d'),
                'start_price': round(prices.iloc[0], 2),
                'end_price': round(prices.iloc[-1], 2),
                'period_high': round(prices.max(), 2),
                'period_low': round(prices.min(), 2),
                'period_return': round((prices.iloc[-1] / prices.iloc[0] - 1) * 100, 2),
                'volatility': round(returns.std() * (252 ** 0.5) * 100, 2),  # Annualized
                'history': {
                    'dates': hist.index.strftime('%Y-%m-%d').tolist()[-30:],
                    'close': hist['Close'].round(2).tolist()[-30:],
                    'high': hist['High'].round(2).tolist()[-30:],
                    'low': hist['Low'].round(2).tolist()[-30:]
                },
                'source': 'yahoo_finance'
            }

        except Exception as e:
            return {'error': f'Failed to fetch history for {metal}: {str(e)}'}

    def get_gold_silver_ratio(self) -> Optional[Dict]:
        """
        计算金银比

        Returns:
            金银比数据
        """
        gold = self.get_metal_price('gold')
        silver = self.get_metal_price('silver')

        if 'error' in gold or 'error' in silver:
            return {'error': 'Failed to calculate gold/silver ratio'}

        ratio = gold['current_price'] / silver['current_price']

        # Historical context
        try:
            gold_ticker = yf.Ticker(self.METAL_SYMBOLS['gold'])
            silver_ticker = yf.Ticker(self.METAL_SYMBOLS['silver'])

            gold_hist = gold_ticker.history(period='1y')['Close']
            silver_hist = silver_ticker.history(period='1y')['Close']

            # Align indices
            common_idx = gold_hist.index.intersection(silver_hist.index)
            gold_hist = gold_hist[common_idx]
            silver_hist = silver_hist[common_idx]

            ratio_hist = gold_hist / silver_hist

            return {
                'current_ratio': round(ratio, 2),
                'gold_price': gold['current_price'],
                'silver_price': silver['current_price'],
                'interpretation': self._interpret_ratio(ratio),
                '1y_avg_ratio': round(ratio_hist.mean(), 2),
                '1y_high_ratio': round(ratio_hist.max(), 2),
                '1y_low_ratio': round(ratio_hist.min(), 2),
                'percentile': self._calculate_percentile(ratio, ratio_hist),
                'timestamp': datetime.now().isoformat(),
                'source': 'yahoo_finance'
            }

        except Exception as e:
            return {
                'current_ratio': round(ratio, 2),
                'gold_price': gold['current_price'],
                'silver_price': silver['current_price'],
                'interpretation': self._interpret_ratio(ratio),
                'error': str(e)
            }

    def _interpret_ratio(self, ratio: float) -> str:
        """解读金银比"""
        if ratio > 80:
            return "High ratio - Silver may be undervalued relative to gold"
        elif ratio > 70:
            return "Above average - Slightly favors silver"
        elif ratio > 50:
            return "Normal range"
        elif ratio > 40:
            return "Below average - Slightly favors gold"
        else:
            return "Low ratio - Gold may be undervalued relative to silver"

    def _calculate_percentile(self, value: float, series: pd.Series) -> int:
        """计算百分位"""
        return int((series < value).sum() / len(series) * 100)

    def get_metal_etfs(self, metal: str = 'gold') -> List[Dict]:
        """
        获取贵金属ETF数据

        Args:
            metal: 金属类型

        Returns:
            ETF列表
        """
        etf_symbols = self.METAL_ETFS.get(metal, [])
        if not etf_symbols:
            return []

        results = []
        for symbol in etf_symbols:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                hist = ticker.history(period='1d')

                if hist.empty:
                    continue

                results.append({
                    'symbol': symbol,
                    'name': info.get('longName', symbol),
                    'price': round(hist['Close'].iloc[-1], 2),
                    'change_percent': round(info.get('regularMarketChangePercent', 0), 2),
                    'volume': int(hist['Volume'].iloc[-1]),
                    'aum': info.get('totalAssets'),
                    'expense_ratio': info.get('annualReportExpenseRatio'),
                    'ytd_return': info.get('ytdReturn'),
                    'source': 'yahoo_finance'
                })

            except Exception as e:
                print(f"Error fetching ETF {symbol}: {e}", file=sys.stderr)
                continue

        return results

    def get_dollar_correlation(self, metal: str = 'gold', period: str = '1y') -> Optional[Dict]:
        """
        计算贵金属与美元指数相关性

        Args:
            metal: 金属类型
            period: 时间段

        Returns:
            相关性数据
        """
        metal_symbol = self.METAL_SYMBOLS.get(metal)
        dollar_symbol = 'DX-Y.NYB'  # US Dollar Index

        try:
            metal_ticker = yf.Ticker(metal_symbol)
            dollar_ticker = yf.Ticker(dollar_symbol)

            metal_hist = metal_ticker.history(period=period)['Close']
            dollar_hist = dollar_ticker.history(period=period)['Close']

            # Align indices
            common_idx = metal_hist.index.intersection(dollar_hist.index)
            metal_hist = metal_hist[common_idx]
            dollar_hist = dollar_hist[common_idx]

            # Calculate correlation
            correlation = metal_hist.corr(dollar_hist)

            # Calculate rolling correlation
            rolling_corr = metal_hist.rolling(30).corr(dollar_hist).dropna()

            return {
                'metal': metal,
                'period': period,
                'correlation': round(correlation, 4),
                'interpretation': self._interpret_correlation(correlation),
                'rolling_30d_corr': round(rolling_corr.iloc[-1], 4) if len(rolling_corr) > 0 else None,
                'rolling_corr_range': {
                    'min': round(rolling_corr.min(), 4) if len(rolling_corr) > 0 else None,
                    'max': round(rolling_corr.max(), 4) if len(rolling_corr) > 0 else None
                },
                'source': 'yahoo_finance'
            }

        except Exception as e:
            return {'error': f'Failed to calculate correlation: {str(e)}'}

    def _interpret_correlation(self, corr: float) -> str:
        """解读相关性"""
        if corr < -0.7:
            return "Strong negative correlation - Typical for gold/USD"
        elif corr < -0.3:
            return "Moderate negative correlation"
        elif corr < 0.3:
            return "Weak/no correlation"
        elif corr < 0.7:
            return "Moderate positive correlation"
        else:
            return "Strong positive correlation - Unusual for gold/USD"


def main():
    parser = argparse.ArgumentParser(description="Fetch precious metals data")
    parser.add_argument("metal", nargs='?', default='gold',
                       choices=['gold', 'silver', 'platinum', 'palladium', 'all'],
                       help="Metal to fetch (default: gold)")
    parser.add_argument("--spot", action="store_true",
                       help="Get spot price instead of futures")
    parser.add_argument("--history", action="store_true",
                       help="Get historical data")
    parser.add_argument("--period", default="1y",
                       choices=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
                       help="Historical period (default: 1y)")
    parser.add_argument("--ratio", action="store_true",
                       help="Get gold/silver ratio")
    parser.add_argument("--etfs", action="store_true",
                       help="Get related ETFs")
    parser.add_argument("--correlation", action="store_true",
                       help="Get USD correlation")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format")

    args = parser.parse_args()

    fetcher = PreciousMetalsFetcher()

    if args.ratio:
        data = fetcher.get_gold_silver_ratio()
    elif args.etfs:
        data = fetcher.get_metal_etfs(args.metal if args.metal != 'all' else 'gold')
    elif args.correlation:
        data = fetcher.get_dollar_correlation(args.metal if args.metal != 'all' else 'gold', args.period)
    elif args.history:
        data = fetcher.get_metal_history(args.metal if args.metal != 'all' else 'gold', args.period)
    elif args.metal == 'all':
        data = fetcher.get_all_metals()
    else:
        price_type = 'spot' if args.spot else 'futures'
        data = fetcher.get_metal_price(args.metal, price_type)

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2, default=str))
    else:
        if args.ratio:
            print("\n=== Gold/Silver Ratio ===\n")
            if 'error' not in data:
                print(f"Current Ratio: {data['current_ratio']}")
                print(f"Gold Price: ${data['gold_price']}/oz")
                print(f"Silver Price: ${data['silver_price']}/oz")
                print(f"\n{data['interpretation']}")
                if '1y_avg_ratio' in data:
                    print(f"\n1Y Average: {data['1y_avg_ratio']}")
                    print(f"1Y Range: {data['1y_low_ratio']} - {data['1y_high_ratio']}")
                    print(f"Percentile: {data.get('percentile', 'N/A')}%")
            else:
                print(f"Error: {data['error']}")

        elif args.etfs:
            print(f"\n=== {args.metal.title()} ETFs ===\n")
            for etf in data:
                print(f"{etf['symbol']}: {etf['name']}")
                print(f"  Price: ${etf['price']} ({etf['change_percent']:+.2f}%)")
                if etf.get('aum'):
                    print(f"  AUM: ${etf['aum']:,.0f}")
                print()

        elif isinstance(data, dict) and 'error' not in data:
            if args.metal == 'all':
                print("\n=== Precious Metals Prices ===\n")
                for metal, info in data.items():
                    if 'error' not in info:
                        print(f"{metal.title()}: ${info['current_price']}/oz ({info['change_percent']:+.2f}%)")
            else:
                print(f"\n=== {data.get('metal', args.metal).title()} Price ===\n")
                print(f"Current: ${data.get('current_price', 'N/A')}/oz")
                print(f"Change: ${data.get('change', 'N/A')} ({data.get('change_percent', 'N/A'):+.2f}%)")
                print(f"Day Range: ${data.get('day_low', 'N/A')} - ${data.get('day_high', 'N/A')}")

                if 'period_return' in data:
                    print(f"\nPeriod Return: {data['period_return']}%")
                    print(f"Volatility (Ann.): {data['volatility']}%")
                    print(f"Period Range: ${data['period_low']} - ${data['period_high']}")
        else:
            print(f"Error: {data.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
