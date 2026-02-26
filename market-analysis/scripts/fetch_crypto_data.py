#!/usr/bin/env python3
"""
Fetch cryptocurrency market data using yfinance.
Supports major cryptocurrencies via Yahoo Finance.
"""

import argparse
import json
import sys

try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install yfinance pandas")
    sys.exit(1)


# Common cryptocurrency symbols
CRYPTO_SYMBOLS = {
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "BNB": "BNB-USD",
    "XRP": "XRP-USD",
    "ADA": "ADA-USD",
    "DOGE": "DOGE-USD",
    "SOL": "SOL-USD",
    "DOT": "DOT-USD",
    "MATIC": "MATIC-USD",
    "LTC": "LTC-USD",
    "AVAX": "AVAX-USD",
    "LINK": "LINK-USD",
    "UNI": "UNI-USD",
    "ATOM": "ATOM-USD",
}


def normalize_symbol(symbol):
    """Normalize cryptocurrency symbol to Yahoo Finance format."""
    symbol = symbol.upper()

    # If already in correct format
    if "-USD" in symbol:
        return symbol

    # If short form
    if symbol in CRYPTO_SYMBOLS:
        return CRYPTO_SYMBOLS[symbol]

    # Add -USD suffix
    return f"{symbol}-USD"


def fetch_crypto_data(symbol, period="1mo", interval="1d"):
    """
    Fetch cryptocurrency data.

    Args:
        symbol: Crypto symbol (e.g., 'BTC', 'BTC-USD', 'ETH')
        period: Data period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
        interval: Data interval ('1m', '5m', '15m', '1h', '1d', '1wk', '1mo')

    Returns:
        Dictionary containing crypto data
    """
    try:
        symbol = normalize_symbol(symbol)
        crypto = yf.Ticker(symbol)

        # Fetch historical data
        hist = crypto.history(period=period, interval=interval)

        if hist.empty:
            return {"error": f"No data available for {symbol}"}

        # Get current info
        info = crypto.info

        # Prepare response
        result = {
            "symbol": symbol,
            "name": info.get("longName", symbol.replace("-USD", "")),
            "currency": "USD",
            "current_price": info.get("regularMarketPrice"),
            "previous_close": info.get("previousClose"),
            "open": info.get("open"),
            "day_high": info.get("dayHigh"),
            "day_low": info.get("dayLow"),
            "volume": info.get("volume"),
            "market_cap": info.get("marketCap"),
            "circulating_supply": info.get("circulatingSupply"),
            "data_points": len(hist),
            "period": period,
            "interval": interval,
        }

        # Calculate change
        if result["current_price"] and result["previous_close"]:
            change = result["current_price"] - result["previous_close"]
            change_pct = (change / result["previous_close"]) * 100
            result["change"] = round(change, 2)
            result["change_percent"] = round(change_pct, 2)

        # Add recent price history
        recent_data = hist.tail(10)
        result["recent_history"] = {
            "dates": recent_data.index.strftime("%Y-%m-%d").tolist(),
            "close": recent_data["Close"].round(2).tolist(),
            "volume": recent_data["Volume"].tolist(),
            "high": recent_data["High"].round(2).tolist(),
            "low": recent_data["Low"].round(2).tolist(),
        }

        # Add price statistics
        result["statistics"] = {
            "period_high": round(hist["High"].max(), 2),
            "period_low": round(hist["Low"].min(), 2),
            "avg_volume": int(hist["Volume"].mean()),
            "price_volatility": round(hist["Close"].pct_change().std() * 100, 2),
            "price_range": round(((hist["High"].max() - hist["Low"].min()) / hist["Low"].min()) * 100, 2),
        }

        # Calculate returns
        period_return = ((hist["Close"].iloc[-1] - hist["Close"].iloc[0]) / hist["Close"].iloc[0]) * 100
        result["statistics"]["period_return"] = round(period_return, 2)

        return result

    except Exception as e:
        return {"error": f"Failed to fetch data for {symbol}: {str(e)}"}


def compare_cryptos(symbols, period="1mo"):
    """
    Compare multiple cryptocurrencies.

    Args:
        symbols: List of crypto symbols
        period: Data period

    Returns:
        Dictionary with comparison data
    """
    results = {}

    for symbol in symbols:
        data = fetch_crypto_data(symbol, period=period)
        if "error" not in data:
            results[symbol] = {
                "name": data["name"],
                "current_price": data["current_price"],
                "change_percent": data.get("change_percent"),
                "market_cap": data.get("market_cap"),
                "volume": data["volume"],
                "volatility": data["statistics"]["price_volatility"],
                "period_return": data["statistics"]["period_return"],
            }
        else:
            results[symbol] = data

    return results


def main():
    parser = argparse.ArgumentParser(description="Fetch cryptocurrency market data")
    parser.add_argument("symbol", help="Crypto symbol(s), comma-separated for comparison (e.g., BTC, ETH)")
    parser.add_argument("--period", default="1mo",
                       choices=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"],
                       help="Data period (default: 1mo)")
    parser.add_argument("--interval", default="1d",
                       choices=["1m", "5m", "15m", "1h", "1d", "1wk", "1mo"],
                       help="Data interval (default: 1d)")
    parser.add_argument("--compare", action="store_true",
                       help="Compare multiple cryptocurrencies")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format (default: text)")

    args = parser.parse_args()

    # Parse symbols
    symbols = [s.strip().upper() for s in args.symbol.split(",")]

    # Fetch data
    if args.compare and len(symbols) > 1:
        data = compare_cryptos(symbols, period=args.period)
    elif len(symbols) == 1:
        data = fetch_crypto_data(symbols[0], period=args.period, interval=args.interval)
    else:
        data = {"error": "Use --compare flag for multiple symbols"}

    # Output results
    if args.output == "json":
        print(json.dumps(data, indent=2, default=str))
    else:
        # Text output
        if "error" in data:
            print(f"Error: {data['error']}")
            sys.exit(1)

        if args.compare:
            # Comparison output
            print("\n=== Cryptocurrency Comparison ===\n")
            for symbol, info in data.items():
                if "error" in info:
                    print(f"{symbol}: {info['error']}")
                else:
                    print(f"{symbol} ({info['name']})")
                    print(f"  Price: ${info['current_price']:,.2f} ({info['change_percent']:+.2f}%)")
                    if info.get('market_cap'):
                        print(f"  Market Cap: ${info['market_cap']:,.0f}")
                    print(f"  Period Return: {info['period_return']:+.2f}%")
                    print(f"  Volatility: {info['volatility']:.2f}%")
                    print()
        else:
            # Single crypto output
            print(f"\n=== {data['name']} ({data['symbol']}) ===\n")

            print(f"Current Price: ${data['current_price']:,.2f}")
            if data.get('change'):
                print(f"Change: ${data['change']:+,.2f} ({data['change_percent']:+.2f}%)")
            print(f"Volume (24h): {data['volume']:,.0f}")

            if data.get('market_cap'):
                print(f"Market Cap: ${data['market_cap']:,.0f}")

            if data.get('circulating_supply'):
                print(f"Circulating Supply: {data['circulating_supply']:,.0f}")

            stats = data['statistics']
            print(f"\nDay Range: ${data['day_low']:,.2f} - ${data['day_high']:,.2f}")
            print(f"Period Range: ${stats['period_low']:,.2f} - ${stats['period_high']:,.2f}")
            print(f"Period Return: {stats['period_return']:+.2f}%")
            print(f"Volatility: {stats['price_volatility']:.2f}%")

            print(f"\n=== Recent History ({data['period']}) ===")
            history = data['recent_history']
            for i in range(len(history['dates'])):
                print(f"{history['dates'][i]}: ${history['close'][i]:,.2f} "
                      f"(H: ${history['high'][i]:,.2f}, L: ${history['low'][i]:,.2f})")


if __name__ == "__main__":
    main()
