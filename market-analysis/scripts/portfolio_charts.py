#!/usr/bin/env python3
"""
Portfolio Charts Generator
Generates portfolio allocation charts, performance curves, and risk visualizations.
"""

import argparse
import json
import sys
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

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

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


class PortfolioChartGenerator:
    """
    Portfolio Visualization Engine

    Features:
    - Allocation pie charts
    - Performance equity curves
    - Drawdown charts
    - Risk/return scatter plots
    """

    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / 'charts'
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def allocation_pie(self, holdings: Dict[str, float], title: str = "Portfolio Allocation",
                       output_format: str = 'png') -> Dict:
        """
        生成资产配置饼图

        Args:
            holdings: {ticker: value} 或 {ticker: weight}
            title: 图表标题
            output_format: 输出格式

        Returns:
            生成结果
        """
        if not MATPLOTLIB_AVAILABLE and not PLOTLY_AVAILABLE:
            return {'error': 'No visualization library available'}

        labels = list(holdings.keys())
        values = list(holdings.values())

        # Normalize to percentages if not already
        total = sum(values)
        if total > 1.5:  # Likely dollar values
            percentages = [v / total * 100 for v in values]
        else:
            percentages = [v * 100 for v in values]

        if output_format == 'html' and PLOTLY_AVAILABLE:
            return self._plotly_pie(labels, percentages, title)
        elif MATPLOTLIB_AVAILABLE:
            return self._matplotlib_pie(labels, percentages, title)
        else:
            return {'error': 'Visualization library not available'}

    def _matplotlib_pie(self, labels: List[str], values: List[float], title: str) -> Dict:
        """使用Matplotlib生成饼图"""
        fig, ax = plt.subplots(figsize=(10, 8))

        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))

        wedges, texts, autotexts = ax.pie(
            values, labels=labels, autopct='%1.1f%%',
            colors=colors, startangle=90
        )

        ax.set_title(title, fontsize=14, fontweight='bold')

        # Add legend
        ax.legend(wedges, [f'{l}: {v:.1f}%' for l, v in zip(labels, values)],
                 title="Holdings", loc="center left", bbox_to_anchor=(1, 0.5))

        plt.tight_layout()

        filename = f"allocation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()

        return {'status': 'success', 'file': str(filepath), 'format': 'png'}

    def _plotly_pie(self, labels: List[str], values: List[float], title: str) -> Dict:
        """使用Plotly生成饼图"""
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3,
            textinfo='label+percent',
            hovertemplate='%{label}: %{value:.1f}%<extra></extra>'
        )])

        fig.update_layout(
            title=title,
            showlegend=True
        )

        filename = f"allocation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = self.output_dir / filename
        fig.write_html(str(filepath))

        return {'status': 'success', 'file': str(filepath), 'format': 'html', 'interactive': True}

    def equity_curve(self, tickers: List[str], weights: List[float],
                     period: str = '1y', benchmark: str = 'SPY',
                     initial_value: float = 100000) -> Dict:
        """
        生成净值曲线图

        Args:
            tickers: 持仓列表
            weights: 权重列表
            period: 时间段
            benchmark: 基准
            initial_value: 初始资金

        Returns:
            生成结果
        """
        if yf is None:
            return {'error': 'yfinance not available'}

        if not MATPLOTLIB_AVAILABLE:
            return {'error': 'matplotlib not available'}

        try:
            all_tickers = tickers + [benchmark]
            data = yf.download(all_tickers, period=period)['Adj Close']
            if data.empty:
                return {'error': 'No data available'}
        except Exception as e:
            return {'error': f'Data fetch failed: {e}'}

        returns = data.pct_change().dropna()

        # Portfolio returns
        weights = np.array(weights)
        portfolio_returns = returns[tickers].dot(weights)

        # Calculate cumulative values
        portfolio_value = (1 + portfolio_returns).cumprod() * initial_value
        benchmark_value = (1 + returns[benchmark]).cumprod() * initial_value

        # Plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                                       gridspec_kw={'height_ratios': [3, 1]})

        # Equity curve
        ax1.plot(portfolio_value.index, portfolio_value, label='Portfolio', linewidth=2)
        ax1.plot(benchmark_value.index, benchmark_value, label=benchmark, linewidth=1, alpha=0.7)
        ax1.fill_between(portfolio_value.index, initial_value, portfolio_value,
                        where=portfolio_value >= initial_value, alpha=0.3, color='green')
        ax1.fill_between(portfolio_value.index, initial_value, portfolio_value,
                        where=portfolio_value < initial_value, alpha=0.3, color='red')
        ax1.axhline(y=initial_value, color='gray', linestyle='--', alpha=0.5)
        ax1.set_ylabel('Portfolio Value ($)')
        ax1.set_title('Portfolio Performance')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Drawdown
        rolling_max = portfolio_value.expanding().max()
        drawdown = (portfolio_value - rolling_max) / rolling_max * 100
        ax2.fill_between(drawdown.index, 0, drawdown, color='red', alpha=0.5)
        ax2.set_ylabel('Drawdown (%)')
        ax2.set_xlabel('Date')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        filename = f"equity_curve_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=150)
        plt.close()

        # Calculate stats
        total_return = (portfolio_value.iloc[-1] / initial_value - 1) * 100
        max_dd = drawdown.min()

        return {
            'status': 'success',
            'file': str(filepath),
            'format': 'png',
            'final_value': round(portfolio_value.iloc[-1], 2),
            'total_return': round(total_return, 2),
            'max_drawdown': round(max_dd, 2)
        }

    def risk_return_scatter(self, tickers: List[str], period: str = '1y') -> Dict:
        """
        生成风险收益散点图

        Args:
            tickers: 股票列表
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
            if data.empty:
                return {'error': 'No data available'}
        except Exception as e:
            return {'error': f'Data fetch failed: {e}'}

        returns = data.pct_change().dropna()

        # Calculate annualized metrics
        annual_returns = returns.mean() * 252 * 100
        annual_volatility = returns.std() * np.sqrt(252) * 100

        fig, ax = plt.subplots(figsize=(10, 8))

        # Scatter plot
        ax.scatter(annual_volatility, annual_returns, s=100, alpha=0.7)

        # Add labels
        for i, ticker in enumerate(tickers):
            ax.annotate(ticker, (annual_volatility[ticker], annual_returns[ticker]),
                       xytext=(5, 5), textcoords='offset points')

        # Add quadrant lines
        ax.axhline(y=annual_returns.mean(), color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=annual_volatility.mean(), color='gray', linestyle='--', alpha=0.5)

        ax.set_xlabel('Annual Volatility (%)')
        ax.set_ylabel('Annual Return (%)')
        ax.set_title('Risk-Return Profile')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        filename = f"risk_return_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=150)
        plt.close()

        return {
            'status': 'success',
            'file': str(filepath),
            'format': 'png',
            'metrics': {t: {'return': round(annual_returns[t], 2), 'volatility': round(annual_volatility[t], 2)}
                       for t in tickers}
        }

    def rolling_metrics(self, tickers: List[str], weights: List[float],
                       period: str = '2y', window: int = 60) -> Dict:
        """
        生成滚动指标图

        Args:
            tickers: 持仓列表
            weights: 权重
            period: 时间段
            window: 滚动窗口（天）

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

        returns = data.pct_change().dropna()
        weights = np.array(weights)
        portfolio_returns = returns.dot(weights)

        # Rolling metrics
        rolling_return = portfolio_returns.rolling(window).mean() * 252 * 100
        rolling_vol = portfolio_returns.rolling(window).std() * np.sqrt(252) * 100
        rolling_sharpe = (rolling_return - 5) / rolling_vol

        fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

        # Rolling return
        axes[0].plot(rolling_return.index, rolling_return, color='blue')
        axes[0].axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        axes[0].set_ylabel(f'{window}d Rolling Return (%)')
        axes[0].set_title(f'Rolling Metrics ({window}-day window)')
        axes[0].grid(True, alpha=0.3)

        # Rolling volatility
        axes[1].plot(rolling_vol.index, rolling_vol, color='red')
        axes[1].set_ylabel(f'{window}d Rolling Volatility (%)')
        axes[1].grid(True, alpha=0.3)

        # Rolling Sharpe
        axes[2].plot(rolling_sharpe.index, rolling_sharpe, color='green')
        axes[2].axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        axes[2].axhline(y=1, color='blue', linestyle='--', alpha=0.5, label='Sharpe=1')
        axes[2].set_ylabel(f'{window}d Rolling Sharpe')
        axes[2].set_xlabel('Date')
        axes[2].grid(True, alpha=0.3)
        axes[2].legend()

        plt.tight_layout()

        filename = f"rolling_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=150)
        plt.close()

        return {
            'status': 'success',
            'file': str(filepath),
            'format': 'png',
            'window': window
        }

    def sector_exposure(self, holdings: Dict[str, float], sectors: Dict[str, str]) -> Dict:
        """
        生成板块暴露图

        Args:
            holdings: {ticker: weight}
            sectors: {ticker: sector}

        Returns:
            生成结果
        """
        if not MATPLOTLIB_AVAILABLE:
            return {'error': 'matplotlib not available'}

        # Aggregate by sector
        sector_weights = {}
        for ticker, weight in holdings.items():
            sector = sectors.get(ticker, 'Other')
            sector_weights[sector] = sector_weights.get(sector, 0) + weight

        return self.allocation_pie(sector_weights, title="Sector Exposure")


def main():
    parser = argparse.ArgumentParser(description="Portfolio Chart Generator")
    parser.add_argument("action", choices=["allocation", "equity", "risk-return", "rolling"],
                       help="Chart type to generate")
    parser.add_argument("--tickers", help="Comma-separated tickers")
    parser.add_argument("--weights", help="Comma-separated weights")
    parser.add_argument("--holdings", help="JSON holdings {ticker: value}")
    parser.add_argument("--period", default="1y", help="Data period")
    parser.add_argument("--benchmark", default="SPY", help="Benchmark ticker")
    parser.add_argument("--initial", type=float, default=100000, help="Initial value")
    parser.add_argument("--window", type=int, default=60, help="Rolling window")
    parser.add_argument("--format", choices=["png", "html"], default="png", help="Output format")
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument("--output", choices=["json", "text"], default="text")

    args = parser.parse_args()

    generator = PortfolioChartGenerator(output_dir=args.output_dir)

    if args.action == "allocation":
        if args.holdings:
            holdings = json.loads(args.holdings)
        elif args.tickers and args.weights:
            tickers = [t.strip() for t in args.tickers.split(',')]
            weights = [float(w.strip()) for w in args.weights.split(',')]
            holdings = dict(zip(tickers, weights))
        else:
            holdings = {'AAPL': 25, 'MSFT': 25, 'GOOGL': 25, 'AMZN': 25}
        data = generator.allocation_pie(holdings, output_format=args.format)

    elif args.action == "equity":
        if not args.tickers:
            args.tickers = "AAPL,MSFT,GOOGL"
        tickers = [t.strip() for t in args.tickers.split(',')]
        if args.weights:
            weights = [float(w.strip()) for w in args.weights.split(',')]
        else:
            weights = [1.0 / len(tickers)] * len(tickers)
        data = generator.equity_curve(tickers, weights, args.period, args.benchmark, args.initial)

    elif args.action == "risk-return":
        if not args.tickers:
            args.tickers = "AAPL,MSFT,GOOGL,AMZN,TSLA"
        tickers = [t.strip() for t in args.tickers.split(',')]
        data = generator.risk_return_scatter(tickers, args.period)

    elif args.action == "rolling":
        if not args.tickers:
            args.tickers = "AAPL,MSFT,GOOGL"
        tickers = [t.strip() for t in args.tickers.split(',')]
        if args.weights:
            weights = [float(w.strip()) for w in args.weights.split(',')]
        else:
            weights = [1.0 / len(tickers)] * len(tickers)
        data = generator.rolling_metrics(tickers, weights, args.period, args.window)

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
