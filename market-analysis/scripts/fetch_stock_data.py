#!/usr/bin/env python3
"""
Fetch stock market data using yfinance.
Supports US stocks, Hong Kong stocks, and China A-shares.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
import pytz

try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install yfinance pandas pytz")
    sys.exit(1)


def fetch_stock_data(ticker, period="1mo", interval="1d", metrics=False):
    """
    Fetch stock data for a given ticker.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', '00700.HK', '600519.SS')
        period: Data period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
        interval: Data interval ('1m', '5m', '15m', '1h', '1d', '1wk', '1mo')
        metrics: Include fundamental metrics

    Returns:
        Dictionary containing stock data
    """
    try:
        stock = yf.Ticker(ticker)

        # Fetch historical data
        hist = stock.history(period=period, interval=interval)

        if hist.empty:
            return {"error": f"No data available for ticker {ticker}"}

        # Get current info
        info = stock.info

        # Get current time and market time
        fetch_time = datetime.now(pytz.UTC)
        last_data_point = hist.index[-1]

        # Prepare response
        result = {
            "ticker": ticker,
            "name": info.get("longName", ticker),
            "currency": info.get("currency", "USD"),
            "exchange": info.get("exchange", "Unknown"),
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "previous_close": info.get("previousClose") or info.get("regularMarketPreviousClose"),
            "open": info.get("open") or info.get("regularMarketOpen"),
            "day_high": info.get("dayHigh") or info.get("regularMarketDayHigh"),
            "day_low": info.get("dayLow") or info.get("regularMarketDayLow"),
            "volume": info.get("volume") or info.get("regularMarketVolume"),
            "market_cap": info.get("marketCap"),
            "data_points": len(hist),
            "period": period,
            "interval": interval,
            "data_timestamp": {
                "fetched_at": fetch_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "last_data_point": last_data_point.strftime("%Y-%m-%d %H:%M:%S"),
                "data_delay": "~15 minutes during market hours",
                "source": "Yahoo Finance"
            }
        }

        # Calculate change
        if result["current_price"] and result["previous_close"]:
            change = result["current_price"] - result["previous_close"]
            change_pct = (change / result["previous_close"]) * 100
            result["change"] = round(change, 2)
            result["change_percent"] = round(change_pct, 2)

        # Add fundamental metrics if requested
        if metrics:
            result["metrics"] = {
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "pb_ratio": info.get("priceToBook"),
                "ps_ratio": info.get("priceToSalesTrailing12Months"),
                "dividend_yield": info.get("dividendYield"),
                "beta": info.get("beta"),
                "52_week_high": info.get("fiftyTwoWeekHigh"),
                "52_week_low": info.get("fiftyTwoWeekLow"),
                "50_day_avg": info.get("fiftyDayAverage"),
                "200_day_avg": info.get("twoHundredDayAverage"),
                "earnings_date": info.get("earningsDate"),
                "analyst_rating": info.get("recommendationKey"),
                "target_price": info.get("targetMeanPrice"),
            }

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
        }

        return result

    except Exception as e:
        return {"error": f"Failed to fetch data for {ticker}: {str(e)}"}


def compare_stocks(tickers, period="1mo"):
    """
    Compare multiple stocks side by side.

    Args:
        tickers: List of ticker symbols
        period: Data period

    Returns:
        Dictionary with comparison data
    """
    results = {}

    for ticker in tickers:
        data = fetch_stock_data(ticker, period=period, metrics=True)
        if "error" not in data:
            results[ticker] = {
                "name": data["name"],
                "current_price": data["current_price"],
                "change_percent": data.get("change_percent"),
                "market_cap": data.get("market_cap"),
                "pe_ratio": data.get("metrics", {}).get("pe_ratio"),
                "volume": data["volume"],
                "volatility": data["statistics"]["price_volatility"],
            }
        else:
            results[ticker] = data

    return results


def main():
    parser = argparse.ArgumentParser(description="Fetch stock market data")
    parser.add_argument("ticker", help="Stock ticker symbol(s), comma-separated for comparison")
    parser.add_argument("--period", default="1mo",
                       choices=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"],
                       help="Data period (default: 1mo)")
    parser.add_argument("--interval", default="1d",
                       choices=["1m", "5m", "15m", "1h", "1d", "1wk", "1mo"],
                       help="Data interval (default: 1d)")
    parser.add_argument("--metrics", action="store_true",
                       help="Include fundamental metrics")
    parser.add_argument("--compare", action="store_true",
                       help="Compare multiple stocks")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format (default: text)")

    args = parser.parse_args()

    # Parse tickers
    tickers = [t.strip().upper() for t in args.ticker.split(",")]

    # Fetch data
    if args.compare and len(tickers) > 1:
        data = compare_stocks(tickers, period=args.period)
    elif len(tickers) == 1:
        data = fetch_stock_data(tickers[0], period=args.period,
                               interval=args.interval, metrics=args.metrics)
    else:
        data = {"error": "Use --compare flag for multiple tickers"}

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
            print("\n=== Stock Comparison ===\n")
            for ticker, info in data.items():
                if "error" in info:
                    print(f"{ticker}: {info['error']}")
                else:
                    print(f"{ticker} ({info['name']})")
                    print(f"  Price: ${info['current_price']:.2f} ({info['change_percent']:+.2f}%)")
                    if info.get('pe_ratio'):
                        print(f"  P/E Ratio: {info['pe_ratio']:.2f}")
                    if info.get('market_cap'):
                        print(f"  Market Cap: ${info['market_cap']:,.0f}")
                    print(f"  Volatility: {info['volatility']:.2f}%")
                    print()
        else:
            # Single stock output
            print(f"\n=== {data['name']} ({data['ticker']}) ===\n")
            print(f"Exchange: {data['exchange']}")
            print(f"Currency: {data['currency']}")
            print(f"\nCurrent Price: ${data['current_price']:.2f}")
            if data.get('change'):
                print(f"Change: ${data['change']:+.2f} ({data['change_percent']:+.2f}%)")
            print(f"Volume: {data['volume']:,}")

            if data.get('market_cap'):
                print(f"Market Cap: ${data['market_cap']:,.0f}")

            print(f"\nDay Range: ${data['day_low']:.2f} - ${data['day_high']:.2f}")
            print(f"Period Range: ${data['statistics']['period_low']:.2f} - ${data['statistics']['period_high']:.2f}")
            print(f"Volatility: {data['statistics']['price_volatility']:.2f}%")

            if args.metrics and data.get('metrics'):
                m = data['metrics']
                print("\n=== Fundamental Metrics ===")
                if m.get('pe_ratio'):
                    print(f"P/E Ratio: {m['pe_ratio']:.2f}")
                if m.get('pb_ratio'):
                    print(f"P/B Ratio: {m['pb_ratio']:.2f}")
                if m.get('dividend_yield'):
                    print(f"Dividend Yield: {m['dividend_yield']*100:.2f}%")
                if m.get('beta'):
                    print(f"Beta: {m['beta']:.2f}")
                if m.get('52_week_high') and m.get('52_week_low'):
                    print(f"52-Week Range: ${m['52_week_low']:.2f} - ${m['52_week_high']:.2f}")
                if m.get('analyst_rating'):
                    print(f"Analyst Rating: {m['analyst_rating']}")
                if m.get('target_price'):
                    print(f"Target Price: ${m['target_price']:.2f}")

            print(f"\n=== Recent History ({data['period']}) ===")
            history = data['recent_history']
            for i in range(len(history['dates'])):
                print(f"{history['dates'][i]}: ${history['close'][i]:.2f} "
                      f"(H: ${history['high'][i]:.2f}, L: ${history['low'][i]:.2f})")

            # Show data timestamp info
            if data.get('data_timestamp'):
                ts = data['data_timestamp']
                print(f"\n=== Data Information ===")
                print(f"Fetched at: {ts['fetched_at']}")
                print(f"Last data point: {ts['last_data_point']}")
                print(f"Data delay: {ts['data_delay']}")
                print(f"Source: {ts['source']}")


if __name__ == "__main__":
    main()
