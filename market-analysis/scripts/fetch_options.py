#!/usr/bin/env python3
"""
Options Data Fetcher for Market Analysis
Fetches options chains, expiration dates, and Greeks.
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


class OptionsDataFetcher:
    """
    Fetcher for options market data.

    Features:
    - Options chain data
    - Expiration dates
    - Strike prices
    - Open interest and volume
    - Implied volatility
    """

    def __init__(self):
        pass

    def get_expiration_dates(self, ticker: str) -> List[str]:
        """
        获取期权到期日列表

        Args:
            ticker: 股票代码

        Returns:
            到期日列表
        """
        try:
            stock = yf.Ticker(ticker)
            return list(stock.options)
        except Exception as e:
            print(f"Error fetching expirations for {ticker}: {e}", file=sys.stderr)
            return []

    def get_options_chain(self, ticker: str, expiration: str = None,
                         option_type: str = 'both') -> Dict:
        """
        获取期权链数据

        Args:
            ticker: 股票代码
            expiration: 到期日 (如不指定，使用最近到期日)
            option_type: 期权类型 ('call', 'put', 'both')

        Returns:
            期权链数据
        """
        try:
            stock = yf.Ticker(ticker)

            # Get current stock price
            hist = stock.history(period='1d')
            current_price = hist['Close'].iloc[-1] if not hist.empty else None

            # Get expiration dates
            expirations = stock.options
            if not expirations:
                return {'error': f'No options available for {ticker}'}

            # Use specified expiration or first available
            if expiration and expiration in expirations:
                exp_date = expiration
            else:
                exp_date = expirations[0]

            # Get options chain
            opt = stock.option_chain(exp_date)

            result = {
                'ticker': ticker,
                'current_price': round(current_price, 2) if current_price else None,
                'expiration': exp_date,
                'days_to_expiration': self._days_to_expiration(exp_date),
                'available_expirations': expirations[:10],  # First 10
                'calls': None,
                'puts': None
            }

            if option_type in ['call', 'both']:
                result['calls'] = self._process_options_df(opt.calls, current_price)

            if option_type in ['put', 'both']:
                result['puts'] = self._process_options_df(opt.puts, current_price)

            return result

        except Exception as e:
            return {'error': f'Failed to fetch options for {ticker}: {str(e)}'}

    def _process_options_df(self, df: pd.DataFrame, current_price: float) -> Dict:
        """处理期权数据框"""
        if df.empty:
            return None

        # Filter and format
        records = []
        for _, row in df.iterrows():
            strike = row['strike']
            moneyness = 'ITM' if current_price else 'Unknown'

            if current_price:
                if row.name and 'call' in str(row.name).lower():
                    moneyness = 'ITM' if strike < current_price else 'OTM'
                else:
                    moneyness = 'ITM' if strike > current_price else 'OTM'

            records.append({
                'strike': strike,
                'lastPrice': row.get('lastPrice'),
                'bid': row.get('bid'),
                'ask': row.get('ask'),
                'volume': int(row.get('volume', 0)) if pd.notna(row.get('volume')) else 0,
                'openInterest': int(row.get('openInterest', 0)) if pd.notna(row.get('openInterest')) else 0,
                'impliedVolatility': round(row.get('impliedVolatility', 0) * 100, 2) if pd.notna(row.get('impliedVolatility')) else None,
                'inTheMoney': row.get('inTheMoney', False),
                'moneyness': moneyness
            })

        # Summary statistics
        total_volume = sum(r['volume'] for r in records)
        total_oi = sum(r['openInterest'] for r in records)
        avg_iv = np.mean([r['impliedVolatility'] for r in records if r['impliedVolatility']])

        return {
            'count': len(records),
            'total_volume': total_volume,
            'total_open_interest': total_oi,
            'avg_implied_volatility': round(avg_iv, 2) if not np.isnan(avg_iv) else None,
            'contracts': records
        }

    def _days_to_expiration(self, exp_date: str) -> int:
        """计算到期天数"""
        try:
            exp = datetime.strptime(exp_date, '%Y-%m-%d')
            return (exp - datetime.now()).days
        except:
            return 0

    def get_atm_options(self, ticker: str, expiration: str = None) -> Dict:
        """
        获取平值期权数据

        Args:
            ticker: 股票代码
            expiration: 到期日

        Returns:
            平值期权数据
        """
        chain = self.get_options_chain(ticker, expiration)
        if 'error' in chain:
            return chain

        current_price = chain['current_price']
        if not current_price:
            return {'error': 'Unable to determine current price'}

        # Find ATM options
        atm_call = None
        atm_put = None

        if chain.get('calls') and chain['calls'].get('contracts'):
            calls = chain['calls']['contracts']
            # Find strike closest to current price
            atm_call = min(calls, key=lambda x: abs(x['strike'] - current_price))

        if chain.get('puts') and chain['puts'].get('contracts'):
            puts = chain['puts']['contracts']
            atm_put = min(puts, key=lambda x: abs(x['strike'] - current_price))

        return {
            'ticker': ticker,
            'current_price': current_price,
            'expiration': chain['expiration'],
            'days_to_expiration': chain['days_to_expiration'],
            'atm_call': atm_call,
            'atm_put': atm_put,
            'atm_straddle_price': (
                (atm_call['ask'] + atm_put['ask'])
                if atm_call and atm_put and atm_call.get('ask') and atm_put.get('ask')
                else None
            )
        }

    def get_put_call_ratio(self, ticker: str, expiration: str = None) -> Dict:
        """
        计算看跌看涨比

        Args:
            ticker: 股票代码
            expiration: 到期日

        Returns:
            看跌看涨比数据
        """
        chain = self.get_options_chain(ticker, expiration)
        if 'error' in chain:
            return chain

        calls = chain.get('calls', {})
        puts = chain.get('puts', {})

        call_volume = calls.get('total_volume', 0) if calls else 0
        put_volume = puts.get('total_volume', 0) if puts else 0
        call_oi = calls.get('total_open_interest', 0) if calls else 0
        put_oi = puts.get('total_open_interest', 0) if puts else 0

        volume_ratio = put_volume / call_volume if call_volume > 0 else None
        oi_ratio = put_oi / call_oi if call_oi > 0 else None

        return {
            'ticker': ticker,
            'expiration': chain['expiration'],
            'call_volume': call_volume,
            'put_volume': put_volume,
            'call_open_interest': call_oi,
            'put_open_interest': put_oi,
            'volume_put_call_ratio': round(volume_ratio, 4) if volume_ratio else None,
            'oi_put_call_ratio': round(oi_ratio, 4) if oi_ratio else None,
            'sentiment_interpretation': self._interpret_pcr(volume_ratio)
        }

    def _interpret_pcr(self, ratio: float) -> str:
        """解读看跌看涨比"""
        if ratio is None:
            return 'Unable to determine'
        elif ratio > 1.2:
            return 'Bearish sentiment (high put activity)'
        elif ratio > 0.8:
            return 'Neutral sentiment'
        else:
            return 'Bullish sentiment (high call activity)'

    def get_max_pain(self, ticker: str, expiration: str = None) -> Dict:
        """
        计算最大痛点

        Args:
            ticker: 股票代码
            expiration: 到期日

        Returns:
            最大痛点数据
        """
        chain = self.get_options_chain(ticker, expiration)
        if 'error' in chain:
            return chain

        calls = chain.get('calls', {}).get('contracts', [])
        puts = chain.get('puts', {}).get('contracts', [])

        if not calls or not puts:
            return {'error': 'Insufficient options data'}

        # Get all unique strikes
        strikes = sorted(set([c['strike'] for c in calls] + [p['strike'] for p in puts]))

        # Calculate pain at each strike
        max_pain_strike = None
        min_pain_value = float('inf')
        pain_values = []

        for strike in strikes:
            pain = 0

            # Pain from calls
            for call in calls:
                if call['strike'] < strike:
                    pain += (strike - call['strike']) * call['openInterest']

            # Pain from puts
            for put in puts:
                if put['strike'] > strike:
                    pain += (put['strike'] - strike) * put['openInterest']

            pain_values.append({'strike': strike, 'pain': pain})

            if pain < min_pain_value:
                min_pain_value = pain
                max_pain_strike = strike

        return {
            'ticker': ticker,
            'expiration': chain['expiration'],
            'current_price': chain['current_price'],
            'max_pain_strike': max_pain_strike,
            'distance_from_current': round(max_pain_strike - chain['current_price'], 2) if max_pain_strike and chain['current_price'] else None,
            'distance_percent': round((max_pain_strike / chain['current_price'] - 1) * 100, 2) if max_pain_strike and chain['current_price'] else None,
            'interpretation': 'Price may gravitate toward max pain strike at expiration'
        }

    def get_iv_term_structure(self, ticker: str) -> Dict:
        """
        获取隐含波动率期限结构

        Args:
            ticker: 股票代码

        Returns:
            IV期限结构
        """
        expirations = self.get_expiration_dates(ticker)
        if not expirations:
            return {'error': f'No options available for {ticker}'}

        term_structure = []

        for exp in expirations[:8]:  # First 8 expirations
            atm = self.get_atm_options(ticker, exp)
            if 'error' not in atm and atm.get('atm_call'):
                iv = atm['atm_call'].get('impliedVolatility')
                if iv:
                    term_structure.append({
                        'expiration': exp,
                        'days_to_expiration': atm['days_to_expiration'],
                        'atm_iv': iv
                    })

        if not term_structure:
            return {'error': 'Unable to calculate IV term structure'}

        return {
            'ticker': ticker,
            'term_structure': term_structure,
            'iv_shape': self._analyze_term_structure(term_structure)
        }

    def _analyze_term_structure(self, structure: List[Dict]) -> str:
        """分析波动率期限结构"""
        if len(structure) < 2:
            return 'insufficient_data'

        ivs = [s['atm_iv'] for s in structure]

        if ivs[-1] > ivs[0] * 1.1:
            return 'contango (upward sloping) - expecting future uncertainty'
        elif ivs[-1] < ivs[0] * 0.9:
            return 'backwardation (downward sloping) - near-term event expected'
        else:
            return 'flat - relatively stable IV expectations'


def main():
    parser = argparse.ArgumentParser(description="Fetch options data")
    parser.add_argument("ticker", help="Stock ticker symbol")
    parser.add_argument("--expiration", help="Expiration date (YYYY-MM-DD)")
    parser.add_argument("--type", choices=["call", "put", "both"], default="both",
                       help="Option type")
    parser.add_argument("--expirations", action="store_true",
                       help="List expiration dates")
    parser.add_argument("--atm", action="store_true",
                       help="Get ATM options")
    parser.add_argument("--pcr", action="store_true",
                       help="Get put/call ratio")
    parser.add_argument("--max-pain", action="store_true",
                       help="Calculate max pain")
    parser.add_argument("--iv-term", action="store_true",
                       help="Get IV term structure")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format")

    args = parser.parse_args()

    fetcher = OptionsDataFetcher()
    ticker = args.ticker.upper()

    if args.expirations:
        data = fetcher.get_expiration_dates(ticker)
        data = {'ticker': ticker, 'expirations': data}
    elif args.atm:
        data = fetcher.get_atm_options(ticker, args.expiration)
    elif args.pcr:
        data = fetcher.get_put_call_ratio(ticker, args.expiration)
    elif args.max_pain:
        data = fetcher.get_max_pain(ticker, args.expiration)
    elif args.iv_term:
        data = fetcher.get_iv_term_structure(ticker)
    else:
        data = fetcher.get_options_chain(ticker, args.expiration, args.type)

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2, default=str))
    else:
        if args.expirations:
            print(f"\n=== {ticker} Option Expirations ===\n")
            for exp in data.get('expirations', []):
                print(f"  {exp}")

        elif args.atm:
            print(f"\n=== {ticker} ATM Options ===\n")
            print(f"Current Price: ${data.get('current_price', 'N/A')}")
            print(f"Expiration: {data.get('expiration', 'N/A')} ({data.get('days_to_expiration', 'N/A')} days)")
            if data.get('atm_call'):
                print(f"\nATM Call (Strike ${data['atm_call']['strike']}):")
                print(f"  Bid/Ask: ${data['atm_call']['bid']} / ${data['atm_call']['ask']}")
                print(f"  IV: {data['atm_call']['impliedVolatility']}%")
            if data.get('atm_put'):
                print(f"\nATM Put (Strike ${data['atm_put']['strike']}):")
                print(f"  Bid/Ask: ${data['atm_put']['bid']} / ${data['atm_put']['ask']}")
                print(f"  IV: {data['atm_put']['impliedVolatility']}%")

        elif args.pcr:
            print(f"\n=== {ticker} Put/Call Ratio ===\n")
            print(f"Expiration: {data.get('expiration', 'N/A')}")
            print(f"Call Volume: {data.get('call_volume', 'N/A'):,}")
            print(f"Put Volume: {data.get('put_volume', 'N/A'):,}")
            print(f"Volume P/C Ratio: {data.get('volume_put_call_ratio', 'N/A')}")
            print(f"OI P/C Ratio: {data.get('oi_put_call_ratio', 'N/A')}")
            print(f"\n{data.get('sentiment_interpretation', '')}")

        elif args.max_pain:
            print(f"\n=== {ticker} Max Pain ===\n")
            print(f"Current Price: ${data.get('current_price', 'N/A')}")
            print(f"Max Pain Strike: ${data.get('max_pain_strike', 'N/A')}")
            print(f"Distance: ${data.get('distance_from_current', 'N/A')} ({data.get('distance_percent', 'N/A')}%)")

        elif 'error' in data:
            print(f"Error: {data['error']}")

        else:
            print(f"\n=== {ticker} Options Chain ===\n")
            print(f"Current Price: ${data.get('current_price', 'N/A')}")
            print(f"Expiration: {data.get('expiration', 'N/A')}")
            print(f"Days to Expiration: {data.get('days_to_expiration', 'N/A')}")

            if data.get('calls'):
                print(f"\nCalls: {data['calls']['count']} contracts")
                print(f"  Total Volume: {data['calls']['total_volume']:,}")
                print(f"  Total OI: {data['calls']['total_open_interest']:,}")
                print(f"  Avg IV: {data['calls']['avg_implied_volatility']}%")

            if data.get('puts'):
                print(f"\nPuts: {data['puts']['count']} contracts")
                print(f"  Total Volume: {data['puts']['total_volume']:,}")
                print(f"  Total OI: {data['puts']['total_open_interest']:,}")
                print(f"  Avg IV: {data['puts']['avg_implied_volatility']}%")


if __name__ == "__main__":
    main()
