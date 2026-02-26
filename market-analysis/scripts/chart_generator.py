#!/usr/bin/env python3
"""
Chart Generator for Market Analysis
Generates candlestick charts, technical indicator overlays, and exports to PNG/HTML.
"""

import argparse
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install pandas numpy")
    sys.exit(1)

# Try importing visualization libraries
try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import mplfinance as mpf
    MPLFINANCE_AVAILABLE = True
except ImportError:
    MPLFINANCE_AVAILABLE = False

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import yfinance as yf
except ImportError:
    yf = None


class ChartGenerator:
    """
    Chart Generation Engine

    Features:
    - Candlestick charts
    - Technical indicator overlays (SMA, EMA, Bollinger Bands)
    - Volume charts
    - Export to PNG, HTML
    """

    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / 'charts'
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_candlestick(self, ticker: str, period: str = '3mo',
                            indicators: List[str] = None,
                            output_format: str = 'png') -> Dict:
        """
        生成K线图

        Args:
            ticker: 股票代码
            period: 时间段
            indicators: 要叠加的指标 ['sma', 'ema', 'bb', 'volume']
            output_format: 输出格式 ('png', 'html')

        Returns:
            生成结果
        """
        if yf is None:
            return {'error': 'yfinance not available'}

        indicators = indicators or ['sma', 'volume']

        # Fetch data
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
            if data.empty:
                return {'error': f'No data available for {ticker}'}
        except Exception as e:
            return {'error': f'Data fetch failed: {e}'}

        # Generate chart based on format
        if output_format == 'html' and PLOTLY_AVAILABLE:
            return self._generate_plotly_chart(ticker, data, indicators)
        elif MPLFINANCE_AVAILABLE:
            return self._generate_mplfinance_chart(ticker, data, indicators)
        elif MATPLOTLIB_AVAILABLE:
            return self._generate_matplotlib_chart(ticker, data, indicators)
        else:
            return {'error': 'No visualization library available. Install matplotlib or plotly.'}

    def _generate_mplfinance_chart(self, ticker: str, data: pd.DataFrame,
                                   indicators: List[str]) -> Dict:
        """使用mplfinance生成图表"""
        # Prepare additional plots
        addplots = []

        # Add indicators
        if 'sma' in indicators:
            sma_20 = data['Close'].rolling(20).mean()
            sma_50 = data['Close'].rolling(50).mean()
            addplots.append(mpf.make_addplot(sma_20, color='blue', width=1))
            addplots.append(mpf.make_addplot(sma_50, color='orange', width=1))

        if 'ema' in indicators:
            ema_12 = data['Close'].ewm(span=12).mean()
            ema_26 = data['Close'].ewm(span=26).mean()
            addplots.append(mpf.make_addplot(ema_12, color='green', width=1))
            addplots.append(mpf.make_addplot(ema_26, color='red', width=1))

        if 'bb' in indicators:
            sma = data['Close'].rolling(20).mean()
            std = data['Close'].rolling(20).std()
            upper = sma + 2 * std
            lower = sma - 2 * std
            addplots.append(mpf.make_addplot(upper, color='gray', linestyle='--', width=0.5))
            addplots.append(mpf.make_addplot(lower, color='gray', linestyle='--', width=0.5))

        # Generate chart
        filename = f"{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = self.output_dir / filename

        kwargs = {
            'type': 'candle',
            'volume': 'volume' in indicators,
            'title': f'{ticker} Chart',
            'style': 'charles',
            'savefig': str(filepath)
        }

        if addplots:
            kwargs['addplot'] = addplots

        mpf.plot(data, **kwargs)

        return {
            'status': 'success',
            'ticker': ticker,
            'file': str(filepath),
            'format': 'png',
            'indicators': indicators
        }

    def _generate_matplotlib_chart(self, ticker: str, data: pd.DataFrame,
                                   indicators: List[str]) -> Dict:
        """使用matplotlib生成基础图表"""
        fig, axes = plt.subplots(2 if 'volume' in indicators else 1, 1,
                                figsize=(12, 8), sharex=True)

        if 'volume' not in indicators:
            axes = [axes]

        ax_price = axes[0]

        # Plot price
        ax_price.plot(data.index, data['Close'], label='Close', color='blue')

        # Add indicators
        if 'sma' in indicators:
            sma_20 = data['Close'].rolling(20).mean()
            sma_50 = data['Close'].rolling(50).mean()
            ax_price.plot(data.index, sma_20, label='SMA 20', color='orange', alpha=0.7)
            ax_price.plot(data.index, sma_50, label='SMA 50', color='green', alpha=0.7)

        if 'bb' in indicators:
            sma = data['Close'].rolling(20).mean()
            std = data['Close'].rolling(20).std()
            ax_price.fill_between(data.index, sma - 2*std, sma + 2*std,
                                 alpha=0.2, color='gray', label='Bollinger Bands')

        ax_price.set_title(f'{ticker} Price Chart')
        ax_price.set_ylabel('Price')
        ax_price.legend(loc='upper left')
        ax_price.grid(True, alpha=0.3)

        # Volume
        if 'volume' in indicators and len(axes) > 1:
            ax_vol = axes[1]
            colors = ['green' if data['Close'].iloc[i] >= data['Open'].iloc[i]
                     else 'red' for i in range(len(data))]
            ax_vol.bar(data.index, data['Volume'], color=colors, alpha=0.7)
            ax_vol.set_ylabel('Volume')
            ax_vol.grid(True, alpha=0.3)

        plt.tight_layout()

        filename = f"{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=150)
        plt.close()

        return {
            'status': 'success',
            'ticker': ticker,
            'file': str(filepath),
            'format': 'png',
            'indicators': indicators
        }

    def _generate_plotly_chart(self, ticker: str, data: pd.DataFrame,
                               indicators: List[str]) -> Dict:
        """使用Plotly生成交互式图表"""
        # Create subplots
        rows = 2 if 'volume' in indicators else 1
        fig = make_subplots(rows=rows, cols=1, shared_xaxes=True,
                           row_heights=[0.7, 0.3] if rows == 2 else [1],
                           vertical_spacing=0.05)

        # Candlestick
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='OHLC'
            ),
            row=1, col=1
        )

        # Add indicators
        if 'sma' in indicators:
            sma_20 = data['Close'].rolling(20).mean()
            sma_50 = data['Close'].rolling(50).mean()
            fig.add_trace(go.Scatter(x=data.index, y=sma_20, name='SMA 20',
                                    line=dict(color='orange', width=1)), row=1, col=1)
            fig.add_trace(go.Scatter(x=data.index, y=sma_50, name='SMA 50',
                                    line=dict(color='blue', width=1)), row=1, col=1)

        if 'ema' in indicators:
            ema_12 = data['Close'].ewm(span=12).mean()
            ema_26 = data['Close'].ewm(span=26).mean()
            fig.add_trace(go.Scatter(x=data.index, y=ema_12, name='EMA 12',
                                    line=dict(color='green', width=1)), row=1, col=1)
            fig.add_trace(go.Scatter(x=data.index, y=ema_26, name='EMA 26',
                                    line=dict(color='red', width=1)), row=1, col=1)

        if 'bb' in indicators:
            sma = data['Close'].rolling(20).mean()
            std = data['Close'].rolling(20).std()
            fig.add_trace(go.Scatter(x=data.index, y=sma + 2*std, name='BB Upper',
                                    line=dict(color='gray', dash='dash', width=1)), row=1, col=1)
            fig.add_trace(go.Scatter(x=data.index, y=sma - 2*std, name='BB Lower',
                                    line=dict(color='gray', dash='dash', width=1),
                                    fill='tonexty', fillcolor='rgba(128,128,128,0.1)'), row=1, col=1)

        # Volume
        if 'volume' in indicators:
            colors = ['green' if data['Close'].iloc[i] >= data['Open'].iloc[i]
                     else 'red' for i in range(len(data))]
            fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume',
                                marker_color=colors, opacity=0.7), row=2, col=1)

        # Layout
        fig.update_layout(
            title=f'{ticker} Chart',
            xaxis_rangeslider_visible=False,
            height=600,
            showlegend=True
        )

        # Save to HTML
        filename = f"{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = self.output_dir / filename
        fig.write_html(str(filepath))

        return {
            'status': 'success',
            'ticker': ticker,
            'file': str(filepath),
            'format': 'html',
            'indicators': indicators,
            'interactive': True
        }

    def generate_comparison_chart(self, tickers: List[str], period: str = '1y',
                                  normalize: bool = True) -> Dict:
        """
        生成多股票比较图

        Args:
            tickers: 股票代码列表
            period: 时间段
            normalize: 是否归一化

        Returns:
            生成结果
        """
        if yf is None:
            return {'error': 'yfinance not available'}

        if not MATPLOTLIB_AVAILABLE:
            return {'error': 'matplotlib not available'}

        try:
            data = yf.download(tickers, period=period)['Adj Close']
            if data.empty:
                return {'error': 'No data available'}
        except Exception as e:
            return {'error': f'Data fetch failed: {e}'}

        fig, ax = plt.subplots(figsize=(12, 6))

        if normalize:
            # Normalize to 100 at start
            normalized = data / data.iloc[0] * 100
            for col in normalized.columns:
                ax.plot(normalized.index, normalized[col], label=col)
            ax.set_ylabel('Normalized Price (Start = 100)')
        else:
            for col in data.columns:
                ax.plot(data.index, data[col], label=col)
            ax.set_ylabel('Price')

        ax.set_title('Stock Comparison')
        ax.legend()
        ax.grid(True, alpha=0.3)

        filename = f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=150)
        plt.close()

        return {
            'status': 'success',
            'tickers': tickers,
            'file': str(filepath),
            'format': 'png',
            'normalized': normalize
        }

    def generate_heatmap(self, tickers: List[str], period: str = '1y') -> Dict:
        """
        生成相关性热力图

        Args:
            tickers: 股票代码列表
            period: 时间段

        Returns:
            生成结果
        """
        if yf is None:
            return {'error': 'yfinance not available'}

        if not MATPLOTLIB_AVAILABLE:
            return {'error': 'matplotlib not available'}

        try:
            data = yf.download(tickers, period=period)['Adj Close']
            returns = data.pct_change().dropna()
            corr = returns.corr()
        except Exception as e:
            return {'error': f'Data processing failed: {e}'}

        fig, ax = plt.subplots(figsize=(10, 8))

        im = ax.imshow(corr, cmap='RdYlGn', vmin=-1, vmax=1)

        ax.set_xticks(range(len(tickers)))
        ax.set_yticks(range(len(tickers)))
        ax.set_xticklabels(tickers, rotation=45, ha='right')
        ax.set_yticklabels(tickers)

        # Add correlation values
        for i in range(len(tickers)):
            for j in range(len(tickers)):
                text = ax.text(j, i, f'{corr.iloc[i, j]:.2f}',
                              ha='center', va='center', color='black', fontsize=10)

        plt.colorbar(im, ax=ax, label='Correlation')
        ax.set_title('Correlation Heatmap')

        plt.tight_layout()

        filename = f"heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=150)
        plt.close()

        return {
            'status': 'success',
            'tickers': tickers,
            'file': str(filepath),
            'format': 'png'
        }

    def list_available_features(self) -> Dict:
        """列出可用功能"""
        return {
            'libraries': {
                'matplotlib': MATPLOTLIB_AVAILABLE,
                'mplfinance': MPLFINANCE_AVAILABLE,
                'plotly': PLOTLY_AVAILABLE
            },
            'chart_types': ['candlestick', 'line', 'comparison', 'heatmap'],
            'indicators': ['sma', 'ema', 'bb', 'volume'],
            'output_formats': ['png'] + (['html'] if PLOTLY_AVAILABLE else []),
            'output_directory': str(self.output_dir)
        }


def main():
    parser = argparse.ArgumentParser(description="Chart Generator")
    parser.add_argument("ticker", nargs='?', help="Stock ticker")
    parser.add_argument("--tickers", help="Comma-separated tickers for comparison")
    parser.add_argument("--period", default="3mo", help="Data period")
    parser.add_argument("--indicators", default="sma,volume",
                       help="Comma-separated indicators (sma,ema,bb,volume)")
    parser.add_argument("--format", choices=["png", "html"], default="png",
                       help="Output format")
    parser.add_argument("--compare", action="store_true", help="Generate comparison chart")
    parser.add_argument("--heatmap", action="store_true", help="Generate correlation heatmap")
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument("--list-features", action="store_true", help="List available features")
    parser.add_argument("--output", choices=["json", "text"], default="text")

    args = parser.parse_args()

    generator = ChartGenerator(output_dir=args.output_dir)

    if args.list_features:
        data = generator.list_available_features()
    elif args.heatmap and args.tickers:
        tickers = [t.strip() for t in args.tickers.split(',')]
        data = generator.generate_heatmap(tickers, args.period)
    elif args.compare and args.tickers:
        tickers = [t.strip() for t in args.tickers.split(',')]
        data = generator.generate_comparison_chart(tickers, args.period)
    elif args.ticker:
        indicators = [i.strip() for i in args.indicators.split(',')]
        data = generator.generate_candlestick(args.ticker, args.period, indicators, args.format)
    else:
        print("Error: --ticker or --tickers required")
        sys.exit(1)

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2))
    else:
        if 'error' in data:
            print(f"Error: {data['error']}")
        else:
            print(f"\n=== Chart Generated ===\n")
            for k, v in data.items():
                print(f"{k}: {v}")


if __name__ == "__main__":
    main()
