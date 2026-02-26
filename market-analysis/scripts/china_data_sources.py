#!/usr/bin/env python3
"""
China Data Sources for Market Analysis
Provides unified access to Chinese financial data from:
- 东方财富 (East Money)
- 新浪财经 (Sina Finance)
- 巨潮资讯 (CNInfo)
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install requests beautifulsoup4")
    sys.exit(1)


class EastMoneyAPI:
    """
    东方财富数据接口
    Covers: A股, 港股, IPO, 资金流向, 债券, 期货
    """

    BASE_URLS = {
        'push': 'https://push2.eastmoney.com',
        'data': 'https://data.eastmoney.com',
        'datacenter': 'https://datacenter-web.eastmoney.com',
        'quote': 'https://quote.eastmoney.com'
    }

    MARKET_CODES = {
        'sh': 1,   # Shanghai
        'sz': 0,   # Shenzhen
        'hk': 116, # Hong Kong
        'us': 105  # US
    }

    def __init__(self, delay: float = 0.5):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://quote.eastmoney.com/'
        })

    def _request(self, url: str, params: dict = None) -> Optional[dict]:
        """Make API request with error handling."""
        try:
            time.sleep(self.delay)
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            # Handle JSONP response
            text = response.text
            if text.startswith('jQuery') or text.startswith('callback'):
                # Extract JSON from JSONP
                match = re.search(r'\((.*)\)', text, re.DOTALL)
                if match:
                    text = match.group(1)

            return json.loads(text)
        except Exception as e:
            print(f"EastMoney API error: {e}", file=sys.stderr)
            return None

    def get_realtime_quote(self, code: str) -> Optional[Dict]:
        """
        获取实时行情

        Args:
            code: 股票代码 (e.g., '600519' or '600519.SS')

        Returns:
            实时行情数据
        """
        # Parse code and market
        code = code.upper().replace('.SS', '').replace('.SZ', '').replace('.HK', '')

        # Determine market
        if code.startswith('6') or code.startswith('9'):
            market = 1  # Shanghai
            secid = f"1.{code}"
        elif code.startswith(('0', '3', '2')):
            market = 0  # Shenzhen
            secid = f"0.{code}"
        else:
            secid = f"1.{code}"

        url = f"{self.BASE_URLS['push']}/api/qt/stock/get"
        params = {
            'secid': secid,
            'fields': 'f43,f44,f45,f46,f47,f48,f50,f51,f52,f55,f57,f58,f60,f116,f117',
            'ut': 'fa5fd1943c7b386f172d6893dbfba10b'
        }

        data = self._request(url, params)
        if not data or 'data' not in data:
            return None

        d = data['data']
        return {
            'code': d.get('f57', code),
            'name': d.get('f58', ''),
            'current_price': d.get('f43', 0) / 100 if d.get('f43') else None,
            'change': d.get('f169', 0) / 100 if d.get('f169') else None,
            'change_percent': d.get('f170', 0) / 100 if d.get('f170') else None,
            'open': d.get('f46', 0) / 100 if d.get('f46') else None,
            'high': d.get('f44', 0) / 100 if d.get('f44') else None,
            'low': d.get('f45', 0) / 100 if d.get('f45') else None,
            'previous_close': d.get('f60', 0) / 100 if d.get('f60') else None,
            'volume': d.get('f47'),
            'amount': d.get('f48'),
            'market_cap': d.get('f116'),
            'pe_ratio': d.get('f55', 0) / 100 if d.get('f55') else None,
            'source': 'eastmoney'
        }

    def get_ipo_calendar(self, market: str = 'A-SHARE') -> List[Dict]:
        """
        获取IPO日历

        Args:
            market: 市场 ('A-SHARE', 'HK')

        Returns:
            IPO列表
        """
        if market == 'A-SHARE':
            return self._get_a_share_ipo()
        elif market == 'HK':
            return self._get_hk_ipo()
        return []

    def _get_a_share_ipo(self) -> List[Dict]:
        """获取A股IPO日历"""
        url = f"{self.BASE_URLS['datacenter']}/api/data/v1/get"
        params = {
            'reportName': 'RPT_NEEQ_ISSUEINFO_LIST',
            'columns': 'ALL',
            'filter': '',
            'pageNumber': 1,
            'pageSize': 50,
            'sortColumns': 'APPLY_DATE',
            'sortTypes': -1,
            'source': 'WEB'
        }

        data = self._request(url, params)
        if not data or 'result' not in data or 'data' not in data['result']:
            # Try alternative endpoint
            return self._get_a_share_ipo_alt()

        ipo_list = []
        for item in data['result']['data']:
            ipo_list.append({
                'market': 'A-SHARE',
                'code': item.get('SECURITY_CODE', ''),
                'name': item.get('SECURITY_NAME_ABBR', ''),
                'issue_price': item.get('ISSUE_PRICE'),
                'issue_date': item.get('APPLY_DATE', '')[:10] if item.get('APPLY_DATE') else '',
                'list_date': item.get('LIST_DATE', '')[:10] if item.get('LIST_DATE') else '',
                'shares_offered': item.get('ONLINE_ISSUE_NUM'),
                'funds_raised': item.get('PLAN_RAISE_FUND'),
                'pe_ratio': item.get('PE_RATIO'),
                'industry': item.get('INDUSTRY'),
                'underwriter': item.get('LEAD_UNDERWRITER'),
                'source': 'eastmoney'
            })

        return ipo_list

    def _get_a_share_ipo_alt(self) -> List[Dict]:
        """备用A股IPO数据获取方式"""
        # Web scraping fallback
        url = "https://data.eastmoney.com/xg/xg/"
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Parse table data...
            return []
        except Exception:
            return []

    def _get_hk_ipo(self) -> List[Dict]:
        """获取港股IPO日历"""
        url = f"{self.BASE_URLS['datacenter']}/api/data/v1/get"
        params = {
            'reportName': 'RPT_HK_IPOAPPLY',
            'columns': 'ALL',
            'pageNumber': 1,
            'pageSize': 50,
            'sortColumns': 'START_DATE',
            'sortTypes': -1,
            'source': 'WEB'
        }

        data = self._request(url, params)
        if not data or 'result' not in data:
            return []

        ipo_list = []
        for item in data.get('result', {}).get('data', []):
            ipo_list.append({
                'market': 'HK',
                'code': item.get('SECUCODE', '').replace('.HK', ''),
                'name': item.get('SECURITY_NAME_ABBR', ''),
                'issue_price': item.get('ISSUE_PRICE'),
                'subscription_start': item.get('START_DATE', '')[:10] if item.get('START_DATE') else '',
                'subscription_end': item.get('END_DATE', '')[:10] if item.get('END_DATE') else '',
                'list_date': item.get('LIST_DATE', '')[:10] if item.get('LIST_DATE') else '',
                'shares_offered': item.get('PLAN_ISSUE_NUM'),
                'subscription_rate': item.get('SUBSCRIPTION_RATIO'),
                'sponsor': item.get('SPONSOR'),
                'source': 'eastmoney'
            })

        return ipo_list

    def get_fund_flow(self, code: str) -> Optional[Dict]:
        """获取资金流向数据"""
        code = code.upper().replace('.SS', '').replace('.SZ', '')

        if code.startswith('6') or code.startswith('9'):
            secid = f"1.{code}"
        else:
            secid = f"0.{code}"

        url = f"{self.BASE_URLS['push']}/api/qt/stock/fflow/kline/get"
        params = {
            'secid': secid,
            'fields1': 'f1,f2,f3,f7',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57',
            'klt': 1,
            'lmt': 1
        }

        data = self._request(url, params)
        if not data or 'data' not in data:
            return None

        d = data['data']
        if not d or 'klines' not in d:
            return None

        latest = d['klines'][-1].split(',') if d['klines'] else None
        if not latest:
            return None

        return {
            'code': code,
            'date': latest[0],
            'main_inflow': float(latest[1]) if latest[1] != '-' else 0,
            'small_inflow': float(latest[2]) if latest[2] != '-' else 0,
            'medium_inflow': float(latest[3]) if latest[3] != '-' else 0,
            'large_inflow': float(latest[4]) if latest[4] != '-' else 0,
            'super_large_inflow': float(latest[5]) if latest[5] != '-' else 0,
            'source': 'eastmoney'
        }

    def get_bond_yields(self) -> List[Dict]:
        """获取国债收益率数据"""
        url = f"{self.BASE_URLS['datacenter']}/api/data/v1/get"
        params = {
            'reportName': 'RPT_BOND_GOV_YLD',
            'columns': 'ALL',
            'pageNumber': 1,
            'pageSize': 30,
            'sortColumns': 'REPORT_DATE',
            'sortTypes': -1,
            'source': 'WEB'
        }

        data = self._request(url, params)
        if not data or 'result' not in data:
            return []

        yields = []
        for item in data.get('result', {}).get('data', []):
            yields.append({
                'date': item.get('REPORT_DATE', '')[:10],
                'cn_1y': item.get('CN_1Y'),
                'cn_5y': item.get('CN_5Y'),
                'cn_10y': item.get('CN_10Y'),
                'cn_30y': item.get('CN_30Y'),
                'source': 'eastmoney'
            })

        return yields


class SinaFinanceAPI:
    """
    新浪财经数据接口
    Covers: A股, 港股, 美股实时行情
    """

    BASE_URL = 'https://hq.sinajs.cn'

    def __init__(self, delay: float = 0.3):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://finance.sina.com.cn/'
        })

    def _parse_a_share(self, code: str, data: str) -> Optional[Dict]:
        """解析A股数据"""
        if not data or '=' not in data:
            return None

        parts = data.split('=')[1].strip('"').split(',')
        if len(parts) < 32:
            return None

        return {
            'code': code,
            'name': parts[0],
            'open': float(parts[1]) if parts[1] else None,
            'previous_close': float(parts[2]) if parts[2] else None,
            'current_price': float(parts[3]) if parts[3] else None,
            'high': float(parts[4]) if parts[4] else None,
            'low': float(parts[5]) if parts[5] else None,
            'volume': int(float(parts[8])) if parts[8] else None,
            'amount': float(parts[9]) if parts[9] else None,
            'date': parts[30],
            'time': parts[31],
            'source': 'sina'
        }

    def _parse_hk(self, code: str, data: str) -> Optional[Dict]:
        """解析港股数据"""
        if not data or '=' not in data:
            return None

        parts = data.split('=')[1].strip('"').split(',')
        if len(parts) < 17:
            return None

        return {
            'code': code,
            'name_en': parts[0],
            'name_cn': parts[1],
            'open': float(parts[2]) if parts[2] else None,
            'previous_close': float(parts[3]) if parts[3] else None,
            'high': float(parts[4]) if parts[4] else None,
            'low': float(parts[5]) if parts[5] else None,
            'current_price': float(parts[6]) if parts[6] else None,
            'change': float(parts[7]) if parts[7] else None,
            'change_percent': float(parts[8]) if parts[8] else None,
            'volume': int(float(parts[12])) if parts[12] else None,
            'amount': float(parts[11]) if parts[11] else None,
            'source': 'sina'
        }

    def get_realtime_quote(self, codes: List[str]) -> Dict[str, Dict]:
        """
        获取实时行情

        Args:
            codes: 股票代码列表

        Returns:
            Dict mapping code to quote data
        """
        # Build request string
        symbols = []
        code_map = {}

        for code in codes:
            code_upper = code.upper()
            if '.HK' in code_upper or code_upper.startswith('HK'):
                # Hong Kong
                clean_code = code_upper.replace('.HK', '').replace('HK', '').zfill(5)
                symbol = f'hk{clean_code}'
                code_map[symbol] = code
            elif '.SS' in code_upper or code_upper.startswith('6') or code_upper.startswith('9'):
                # Shanghai
                clean_code = code_upper.replace('.SS', '')
                symbol = f'sh{clean_code}'
                code_map[symbol] = code
            elif '.SZ' in code_upper or code_upper.startswith(('0', '3', '2')):
                # Shenzhen
                clean_code = code_upper.replace('.SZ', '')
                symbol = f'sz{clean_code}'
                code_map[symbol] = code
            else:
                # Default to Shanghai
                symbol = f'sh{code}'
                code_map[symbol] = code

            symbols.append(symbol)

        if not symbols:
            return {}

        # Make request
        url = f"{self.BASE_URL}/list={','.join(symbols)}"
        try:
            time.sleep(self.delay)
            response = self.session.get(url, timeout=10)
            response.encoding = 'gbk'  # Sina uses GBK encoding
            lines = response.text.strip().split('\n')
        except Exception as e:
            print(f"Sina API error: {e}", file=sys.stderr)
            return {}

        results = {}
        for line in lines:
            if not line or '=' not in line:
                continue

            # Extract symbol from line
            match = re.search(r'hq_str_(\w+)=', line)
            if not match:
                continue

            symbol = match.group(1)
            original_code = code_map.get(symbol, symbol)

            if symbol.startswith('sh') or symbol.startswith('sz'):
                data = self._parse_a_share(original_code, line)
            elif symbol.startswith('hk'):
                data = self._parse_hk(original_code, line)
            else:
                continue

            if data:
                results[original_code] = data

        return results


class CNInfoAPI:
    """
    巨潮资讯数据接口
    Covers: 招股书, 公告, 财务报表
    """

    BASE_URL = 'http://www.cninfo.com.cn'

    def __init__(self, delay: float = 2.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def search_announcements(self, code: str, category: str = 'IPO') -> List[Dict]:
        """
        搜索公告

        Args:
            code: 股票代码
            category: 公告类别 ('IPO', 'ANNUAL', 'QUARTERLY')

        Returns:
            公告列表
        """
        url = f"{self.BASE_URL}/new/hisAnnouncement/query"

        category_map = {
            'IPO': 'category_ipo_szsh',
            'ANNUAL': 'category_ndbg_szsh',
            'QUARTERLY': 'category_jibg_szsh'
        }

        params = {
            'stock': code,
            'category': category_map.get(category, 'category_ipo_szsh'),
            'pageNum': 1,
            'pageSize': 30,
            'tabName': 'fulltext'
        }

        try:
            time.sleep(self.delay)
            response = self.session.post(url, data=params, timeout=10)
            data = response.json()
        except Exception as e:
            print(f"CNInfo API error: {e}", file=sys.stderr)
            return []

        announcements = []
        for item in data.get('announcements', []):
            announcements.append({
                'code': code,
                'title': item.get('announcementTitle', ''),
                'date': item.get('announcementTime', ''),
                'url': f"{self.BASE_URL}/{item.get('adjunctUrl', '')}",
                'type': item.get('announcementType', ''),
                'source': 'cninfo'
            })

        return announcements


class ChinaDataSource:
    """
    Unified interface for China data sources.
    """

    def __init__(self):
        self.eastmoney = EastMoneyAPI()
        self.sina = SinaFinanceAPI()
        self.cninfo = CNInfoAPI()

    def get_realtime_quote(self, code: str, source: str = 'auto') -> Optional[Dict]:
        """
        获取实时行情

        Args:
            code: 股票代码
            source: 数据源 ('eastmoney', 'sina', 'auto')

        Returns:
            行情数据
        """
        if source == 'auto':
            # Try eastmoney first, fallback to sina
            result = self.eastmoney.get_realtime_quote(code)
            if not result:
                quotes = self.sina.get_realtime_quote([code])
                result = quotes.get(code)
            return result
        elif source == 'eastmoney':
            return self.eastmoney.get_realtime_quote(code)
        elif source == 'sina':
            quotes = self.sina.get_realtime_quote([code])
            return quotes.get(code)
        return None

    def get_batch_quotes(self, codes: List[str], source: str = 'sina') -> Dict[str, Dict]:
        """
        批量获取行情

        Args:
            codes: 股票代码列表
            source: 数据源

        Returns:
            行情数据字典
        """
        if source == 'sina':
            return self.sina.get_realtime_quote(codes)
        else:
            results = {}
            for code in codes:
                data = self.eastmoney.get_realtime_quote(code)
                if data:
                    results[code] = data
            return results

    def get_ipo_calendar(self, market: str = 'A-SHARE') -> List[Dict]:
        """获取IPO日历"""
        return self.eastmoney.get_ipo_calendar(market)

    def get_bond_yields(self) -> List[Dict]:
        """获取国债收益率"""
        return self.eastmoney.get_bond_yields()

    def get_fund_flow(self, code: str) -> Optional[Dict]:
        """获取资金流向"""
        return self.eastmoney.get_fund_flow(code)

    def search_prospectus(self, code: str) -> List[Dict]:
        """搜索招股书"""
        return self.cninfo.search_announcements(code, 'IPO')


# Global instance
_china_source: Optional[ChinaDataSource] = None


def get_china_source() -> ChinaDataSource:
    """Get or create global China data source instance."""
    global _china_source
    if _china_source is None:
        _china_source = ChinaDataSource()
    return _china_source


def main():
    parser = argparse.ArgumentParser(description="China Financial Data Sources")
    parser.add_argument("action", choices=["quote", "ipo", "bonds", "flow", "prospectus"],
                       help="Action to perform")
    parser.add_argument("--code", help="Stock code")
    parser.add_argument("--codes", help="Comma-separated stock codes")
    parser.add_argument("--market", default="A-SHARE", choices=["A-SHARE", "HK"],
                       help="Market for IPO calendar")
    parser.add_argument("--source", default="auto", choices=["auto", "eastmoney", "sina"],
                       help="Data source")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format")

    args = parser.parse_args()

    source = get_china_source()

    if args.action == "quote":
        if args.codes:
            codes = [c.strip() for c in args.codes.split(',')]
            data = source.get_batch_quotes(codes, args.source)
        elif args.code:
            data = source.get_realtime_quote(args.code, args.source)
        else:
            print("Error: --code or --codes required", file=sys.stderr)
            sys.exit(1)

    elif args.action == "ipo":
        data = source.get_ipo_calendar(args.market)

    elif args.action == "bonds":
        data = source.get_bond_yields()

    elif args.action == "flow":
        if not args.code:
            print("Error: --code required", file=sys.stderr)
            sys.exit(1)
        data = source.get_fund_flow(args.code)

    elif args.action == "prospectus":
        if not args.code:
            print("Error: --code required", file=sys.stderr)
            sys.exit(1)
        data = source.search_prospectus(args.code)

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
    else:
        if isinstance(data, list):
            print(f"\n=== Results ({len(data)} items) ===\n")
            for i, item in enumerate(data[:10], 1):
                print(f"{i}. {json.dumps(item, ensure_ascii=False)}")
        elif isinstance(data, dict):
            print(f"\n=== Result ===\n")
            for k, v in data.items():
                print(f"  {k}: {v}")
        else:
            print("No data found")


if __name__ == "__main__":
    main()
