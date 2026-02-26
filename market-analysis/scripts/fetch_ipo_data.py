#!/usr/bin/env python3
"""
IPO Data Fetcher for Market Analysis
Supports A-Share, Hong Kong, and US IPO markets.
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install requests beautifulsoup4")
    sys.exit(1)

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
try:
    from china_data_sources import get_china_source
    from cache_manager import get_cache
    from rate_limiter import get_limiter
except ImportError:
    get_china_source = None
    get_cache = None
    get_limiter = None


class IPODataFetcher:
    """
    Unified IPO data fetcher for multiple markets.

    Markets supported:
    - A-SHARE: China A-shares (Shanghai/Shenzhen)
    - HK: Hong Kong (HKEX)
    - US: United States (NASDAQ/NYSE)
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.cache = get_cache() if get_cache else None
        self.limiter = get_limiter() if get_limiter else None
        self.china_source = get_china_source() if get_china_source else None

    def _request(self, url: str, params: dict = None, source: str = 'default') -> Optional[requests.Response]:
        """Make HTTP request with rate limiting."""
        if self.limiter:
            self.limiter.acquire(source)
        try:
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"Request error: {e}", file=sys.stderr)
            return None

    def get_upcoming_ipos(self, market: str = 'A-SHARE', days: int = 30) -> List[Dict]:
        """
        获取即将上市的IPO列表

        Args:
            market: 市场 ('A-SHARE', 'HK', 'US')
            days: 查询未来天数

        Returns:
            IPO列表
        """
        if market == 'A-SHARE':
            return self._get_a_share_upcoming()
        elif market == 'HK':
            return self._get_hk_upcoming()
        elif market == 'US':
            return self._get_us_upcoming()
        else:
            raise ValueError(f"Unsupported market: {market}")

    def _get_a_share_upcoming(self) -> List[Dict]:
        """获取A股IPO日历"""
        if self.china_source:
            return self.china_source.get_ipo_calendar('A-SHARE')

        # Fallback: scrape from eastmoney
        url = "https://data.eastmoney.com/xg/xg/"
        response = self._request(url, source='eastmoney')
        if not response:
            return []

        ipo_list = []
        soup = BeautifulSoup(response.content, 'html.parser')

        # Parse the IPO table
        table = soup.find('table', {'id': 'dt_1'})
        if table:
            rows = table.find_all('tr')[1:]  # Skip header
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 8:
                    ipo_list.append({
                        'market': 'A-SHARE',
                        'code': cols[0].get_text(strip=True),
                        'name': cols[1].get_text(strip=True),
                        'issue_price': self._parse_number(cols[2].get_text(strip=True)),
                        'issue_date': cols[3].get_text(strip=True),
                        'subscription_start': cols[4].get_text(strip=True),
                        'subscription_end': cols[5].get_text(strip=True),
                        'shares_offered': self._parse_number(cols[6].get_text(strip=True)),
                        'pe_ratio': self._parse_number(cols[7].get_text(strip=True)),
                        'source': 'eastmoney'
                    })

        return ipo_list

    def _get_hk_upcoming(self) -> List[Dict]:
        """获取港股IPO日历"""
        if self.china_source:
            return self.china_source.get_ipo_calendar('HK')

        # Fallback: HKEX disclosure
        url = "https://www.hkexnews.hk/app/appIndex.html?lang=en"
        # This would require more complex scraping
        return []

    def _get_us_upcoming(self) -> List[Dict]:
        """获取美股IPO日历"""
        ipo_list = []

        # Try NASDAQ IPO calendar
        url = "https://api.nasdaq.com/api/ipo/calendar"
        params = {'date': datetime.now().strftime('%Y-%m')}

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }

        try:
            response = self.session.get(url, params=params, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()

                # Parse upcoming IPOs
                for section in ['priced', 'upcoming', 'filed']:
                    for item in data.get('data', {}).get(section, {}).get('rows', []):
                        ipo_list.append({
                            'market': 'US',
                            'code': item.get('proposedTickerSymbol', ''),
                            'name': item.get('companyName', ''),
                            'exchange': item.get('proposedExchange', ''),
                            'issue_price_range': item.get('proposedSharePrice', ''),
                            'shares_offered': self._parse_number(item.get('sharesOffered', '')),
                            'issue_date': item.get('pricedDate', item.get('expectedPriceDate', '')),
                            'status': section,
                            'source': 'nasdaq'
                        })
        except Exception as e:
            print(f"NASDAQ API error: {e}", file=sys.stderr)

        return ipo_list

    def get_ipo_details(self, code: str, market: str = None) -> Optional[Dict]:
        """
        获取单个IPO详情

        Args:
            code: 股票代码
            market: 市场（如果不指定，自动检测）

        Returns:
            IPO详情
        """
        if not market:
            market = self._detect_market(code)

        if market == 'A-SHARE':
            return self._get_a_share_details(code)
        elif market == 'HK':
            return self._get_hk_details(code)
        elif market == 'US':
            return self._get_us_details(code)

        return None

    def _detect_market(self, code: str) -> str:
        """自动检测市场"""
        code = code.upper()
        if '.HK' in code or (code.isdigit() and len(code) == 5):
            return 'HK'
        elif '.SS' in code or '.SZ' in code:
            return 'A-SHARE'
        elif code.isdigit() and len(code) == 6:
            return 'A-SHARE'
        else:
            return 'US'

    def _get_a_share_details(self, code: str) -> Optional[Dict]:
        """获取A股IPO详情"""
        clean_code = code.replace('.SS', '').replace('.SZ', '')

        # Get basic info from eastmoney
        url = f"https://data.eastmoney.com/xg/xg/detail/{clean_code}.html"
        response = self._request(url, source='eastmoney')
        if not response:
            return None

        details = {
            'market': 'A-SHARE',
            'code': code,
            'source': 'eastmoney'
        }

        soup = BeautifulSoup(response.content, 'html.parser')

        # Parse details table
        info_table = soup.find('table', class_='xg_info')
        if info_table:
            for row in info_table.find_all('tr'):
                cols = row.find_all(['th', 'td'])
                for i in range(0, len(cols) - 1, 2):
                    key = cols[i].get_text(strip=True)
                    value = cols[i + 1].get_text(strip=True)
                    details[self._normalize_key(key)] = value

        # Try to get prospectus link
        if self.china_source:
            prospectus = self.china_source.search_prospectus(clean_code)
            if prospectus:
                details['prospectus'] = prospectus[0] if prospectus else None

        return details

    def _get_hk_details(self, code: str) -> Optional[Dict]:
        """获取港股IPO详情"""
        clean_code = code.replace('.HK', '').zfill(5)

        details = {
            'market': 'HK',
            'code': f"{clean_code}.HK",
            'source': 'hkex'
        }

        # HKEX披露易查询需要更复杂的处理
        return details

    def _get_us_details(self, code: str) -> Optional[Dict]:
        """获取美股IPO详情"""
        details = {
            'market': 'US',
            'code': code.upper(),
            'source': 'sec'
        }

        # SEC EDGAR查询
        url = f"https://www.sec.gov/cgi-bin/browse-edgar"
        params = {
            'action': 'getcompany',
            'company': code,
            'type': 'S-1',
            'dateb': '',
            'owner': 'include',
            'count': 10,
            'output': 'atom'
        }

        try:
            response = self.session.get(url, params=params, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                entries = soup.find_all('entry')

                if entries:
                    entry = entries[0]
                    details['s1_filing'] = {
                        'title': entry.find('title').text if entry.find('title') else '',
                        'filed_date': entry.find('updated').text if entry.find('updated') else '',
                        'url': entry.find('link')['href'] if entry.find('link') else ''
                    }
        except Exception as e:
            print(f"SEC EDGAR error: {e}", file=sys.stderr)

        return details

    def get_recent_ipos(self, market: str = 'A-SHARE', days: int = 30) -> List[Dict]:
        """
        获取近期已上市IPO

        Args:
            market: 市场
            days: 查询过去天数

        Returns:
            IPO列表
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        all_ipos = self.get_upcoming_ipos(market)

        # Filter to recently listed ones
        recent = []
        for ipo in all_ipos:
            list_date = ipo.get('list_date', '')
            if list_date:
                try:
                    dt = datetime.strptime(list_date[:10], '%Y-%m-%d')
                    if dt >= cutoff_date and dt <= datetime.now():
                        recent.append(ipo)
                except ValueError:
                    pass

        return recent

    def get_subscription_info(self, code: str, market: str = 'A-SHARE') -> Optional[Dict]:
        """
        获取申购信息

        Args:
            code: 股票代码
            market: 市场

        Returns:
            申购信息
        """
        if market == 'A-SHARE':
            return self._get_a_share_subscription(code)
        elif market == 'HK':
            return self._get_hk_subscription(code)

        return None

    def _get_a_share_subscription(self, code: str) -> Optional[Dict]:
        """获取A股申购信息"""
        clean_code = code.replace('.SS', '').replace('.SZ', '')

        # Try eastmoney API
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        params = {
            'reportName': 'RPT_NEEQ_ISSUEINFO_LIST',
            'filter': f'(SECURITY_CODE="{clean_code}")',
            'columns': 'ALL',
            'source': 'WEB'
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()

            if data.get('result', {}).get('data'):
                item = data['result']['data'][0]
                return {
                    'code': code,
                    'name': item.get('SECURITY_NAME_ABBR', ''),
                    'issue_price': item.get('ISSUE_PRICE'),
                    'subscription_code': item.get('APPLY_CODE'),
                    'subscription_date': item.get('APPLY_DATE', '')[:10] if item.get('APPLY_DATE') else '',
                    'online_issue_num': item.get('ONLINE_ISSUE_NUM'),
                    'subscription_upper_limit': item.get('APPLY_UPPER_LIMIT'),
                    'lottery_rate': item.get('LOTTERY_RATE'),
                    'subscription_funds': item.get('ONLINE_FUNDS'),
                    'source': 'eastmoney'
                }
        except Exception as e:
            print(f"Subscription info error: {e}", file=sys.stderr)

        return None

    def _get_hk_subscription(self, code: str) -> Optional[Dict]:
        """获取港股认购信息"""
        # Would need to scrape from HKEX or financial news sites
        return {
            'code': code,
            'market': 'HK',
            'note': 'HK subscription info requires additional data sources'
        }

    def _parse_number(self, text: str) -> Optional[float]:
        """解析数字字符串"""
        if not text or text == '-' or text == '--':
            return None
        try:
            # Remove common formatting
            cleaned = text.replace(',', '').replace('$', '').replace('¥', '')
            cleaned = cleaned.replace('亿', 'e8').replace('万', 'e4')
            return float(cleaned)
        except ValueError:
            return None

    def _normalize_key(self, key: str) -> str:
        """标准化字段名"""
        key_map = {
            '股票代码': 'code',
            '股票简称': 'name',
            '发行价格': 'issue_price',
            '发行日期': 'issue_date',
            '上市日期': 'list_date',
            '发行数量': 'shares_offered',
            '募集资金': 'funds_raised',
            '发行市盈率': 'pe_ratio',
            '行业市盈率': 'industry_pe',
            '主承销商': 'underwriter',
            '中签率': 'lottery_rate'
        }
        return key_map.get(key, key.lower().replace(' ', '_'))


def main():
    parser = argparse.ArgumentParser(description="Fetch IPO data from multiple markets")
    parser.add_argument("code", nargs='?', help="Stock code (optional)")
    parser.add_argument("--market", choices=["A-SHARE", "HK", "US"], default="A-SHARE",
                       help="Market (default: A-SHARE)")
    parser.add_argument("--upcoming", action="store_true",
                       help="Get upcoming IPOs")
    parser.add_argument("--recent", action="store_true",
                       help="Get recent IPOs")
    parser.add_argument("--details", action="store_true",
                       help="Get IPO details for specific code")
    parser.add_argument("--subscription", action="store_true",
                       help="Get subscription info")
    parser.add_argument("--days", type=int, default=30,
                       help="Days for recent/upcoming (default: 30)")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format")

    args = parser.parse_args()

    fetcher = IPODataFetcher()

    if args.details and args.code:
        data = fetcher.get_ipo_details(args.code, args.market)
    elif args.subscription and args.code:
        data = fetcher.get_subscription_info(args.code, args.market)
    elif args.recent:
        data = fetcher.get_recent_ipos(args.market, args.days)
    elif args.upcoming or not args.code:
        data = fetcher.get_upcoming_ipos(args.market, args.days)
    else:
        data = fetcher.get_ipo_details(args.code, args.market)

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
    else:
        if isinstance(data, list):
            print(f"\n=== {args.market} IPO List ({len(data)} items) ===\n")
            for i, item in enumerate(data[:20], 1):
                print(f"{i}. {item.get('code', 'N/A')} - {item.get('name', 'N/A')}")
                if item.get('issue_price'):
                    print(f"   Issue Price: {item['issue_price']}")
                if item.get('issue_date'):
                    print(f"   Issue Date: {item['issue_date']}")
                if item.get('list_date'):
                    print(f"   List Date: {item['list_date']}")
                print()
        elif isinstance(data, dict):
            print(f"\n=== IPO Details ===\n")
            for k, v in data.items():
                if v is not None:
                    print(f"  {k}: {v}")
        else:
            print("No data found")


if __name__ == "__main__":
    main()
