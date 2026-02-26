#!/usr/bin/env python3
"""
Fetch real-time cryptocurrency data from CoinGecko API.
Free API with 1-2 minute delay (better than Yahoo's 15 minutes).
No API key required for basic usage.
"""

import argparse
import json
import sys
from datetime import datetime

try:
    import requests
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install requests")
    sys.exit(1)


# CoinGecko API base URL
COINGECKO_API = "https://api.coingecko.com/api/v3"

# Common crypto ID mappings
CRYPTO_IDS = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'BNB': 'binancecoin',
    'XRP': 'ripple',
    'ADA': 'cardano',
    'DOGE': 'dogecoin',
    'SOL': 'solana',
    'DOT': 'polkadot',
    'MATIC': 'matic-network',
    'LTC': 'litecoin',
    'AVAX': 'avalanche-2',
    'LINK': 'chainlink',
    'UNI': 'uniswap',
    'ATOM': 'cosmos',
    'XLM': 'stellar',
    'USDT': 'tether',
    'USDC': 'usd-coin',
}


def normalize_symbol(symbol):
    """Convert symbol to CoinGecko ID."""
    symbol = symbol.upper().replace('-USD', '').replace('-BTC', '')

    if symbol in CRYPTO_IDS:
        return CRYPTO_IDS[symbol]

    # Try lowercase as fallback
    return symbol.lower()


def fetch_crypto_price(coin_id, vs_currency='usd'):
    """
    Fetch current price and basic info for a cryptocurrency.

    Args:
        coin_id: CoinGecko coin ID (e.g., 'bitcoin')
        vs_currency: Currency to show price in (default: 'usd')

    Returns:
        Dictionary with price data
    """
    try:
        url = f"{COINGECKO_API}/simple/price"
        params = {
            'ids': coin_id,
            'vs_currencies': vs_currency,
            'include_market_cap': 'true',
            'include_24hr_vol': 'true',
            'include_24hr_change': 'true',
            'include_last_updated_at': 'true'
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if coin_id not in data:
            return {'error': f'Coin {coin_id} not found'}

        coin_data = data[coin_id]

        # Convert timestamp to readable format
        last_updated = datetime.fromtimestamp(coin_data.get('last_updated_at', 0))

        return {
            'coin_id': coin_id,
            'price': coin_data.get(vs_currency),
            'market_cap': coin_data.get(f'{vs_currency}_market_cap'),
            'volume_24h': coin_data.get(f'{vs_currency}_24h_vol'),
            'change_24h': coin_data.get(f'{vs_currency}_24h_change'),
            'currency': vs_currency.upper(),
            'last_updated': last_updated.strftime('%Y-%m-%d %H:%M:%S UTC'),
            'data_freshness': 'Real-time (1-2 min delay)'
        }

    except Exception as e:
        return {'error': f'Failed to fetch data: {str(e)}'}


def fetch_crypto_details(coin_id):
    """
    Fetch detailed information about a cryptocurrency.

    Args:
        coin_id: CoinGecko coin ID

    Returns:
        Dictionary with detailed data
    """
    try:
        url = f"{COINGECKO_API}/coins/{coin_id}"
        params = {
            'localization': 'false',
            'tickers': 'false',
            'community_data': 'true',
            'developer_data': 'false'
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        market_data = data.get('market_data', {})

        return {
            'name': data.get('name'),
            'symbol': data.get('symbol', '').upper(),
            'rank': data.get('market_cap_rank'),
            'price_usd': market_data.get('current_price', {}).get('usd'),
            'market_cap_usd': market_data.get('market_cap', {}).get('usd'),
            'total_volume_usd': market_data.get('total_volume', {}).get('usd'),
            'circulating_supply': market_data.get('circulating_supply'),
            'total_supply': market_data.get('total_supply'),
            'max_supply': market_data.get('max_supply'),
            'ath': market_data.get('ath', {}).get('usd'),
            'ath_change_percentage': market_data.get('ath_change_percentage', {}).get('usd'),
            'atl': market_data.get('atl', {}).get('usd'),
            'atl_change_percentage': market_data.get('atl_change_percentage', {}).get('usd'),
            'price_change_24h': market_data.get('price_change_24h'),
            'price_change_percentage_24h': market_data.get('price_change_percentage_24h'),
            'price_change_percentage_7d': market_data.get('price_change_percentage_7d'),
            'price_change_percentage_30d': market_data.get('price_change_percentage_30d'),
            'last_updated': data.get('last_updated'),
        }

    except Exception as e:
        return {'error': f'Failed to fetch details: {str(e)}'}


def fetch_market_chart(coin_id, days=30, vs_currency='usd'):
    """
    Fetch historical price chart data.

    Args:
        coin_id: CoinGecko coin ID
        days: Number of days of historical data
        vs_currency: Currency

    Returns:
        Dictionary with price history
    """
    try:
        url = f"{COINGECKO_API}/coins/{coin_id}/market_chart"
        params = {
            'vs_currency': vs_currency,
            'days': days
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Convert timestamps to dates
        prices = data.get('prices', [])
        formatted_prices = []

        for timestamp, price in prices[-10:]:  # Last 10 data points
            date = datetime.fromtimestamp(timestamp / 1000)
            formatted_prices.append({
                'date': date.strftime('%Y-%m-%d %H:%M'),
                'price': round(price, 2)
            })

        return {
            'coin_id': coin_id,
            'period_days': days,
            'data_points': len(prices),
            'recent_prices': formatted_prices
        }

    except Exception as e:
        return {'error': f'Failed to fetch chart data: {str(e)}'}


def compare_cryptos(coin_ids, vs_currency='usd'):
    """
    Compare multiple cryptocurrencies.

    Args:
        coin_ids: List of CoinGecko coin IDs
        vs_currency: Currency

    Returns:
        Dictionary with comparison data
    """
    try:
        url = f"{COINGECKO_API}/simple/price"
        params = {
            'ids': ','.join(coin_ids),
            'vs_currencies': vs_currency,
            'include_market_cap': 'true',
            'include_24hr_vol': 'true',
            'include_24hr_change': 'true'
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = {}

        for coin_id in coin_ids:
            if coin_id in data:
                coin_data = data[coin_id]
                results[coin_id] = {
                    'price': coin_data.get(vs_currency),
                    'market_cap': coin_data.get(f'{vs_currency}_market_cap'),
                    'volume_24h': coin_data.get(f'{vs_currency}_24h_vol'),
                    'change_24h': coin_data.get(f'{vs_currency}_24h_change'),
                }

        return results

    except Exception as e:
        return {'error': f'Failed to compare: {str(e)}'}


def main():
    parser = argparse.ArgumentParser(description="Fetch real-time crypto data from CoinGecko")
    parser.add_argument("symbol", help="Crypto symbol (e.g., BTC, ETH) or coin ID")
    parser.add_argument("--detailed", action="store_true",
                       help="Fetch detailed information")
    parser.add_argument("--chart", type=int, metavar="DAYS",
                       help="Fetch price chart for N days")
    parser.add_argument("--compare", help="Compare with other cryptos (comma-separated)")
    parser.add_argument("--currency", default="usd",
                       help="Currency to show prices in (default: usd)")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format (default: text)")

    args = parser.parse_args()

    # Normalize symbol to coin ID
    coin_id = normalize_symbol(args.symbol)

    # Fetch data based on options
    if args.compare:
        # Compare mode
        compare_ids = [coin_id] + [normalize_symbol(s.strip()) for s in args.compare.split(',')]
        data = compare_cryptos(compare_ids, args.currency)
    elif args.detailed:
        # Detailed mode
        data = fetch_crypto_details(coin_id)
    elif args.chart:
        # Chart mode
        data = fetch_market_chart(coin_id, args.chart, args.currency)
    else:
        # Simple price mode
        data = fetch_crypto_price(coin_id, args.currency)

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2))
    else:
        # Text output
        if 'error' in data:
            print(f"Error: {data['error']}")
            sys.exit(1)

        if args.compare:
            print("\n=== Cryptocurrency Comparison ===\n")
            for cid, info in data.items():
                print(f"{cid.upper()}:")
                print(f"  Price: ${info['price']:,.2f}")
                print(f"  24h Change: {info['change_24h']:+.2f}%")
                print(f"  Market Cap: ${info['market_cap']:,.0f}")
                print(f"  24h Volume: ${info['volume_24h']:,.0f}")
                print()

        elif args.detailed:
            print(f"\n=== {data['name']} ({data['symbol']}) ===\n")
            print(f"Rank: #{data['rank']}")
            print(f"Price: ${data['price_usd']:,.2f}")
            print(f"Market Cap: ${data['market_cap_usd']:,.0f}")
            print(f"24h Volume: ${data['total_volume_usd']:,.0f}")
            print(f"\n24h Change: {data['price_change_percentage_24h']:+.2f}%")
            print(f"7d Change: {data.get('price_change_percentage_7d', 0):+.2f}%")
            print(f"30d Change: {data.get('price_change_percentage_30d', 0):+.2f}%")
            print(f"\nCirculating Supply: {data['circulating_supply']:,.0f} {data['symbol']}")
            if data.get('total_supply'):
                print(f"Total Supply: {data['total_supply']:,.0f} {data['symbol']}")
            if data.get('max_supply'):
                print(f"Max Supply: {data['max_supply']:,.0f} {data['symbol']}")
            print(f"\nAll-Time High: ${data['ath']:,.2f} ({data['ath_change_percentage']:+.2f}% from ATH)")
            print(f"All-Time Low: ${data['atl']:,.2f} ({data['atl_change_percentage']:+.2f}% from ATL)")
            print(f"\nLast Updated: {data['last_updated']}")

        elif args.chart:
            print(f"\n=== {coin_id.upper()} Price Chart ({args.chart} days) ===\n")
            print(f"Total data points: {data['data_points']}\n")
            print("Recent prices:")
            for point in data['recent_prices']:
                print(f"  {point['date']}: ${point['price']:,.2f}")

        else:
            print(f"\n=== {coin_id.upper()} Real-Time Price ===\n")
            print(f"Price: ${data['price']:,.2f} {data['currency']}")
            print(f"24h Change: {data['change_24h']:+.2f}%")
            print(f"Market Cap: ${data['market_cap']:,.0f}")
            print(f"24h Volume: ${data['volume_24h']:,.0f}")
            print(f"\nData Freshness: {data['data_freshness']}")
            print(f"Last Updated: {data['last_updated']}")


if __name__ == "__main__":
    main()
