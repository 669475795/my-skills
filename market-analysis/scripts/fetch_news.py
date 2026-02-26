#!/usr/bin/env python3
"""
Fetch market news for stocks and cryptocurrencies.
Uses multiple sources: RSS feeds, web scraping, and optional NewsAPI.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from urllib.parse import quote

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install requests beautifulsoup4")
    sys.exit(1)


def fetch_yahoo_finance_news(ticker, max_results=10):
    """
    Fetch news from Yahoo Finance for a specific ticker.

    Args:
        ticker: Stock ticker symbol
        max_results: Maximum number of news items to return

    Returns:
        List of news items
    """
    try:
        # Yahoo Finance news URL
        url = f"https://finance.yahoo.com/quote/{ticker}/news"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = []

        # Find news items (HTML structure may change)
        articles = soup.find_all('h3', limit=max_results)

        for article in articles[:max_results]:
            link = article.find('a')
            if link:
                title = link.get_text(strip=True)
                href = link.get('href', '')

                # Make absolute URL
                if href.startswith('/'):
                    href = f"https://finance.yahoo.com{href}"

                news_items.append({
                    'title': title,
                    'url': href,
                    'source': 'Yahoo Finance',
                    'published': 'Recent'
                })

        return news_items

    except Exception as e:
        print(f"Warning: Failed to fetch Yahoo Finance news: {e}", file=sys.stderr)
        return []


def fetch_google_news_rss(query, max_results=10):
    """
    Fetch news from Google News RSS feed.

    Args:
        query: Search query (e.g., "AAPL stock", "Bitcoin")
        max_results: Maximum number of results

    Returns:
        List of news items
    """
    try:
        # Google News RSS feed
        url = f"https://news.google.com/rss/search?q={quote(query)}&hl=en-US&gl=US&ceid=US:en"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item', limit=max_results)

        news_items = []
        for item in items:
            title = item.title.text if item.title else "No title"
            link = item.link.text if item.link else ""
            pub_date = item.pubDate.text if item.pubDate else "Unknown"
            source = item.source.text if item.source else "Google News"

            news_items.append({
                'title': title,
                'url': link,
                'source': source,
                'published': pub_date
            })

        return news_items

    except Exception as e:
        print(f"Warning: Failed to fetch Google News: {e}", file=sys.stderr)
        return []


def fetch_crypto_news(symbol, max_results=10):
    """
    Fetch cryptocurrency news from CoinDesk RSS feed.

    Args:
        symbol: Crypto symbol (e.g., "BTC", "ETH")
        max_results: Maximum number of results

    Returns:
        List of news items
    """
    try:
        # CoinDesk RSS feed
        url = "https://www.coindesk.com/arc/outboundfeeds/rss/"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item', limit=max_results * 2)  # Get more to filter

        news_items = []
        symbol_lower = symbol.lower().replace('-usd', '')

        for item in items:
            title = item.title.text if item.title else ""
            description = item.description.text if item.description else ""

            # Filter for relevant crypto
            if symbol_lower in title.lower() or symbol_lower in description.lower():
                link = item.link.text if item.link else ""
                pub_date = item.pubDate.text if item.pubDate else "Unknown"

                news_items.append({
                    'title': title,
                    'url': link,
                    'source': 'CoinDesk',
                    'published': pub_date
                })

                if len(news_items) >= max_results:
                    break

        return news_items

    except Exception as e:
        print(f"Warning: Failed to fetch crypto news: {e}", file=sys.stderr)
        return []


def fetch_newsapi(query, api_key=None, max_results=10):
    """
    Fetch news from NewsAPI (requires API key).

    Args:
        query: Search query
        api_key: NewsAPI key (get from https://newsapi.org)
        max_results: Maximum number of results

    Returns:
        List of news items
    """
    if not api_key:
        return []

    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': query,
            'apiKey': api_key,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': max_results
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        news_items = []

        for article in data.get('articles', []):
            news_items.append({
                'title': article.get('title', ''),
                'url': article.get('url', ''),
                'source': article.get('source', {}).get('name', 'NewsAPI'),
                'published': article.get('publishedAt', ''),
                'description': article.get('description', '')
            })

        return news_items

    except Exception as e:
        print(f"Warning: Failed to fetch NewsAPI: {e}", file=sys.stderr)
        return []


def get_stock_news(ticker, sources=['yahoo', 'google'], max_results=10, newsapi_key=None):
    """
    Aggregate news from multiple sources for a stock.

    Args:
        ticker: Stock ticker
        sources: List of sources to use
        max_results: Max results per source
        newsapi_key: Optional NewsAPI key

    Returns:
        Dictionary with news from each source
    """
    results = {'ticker': ticker, 'news': {}, 'total': 0}

    if 'yahoo' in sources:
        yahoo_news = fetch_yahoo_finance_news(ticker, max_results)
        if yahoo_news:
            results['news']['Yahoo Finance'] = yahoo_news
            results['total'] += len(yahoo_news)

    if 'google' in sources:
        query = f"{ticker} stock news"
        google_news = fetch_google_news_rss(query, max_results)
        if google_news:
            results['news']['Google News'] = google_news
            results['total'] += len(google_news)

    if 'newsapi' in sources and newsapi_key:
        newsapi_news = fetch_newsapi(f"{ticker} stock", newsapi_key, max_results)
        if newsapi_news:
            results['news']['NewsAPI'] = newsapi_news
            results['total'] += len(newsapi_news)

    return results


def get_crypto_news(symbol, sources=['coindesk', 'google'], max_results=10):
    """
    Aggregate crypto news from multiple sources.

    Args:
        symbol: Crypto symbol
        sources: List of sources
        max_results: Max results per source

    Returns:
        Dictionary with news from each source
    """
    results = {'symbol': symbol, 'news': {}, 'total': 0}

    # Clean symbol
    crypto_name = symbol.replace('-USD', '').upper()

    if 'coindesk' in sources:
        coindesk_news = fetch_crypto_news(symbol, max_results)
        if coindesk_news:
            results['news']['CoinDesk'] = coindesk_news
            results['total'] += len(coindesk_news)

    if 'google' in sources:
        query = f"{crypto_name} cryptocurrency news"
        google_news = fetch_google_news_rss(query, max_results)
        if google_news:
            results['news']['Google News'] = google_news
            results['total'] += len(google_news)

    return results


def main():
    parser = argparse.ArgumentParser(description="Fetch market news")
    parser.add_argument("symbol", help="Stock ticker or crypto symbol")
    parser.add_argument("--type", choices=["stock", "crypto"], default="stock",
                       help="Asset type (default: stock)")
    parser.add_argument("--sources", default="yahoo,google",
                       help="Comma-separated list of sources (default: yahoo,google)")
    parser.add_argument("--max-results", type=int, default=10,
                       help="Max results per source (default: 10)")
    parser.add_argument("--newsapi-key", help="Optional NewsAPI key")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format (default: text)")

    args = parser.parse_args()

    # Parse sources
    sources = [s.strip().lower() for s in args.sources.split(",")]

    # Fetch news
    if args.type == "crypto":
        results = get_crypto_news(args.symbol, sources, args.max_results)
    else:
        results = get_stock_news(args.symbol, sources, args.max_results, args.newsapi_key)

    # Output results
    if args.output == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        # Text output
        asset_name = results.get('ticker') or results.get('symbol')
        print(f"\n=== News for {asset_name} ===\n")
        print(f"Total articles found: {results['total']}\n")

        if results['total'] == 0:
            print("No news found. Try different sources or check your internet connection.")
        else:
            for source_name, articles in results['news'].items():
                print(f"--- {source_name} ({len(articles)} articles) ---\n")

                for i, article in enumerate(articles, 1):
                    print(f"{i}. {article['title']}")
                    print(f"   Source: {article['source']}")
                    print(f"   Published: {article['published']}")
                    print(f"   URL: {article['url']}")
                    if article.get('description'):
                        print(f"   {article['description'][:150]}...")
                    print()


if __name__ == "__main__":
    main()
