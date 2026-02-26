#!/usr/bin/env python3
"""
Macro Economic Data Fetcher for Market Analysis
Fetches GDP, CPI, interest rates, employment data, and economic calendar.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

try:
    import requests
    import pandas as pd
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install requests pandas")
    sys.exit(1)

# Try to import FRED API
try:
    from fredapi import Fred
    FRED_AVAILABLE = True
except ImportError:
    FRED_AVAILABLE = False


class MacroDataFetcher:
    """
    Fetcher for macroeconomic data.

    Data sources:
    - FRED (Federal Reserve Economic Data) - US data
    - 东方财富 - China data
    - Various free APIs for global data
    """

    # FRED series IDs for common indicators
    FRED_SERIES = {
        # GDP
        'gdp': 'GDP',
        'gdp_growth': 'A191RL1Q225SBEA',
        'real_gdp': 'GDPC1',

        # Inflation
        'cpi': 'CPIAUCSL',
        'cpi_yoy': 'CPIAUCNS',
        'core_cpi': 'CPILFESL',
        'pce': 'PCEPI',

        # Interest Rates
        'fed_funds_rate': 'FEDFUNDS',
        'prime_rate': 'DPRIME',
        '10y_treasury': 'DGS10',
        '2y_treasury': 'DGS2',
        '30y_treasury': 'DGS30',
        '3m_treasury': 'DTB3',

        # Employment
        'unemployment_rate': 'UNRATE',
        'nonfarm_payrolls': 'PAYEMS',
        'initial_claims': 'ICSA',
        'labor_force_participation': 'CIVPART',

        # Housing
        'housing_starts': 'HOUST',
        'existing_home_sales': 'EXHOSLUSM495S',
        'case_shiller': 'CSUSHPINSA',

        # Manufacturing
        'industrial_production': 'INDPRO',
        'capacity_utilization': 'TCU',
        'ism_manufacturing': 'MANEMP',

        # Consumer
        'retail_sales': 'RSAFS',
        'consumer_confidence': 'UMCSENT',
        'personal_income': 'PI',

        # Money Supply
        'm1': 'M1SL',
        'm2': 'M2SL',

        # Trade
        'trade_balance': 'BOPGSTB',

        # Other
        'vix': 'VIXCLS',
        'dollar_index': 'DTWEXBGS'
    }

    def __init__(self, fred_api_key: str = None):
        """
        Initialize macro data fetcher.

        Args:
            fred_api_key: FRED API key (optional, can use env var FRED_API_KEY)
        """
        self.fred_api_key = fred_api_key or os.environ.get('FRED_API_KEY')
        self.fred = None

        if FRED_AVAILABLE and self.fred_api_key:
            try:
                self.fred = Fred(api_key=self.fred_api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize FRED: {e}", file=sys.stderr)

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_indicator(self, indicator: str, start_date: str = None,
                      end_date: str = None) -> Optional[Dict]:
        """
        获取单个经济指标

        Args:
            indicator: 指标名称或FRED系列ID
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)

        Returns:
            指标数据
        """
        series_id = self.FRED_SERIES.get(indicator.lower(), indicator)

        if self.fred:
            return self._get_from_fred(series_id, indicator, start_date, end_date)
        else:
            return self._get_from_alternative(series_id, indicator)

    def _get_from_fred(self, series_id: str, indicator: str,
                       start_date: str = None, end_date: str = None) -> Optional[Dict]:
        """从FRED获取数据"""
        try:
            # Get series data
            data = self.fred.get_series(series_id, start_date, end_date)

            if data.empty:
                return {'error': f'No data available for {indicator}'}

            # Get series info
            info = self.fred.get_series_info(series_id)

            # Calculate changes
            latest = data.iloc[-1]
            previous = data.iloc[-2] if len(data) > 1 else latest

            return {
                'indicator': indicator,
                'series_id': series_id,
                'title': info.get('title', indicator),
                'latest_value': round(float(latest), 4),
                'latest_date': data.index[-1].strftime('%Y-%m-%d'),
                'previous_value': round(float(previous), 4),
                'change': round(float(latest - previous), 4),
                'change_percent': round((latest - previous) / previous * 100, 2) if previous != 0 else 0,
                'frequency': info.get('frequency_short', 'Unknown'),
                'units': info.get('units', 'Unknown'),
                'seasonal_adjustment': info.get('seasonal_adjustment_short', 'Unknown'),
                'history': {
                    'dates': data.index[-12:].strftime('%Y-%m-%d').tolist(),
                    'values': data.iloc[-12:].round(4).tolist()
                },
                'source': 'FRED',
                'notes': info.get('notes', '')[:200] if info.get('notes') else None
            }

        except Exception as e:
            return {'error': f'Failed to fetch {indicator}: {str(e)}'}

    def _get_from_alternative(self, series_id: str, indicator: str) -> Optional[Dict]:
        """从备用源获取数据（无API密钥时）"""
        return {
            'indicator': indicator,
            'series_id': series_id,
            'error': 'FRED API key not configured. Set FRED_API_KEY environment variable.',
            'get_key_at': 'https://fred.stlouisfed.org/docs/api/api_key.html'
        }

    def get_interest_rates(self) -> Dict:
        """获取利率数据"""
        rates = {}
        rate_indicators = [
            'fed_funds_rate', '3m_treasury', '2y_treasury',
            '10y_treasury', '30y_treasury', 'prime_rate'
        ]

        for indicator in rate_indicators:
            data = self.get_indicator(indicator)
            if data and 'error' not in data:
                rates[indicator] = {
                    'value': data['latest_value'],
                    'date': data['latest_date'],
                    'change': data['change']
                }

        # Calculate yield curve spread
        if '10y_treasury' in rates and '2y_treasury' in rates:
            spread = rates['10y_treasury']['value'] - rates['2y_treasury']['value']
            rates['yield_curve_spread'] = {
                'value': round(spread, 4),
                'interpretation': 'Normal' if spread > 0 else 'Inverted (recession signal)'
            }

        return rates

    def get_inflation_data(self) -> Dict:
        """获取通胀数据"""
        inflation = {}
        indicators = ['cpi', 'cpi_yoy', 'core_cpi', 'pce']

        for indicator in indicators:
            data = self.get_indicator(indicator)
            if data and 'error' not in data:
                inflation[indicator] = {
                    'value': data['latest_value'],
                    'date': data['latest_date'],
                    'units': data.get('units', '')
                }

        return inflation

    def get_employment_data(self) -> Dict:
        """获取就业数据"""
        employment = {}
        indicators = ['unemployment_rate', 'nonfarm_payrolls', 'initial_claims',
                     'labor_force_participation']

        for indicator in indicators:
            data = self.get_indicator(indicator)
            if data and 'error' not in data:
                employment[indicator] = {
                    'value': data['latest_value'],
                    'date': data['latest_date'],
                    'change': data.get('change'),
                    'units': data.get('units', '')
                }

        return employment

    def get_economic_calendar(self, days: int = 7) -> List[Dict]:
        """
        获取经济日历

        Args:
            days: 查询未来天数

        Returns:
            事件列表
        """
        # This would typically come from a dedicated API
        # For now, return a structured template
        events = []

        # Try to get from investing.com or similar (simplified)
        url = "https://api.investing.com/economic-calendar"
        # Note: This API may require authentication or may not be publicly available

        # Return placeholder with common recurring events
        today = datetime.now()
        recurring_events = [
            {'name': 'FOMC Meeting', 'frequency': 'Every 6 weeks', 'importance': 'High'},
            {'name': 'Nonfarm Payrolls', 'frequency': 'First Friday monthly', 'importance': 'High'},
            {'name': 'CPI Release', 'frequency': 'Monthly', 'importance': 'High'},
            {'name': 'GDP Release', 'frequency': 'Quarterly', 'importance': 'High'},
            {'name': 'Retail Sales', 'frequency': 'Monthly', 'importance': 'Medium'},
            {'name': 'ISM Manufacturing', 'frequency': 'Monthly', 'importance': 'Medium'}
        ]

        return {
            'note': 'Economic calendar requires premium data source',
            'common_events': recurring_events,
            'recommendation': 'Use investing.com or tradingeconomics.com for detailed calendar'
        }

    def get_china_macro(self) -> Dict:
        """获取中国宏观数据"""
        # Using eastmoney API
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"

        indicators = {}

        # GDP
        try:
            params = {
                'reportName': 'RPT_ECONOMY_GDP',
                'columns': 'ALL',
                'pageSize': 5,
                'sortColumns': 'REPORT_DATE',
                'sortTypes': -1,
                'source': 'WEB'
            }
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()

            if data.get('result', {}).get('data'):
                item = data['result']['data'][0]
                indicators['gdp'] = {
                    'value': item.get('GDP'),
                    'growth_rate': item.get('GDP_YOY'),
                    'date': item.get('REPORT_DATE', '')[:10]
                }
        except Exception:
            pass

        # CPI
        try:
            params = {
                'reportName': 'RPT_ECONOMY_CPI',
                'columns': 'ALL',
                'pageSize': 5,
                'sortColumns': 'REPORT_DATE',
                'sortTypes': -1,
                'source': 'WEB'
            }
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()

            if data.get('result', {}).get('data'):
                item = data['result']['data'][0]
                indicators['cpi'] = {
                    'value': item.get('NATIONAL_SAME'),
                    'mom': item.get('NATIONAL_BASE'),
                    'date': item.get('REPORT_DATE', '')[:10]
                }
        except Exception:
            pass

        # PMI
        try:
            params = {
                'reportName': 'RPT_ECONOMY_PMI',
                'columns': 'ALL',
                'pageSize': 5,
                'sortColumns': 'REPORT_DATE',
                'sortTypes': -1,
                'source': 'WEB'
            }
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()

            if data.get('result', {}).get('data'):
                item = data['result']['data'][0]
                indicators['pmi'] = {
                    'manufacturing': item.get('MAKE_INDEX'),
                    'non_manufacturing': item.get('NMAKE_INDEX'),
                    'date': item.get('REPORT_DATE', '')[:10]
                }
        except Exception:
            pass

        indicators['source'] = 'eastmoney'
        return indicators

    def get_currency_data(self, base: str = 'USD') -> Dict:
        """
        获取汇率数据

        Args:
            base: 基准货币

        Returns:
            汇率数据
        """
        import yfinance as yf

        pairs = {
            'USDCNY': 'CNY=X',
            'USDJPY': 'JPY=X',
            'EURUSD': 'EURUSD=X',
            'GBPUSD': 'GBPUSD=X',
            'USDHKD': 'HKD=X'
        }

        rates = {}
        for name, symbol in pairs.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='5d')
                if not hist.empty:
                    rates[name] = {
                        'rate': round(hist['Close'].iloc[-1], 4),
                        'change': round(hist['Close'].iloc[-1] - hist['Close'].iloc[-2], 4) if len(hist) > 1 else 0
                    }
            except Exception:
                continue

        rates['source'] = 'yahoo_finance'
        return rates

    def get_summary(self) -> Dict:
        """获取宏观经济概览"""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'us': {},
            'china': {},
            'currencies': {}
        }

        # US Data
        if self.fred:
            key_indicators = ['fed_funds_rate', 'unemployment_rate', 'cpi', '10y_treasury']
            for ind in key_indicators:
                data = self.get_indicator(ind)
                if data and 'error' not in data:
                    summary['us'][ind] = {
                        'value': data['latest_value'],
                        'date': data['latest_date']
                    }

        # China Data
        summary['china'] = self.get_china_macro()

        # Currencies
        summary['currencies'] = self.get_currency_data()

        return summary


def main():
    parser = argparse.ArgumentParser(description="Fetch macroeconomic data")
    parser.add_argument("indicator", nargs='?',
                       help="Indicator name or FRED series ID")
    parser.add_argument("--rates", action="store_true",
                       help="Get interest rates")
    parser.add_argument("--inflation", action="store_true",
                       help="Get inflation data")
    parser.add_argument("--employment", action="store_true",
                       help="Get employment data")
    parser.add_argument("--china", action="store_true",
                       help="Get China macro data")
    parser.add_argument("--currency", action="store_true",
                       help="Get currency data")
    parser.add_argument("--summary", action="store_true",
                       help="Get economic summary")
    parser.add_argument("--calendar", action="store_true",
                       help="Get economic calendar")
    parser.add_argument("--list", action="store_true",
                       help="List available indicators")
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="End date (YYYY-MM-DD)")
    parser.add_argument("--api-key", help="FRED API key")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format")

    args = parser.parse_args()

    fetcher = MacroDataFetcher(fred_api_key=args.api_key)

    if args.list:
        data = {'available_indicators': list(fetcher.FRED_SERIES.keys())}
    elif args.rates:
        data = fetcher.get_interest_rates()
    elif args.inflation:
        data = fetcher.get_inflation_data()
    elif args.employment:
        data = fetcher.get_employment_data()
    elif args.china:
        data = fetcher.get_china_macro()
    elif args.currency:
        data = fetcher.get_currency_data()
    elif args.summary:
        data = fetcher.get_summary()
    elif args.calendar:
        data = fetcher.get_economic_calendar()
    elif args.indicator:
        data = fetcher.get_indicator(args.indicator, args.start_date, args.end_date)
    else:
        data = fetcher.get_summary()

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2, default=str))
    else:
        if args.list:
            print("\n=== Available Indicators ===\n")
            for ind in sorted(data['available_indicators']):
                print(f"  {ind}")
        elif isinstance(data, dict):
            print(f"\n=== Macro Economic Data ===\n")
            for k, v in data.items():
                if isinstance(v, dict):
                    print(f"\n{k}:")
                    for k2, v2 in v.items():
                        print(f"  {k2}: {v2}")
                else:
                    print(f"{k}: {v}")
        else:
            print(json.dumps(data, indent=2, default=str))


if __name__ == "__main__":
    main()
