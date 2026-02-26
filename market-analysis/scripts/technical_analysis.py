#!/usr/bin/env python3
"""
Perform technical analysis on stock or cryptocurrency data.
Calculates common technical indicators and generates trading signals.
"""

import argparse
import json
import sys

try:
    import yfinance as yf
    import pandas as pd
    import numpy as np
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install yfinance pandas numpy")
    sys.exit(1)


def calculate_sma(data, periods=[20, 50, 200]):
    """Calculate Simple Moving Averages."""
    result = {}
    for period in periods:
        if len(data) >= period:
            result[f"SMA_{period}"] = data["Close"].rolling(window=period).mean().iloc[-1]
    return result


def calculate_ema(data, periods=[12, 26]):
    """Calculate Exponential Moving Averages."""
    result = {}
    for period in periods:
        if len(data) >= period:
            result[f"EMA_{period}"] = data["Close"].ewm(span=period, adjust=False).mean().iloc[-1]
    return result


def calculate_rsi(data, period=14):
    """Calculate Relative Strength Index."""
    if len(data) < period + 1:
        return None

    delta = data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi.iloc[-1]


def calculate_macd(data):
    """Calculate MACD (Moving Average Convergence Divergence)."""
    if len(data) < 26:
        return None

    ema_12 = data["Close"].ewm(span=12, adjust=False).mean()
    ema_26 = data["Close"].ewm(span=26, adjust=False).mean()
    macd_line = ema_12 - ema_26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal_line

    return {
        "MACD": macd_line.iloc[-1],
        "Signal": signal_line.iloc[-1],
        "Histogram": histogram.iloc[-1],
    }


def calculate_bollinger_bands(data, period=20, std_dev=2):
    """Calculate Bollinger Bands."""
    if len(data) < period:
        return None

    sma = data["Close"].rolling(window=period).mean()
    std = data["Close"].rolling(window=period).std()

    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)

    current_price = data["Close"].iloc[-1]

    return {
        "Upper": upper_band.iloc[-1],
        "Middle": sma.iloc[-1],
        "Lower": lower_band.iloc[-1],
        "Current": current_price,
        "Position": ((current_price - lower_band.iloc[-1]) / (upper_band.iloc[-1] - lower_band.iloc[-1])) * 100,
    }


def analyze_volume(data):
    """Analyze volume trends."""
    if len(data) < 20:
        return None

    avg_volume = data["Volume"].rolling(window=20).mean().iloc[-1]
    current_volume = data["Volume"].iloc[-1]
    volume_ratio = current_volume / avg_volume

    return {
        "Current": current_volume,
        "Avg_20d": avg_volume,
        "Ratio": volume_ratio,
        "Trend": "High" if volume_ratio > 1.5 else "Normal" if volume_ratio > 0.5 else "Low",
    }


def generate_signals(data, indicators):
    """Generate trading signals based on technical indicators."""
    signals = {"Overall": "NEUTRAL", "Signals": []}

    current_price = data["Close"].iloc[-1]
    bullish_count = 0
    bearish_count = 0

    # RSI signals
    if "RSI" in indicators and indicators["RSI"]:
        rsi = indicators["RSI"]
        if rsi < 30:
            signals["Signals"].append("RSI: Oversold (Bullish)")
            bullish_count += 1
        elif rsi > 70:
            signals["Signals"].append("RSI: Overbought (Bearish)")
            bearish_count += 1
        else:
            signals["Signals"].append(f"RSI: Neutral ({rsi:.1f})")

    # MACD signals
    if "MACD" in indicators and indicators["MACD"]:
        macd = indicators["MACD"]
        if macd["Histogram"] > 0:
            signals["Signals"].append("MACD: Bullish crossover")
            bullish_count += 1
        elif macd["Histogram"] < 0:
            signals["Signals"].append("MACD: Bearish crossover")
            bearish_count += 1

    # Moving Average signals
    if "SMA" in indicators:
        sma = indicators["SMA"]
        if "SMA_50" in sma and "SMA_200" in sma:
            if sma["SMA_50"] > sma["SMA_200"]:
                signals["Signals"].append("MA: Golden Cross (Bullish)")
                bullish_count += 1
            else:
                signals["Signals"].append("MA: Death Cross (Bearish)")
                bearish_count += 1

        if "SMA_20" in sma:
            if current_price > sma["SMA_20"]:
                signals["Signals"].append("Price above SMA20 (Bullish)")
                bullish_count += 0.5
            else:
                signals["Signals"].append("Price below SMA20 (Bearish)")
                bearish_count += 0.5

    # Bollinger Bands signals
    if "BollingerBands" in indicators and indicators["BollingerBands"]:
        bb = indicators["BollingerBands"]
        position = bb["Position"]
        if position < 20:
            signals["Signals"].append("BB: Near lower band (Bullish)")
            bullish_count += 1
        elif position > 80:
            signals["Signals"].append("BB: Near upper band (Bearish)")
            bearish_count += 1

    # Overall signal
    if bullish_count > bearish_count + 1:
        signals["Overall"] = "BULLISH"
    elif bearish_count > bullish_count + 1:
        signals["Overall"] = "BEARISH"

    signals["Score"] = f"+{int(bullish_count)} / -{int(bearish_count)}"

    return signals


def perform_technical_analysis(ticker, period="3mo", indicators=["ALL"]):
    """
    Perform complete technical analysis on a ticker.

    Args:
        ticker: Stock or crypto ticker symbol
        period: Data period
        indicators: List of indicators to calculate

    Returns:
        Dictionary containing analysis results
    """
    try:
        # Fetch data
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)

        if data.empty:
            return {"error": f"No data available for {ticker}"}

        result = {
            "ticker": ticker,
            "current_price": data["Close"].iloc[-1],
            "period": period,
            "indicators": {},
        }

        # Calculate requested indicators
        if "ALL" in indicators or "SMA" in indicators:
            result["indicators"]["SMA"] = calculate_sma(data)

        if "ALL" in indicators or "EMA" in indicators:
            result["indicators"]["EMA"] = calculate_ema(data)

        if "ALL" in indicators or "RSI" in indicators:
            rsi = calculate_rsi(data)
            if rsi:
                result["indicators"]["RSI"] = round(rsi, 2)

        if "ALL" in indicators or "MACD" in indicators:
            macd = calculate_macd(data)
            if macd:
                result["indicators"]["MACD"] = {k: round(v, 4) for k, v in macd.items()}

        if "ALL" in indicators or "BB" in indicators:
            bb = calculate_bollinger_bands(data)
            if bb:
                result["indicators"]["BollingerBands"] = {k: round(v, 2) if isinstance(v, float) else v
                                                          for k, v in bb.items()}

        if "ALL" in indicators or "VOL" in indicators:
            vol = analyze_volume(data)
            if vol:
                result["indicators"]["Volume"] = vol

        # Generate trading signals
        result["signals"] = generate_signals(data, result["indicators"])

        return result

    except Exception as e:
        return {"error": f"Failed to analyze {ticker}: {str(e)}"}


def main():
    parser = argparse.ArgumentParser(description="Perform technical analysis on stocks/crypto")
    parser.add_argument("ticker", help="Stock or crypto ticker symbol")
    parser.add_argument("--period", default="3mo",
                       choices=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
                       help="Data period (default: 3mo)")
    parser.add_argument("--indicators", default="ALL",
                       help="Indicators to calculate: SMA,EMA,RSI,MACD,BB,VOL,ALL (default: ALL)")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format (default: text)")

    args = parser.parse_args()

    # Parse indicators
    indicators = [i.strip().upper() for i in args.indicators.split(",")]

    # Perform analysis
    result = perform_technical_analysis(args.ticker, period=args.period, indicators=indicators)

    # Output results
    if args.output == "json":
        print(json.dumps(result, indent=2, default=str))
    else:
        # Text output
        if "error" in result:
            print(f"Error: {result['error']}")
            sys.exit(1)

        print(f"\n=== Technical Analysis: {result['ticker']} ===\n")
        print(f"Current Price: ${result['current_price']:.2f}")
        print(f"Period: {result['period']}\n")

        ind = result["indicators"]

        # Moving Averages
        if "SMA" in ind and ind["SMA"]:
            print("=== Simple Moving Averages ===")
            for key, value in ind["SMA"].items():
                print(f"  {key}: ${value:.2f}")
            print()

        if "EMA" in ind and ind["EMA"]:
            print("=== Exponential Moving Averages ===")
            for key, value in ind["EMA"].items():
                print(f"  {key}: ${value:.2f}")
            print()

        # RSI
        if "RSI" in ind and ind["RSI"]:
            rsi = ind["RSI"]
            print("=== Relative Strength Index (RSI) ===")
            print(f"  RSI(14): {rsi:.2f}")
            if rsi < 30:
                print("  Status: Oversold (Potential BUY signal)")
            elif rsi > 70:
                print("  Status: Overbought (Potential SELL signal)")
            else:
                print("  Status: Neutral")
            print()

        # MACD
        if "MACD" in ind and ind["MACD"]:
            macd = ind["MACD"]
            print("=== MACD ===")
            print(f"  MACD Line: {macd['MACD']:.4f}")
            print(f"  Signal Line: {macd['Signal']:.4f}")
            print(f"  Histogram: {macd['Histogram']:.4f}")
            if macd["Histogram"] > 0:
                print("  Status: Bullish (MACD above signal)")
            else:
                print("  Status: Bearish (MACD below signal)")
            print()

        # Bollinger Bands
        if "BollingerBands" in ind and ind["BollingerBands"]:
            bb = ind["BollingerBands"]
            print("=== Bollinger Bands ===")
            print(f"  Upper Band: ${bb['Upper']:.2f}")
            print(f"  Middle Band: ${bb['Middle']:.2f}")
            print(f"  Lower Band: ${bb['Lower']:.2f}")
            print(f"  Current Price: ${bb['Current']:.2f}")
            print(f"  Position: {bb['Position']:.1f}% (0=Lower, 100=Upper)")
            print()

        # Volume
        if "Volume" in ind and ind["Volume"]:
            vol = ind["Volume"]
            print("=== Volume Analysis ===")
            print(f"  Current Volume: {vol['Current']:,.0f}")
            print(f"  20-day Avg: {vol['Avg_20d']:,.0f}")
            print(f"  Ratio: {vol['Ratio']:.2f}x")
            print(f"  Trend: {vol['Trend']}")
            print()

        # Trading Signals
        signals = result["signals"]
        print("=== Trading Signals ===")
        print(f"Overall Signal: {signals['Overall']}")
        print(f"Signal Score: {signals['Score']}")
        print("\nDetailed Signals:")
        for signal in signals["Signals"]:
            print(f"  • {signal}")


if __name__ == "__main__":
    main()
