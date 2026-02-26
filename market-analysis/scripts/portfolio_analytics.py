#!/usr/bin/env python3
"""
Portfolio Analytics Module
Provides backtesting, optimization, and performance attribution.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
    from scipy.optimize import minimize
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install pandas numpy scipy")
    sys.exit(1)

try:
    import yfinance as yf
except ImportError:
    yf = None


class PortfolioAnalyzer:
    """
    Portfolio Analytics Engine

    Features:
    - Portfolio backtesting
    - Mean-variance optimization
    - Performance attribution
    - Rebalancing analysis
    """

    def __init__(self):
        pass

    def backtest_portfolio(self, tickers: List[str], weights: List[float],
                           start_date: str, end_date: str = None,
                           initial_value: float = 100000,
                           rebalance_freq: str = None) -> Dict:
        """
        回测投资组合

        Args:
            tickers: 股票代码列表
            weights: 权重列表
            start_date: 开始日期
            end_date: 结束日期
            initial_value: 初始资金
            rebalance_freq: 再平衡频率 ('M'=月, 'Q'=季, 'Y'=年)

        Returns:
            回测结果
        """
        if yf is None:
            return {'error': 'yfinance not available'}

        if len(tickers) != len(weights):
            return {'error': 'Tickers and weights must have same length'}

        weights = np.array(weights)
        if abs(weights.sum() - 1.0) > 0.01:
            return {'error': 'Weights must sum to 1'}

        # Fetch data
        try:
            data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
            if data.empty:
                return {'error': 'No data available'}
        except Exception as e:
            return {'error': f'Data fetch failed: {e}'}

        # Calculate returns
        returns = data.pct_change().dropna()

        # Portfolio returns
        portfolio_returns = returns.dot(weights)

        # Calculate cumulative returns
        cumulative = (1 + portfolio_returns).cumprod()
        portfolio_value = cumulative * initial_value

        # Calculate metrics
        total_return = (portfolio_value.iloc[-1] / initial_value - 1) * 100
        trading_days = len(returns)
        annual_factor = 252 / trading_days if trading_days > 0 else 1

        annual_return = ((1 + total_return / 100) ** annual_factor - 1) * 100
        annual_volatility = portfolio_returns.std() * np.sqrt(252) * 100

        sharpe_ratio = (annual_return - 5) / annual_volatility if annual_volatility > 0 else 0

        # Max drawdown
        rolling_max = portfolio_value.expanding().max()
        drawdown = (portfolio_value - rolling_max) / rolling_max
        max_drawdown = drawdown.min() * 100

        # Win rate
        win_days = (portfolio_returns > 0).sum()
        win_rate = win_days / len(portfolio_returns) * 100

        return {
            'initial_value': initial_value,
            'final_value': round(portfolio_value.iloc[-1], 2),
            'total_return': round(total_return, 2),
            'annualized_return': round(annual_return, 2),
            'annualized_volatility': round(annual_volatility, 2),
            'sharpe_ratio': round(sharpe_ratio, 3),
            'max_drawdown': round(max_drawdown, 2),
            'win_rate': round(win_rate, 2),
            'trading_days': trading_days,
            'start_date': returns.index[0].strftime('%Y-%m-%d'),
            'end_date': returns.index[-1].strftime('%Y-%m-%d'),
            'holdings': dict(zip(tickers, [round(w * 100, 2) for w in weights]))
        }

    def optimize_portfolio(self, tickers: List[str], period: str = '2y',
                           target: str = 'sharpe',
                           constraints: Dict = None) -> Dict:
        """
        优化投资组合

        Args:
            tickers: 股票代码列表
            period: 历史数据期间
            target: 优化目标 ('sharpe', 'min_volatility', 'max_return')
            constraints: 约束条件

        Returns:
            优化结果
        """
        if yf is None:
            return {'error': 'yfinance not available'}

        # Fetch data
        try:
            data = yf.download(tickers, period=period)['Adj Close']
            if data.empty:
                return {'error': 'No data available'}
        except Exception as e:
            return {'error': f'Data fetch failed: {e}'}

        returns = data.pct_change().dropna()

        # Calculate expected returns and covariance
        mean_returns = returns.mean() * 252
        cov_matrix = returns.cov() * 252
        n_assets = len(tickers)

        # Optimization functions
        def portfolio_return(weights):
            return np.dot(weights, mean_returns)

        def portfolio_volatility(weights):
            return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        def neg_sharpe_ratio(weights):
            ret = portfolio_return(weights)
            vol = portfolio_volatility(weights)
            return -(ret - 0.05) / vol if vol > 0 else 0

        # Constraints
        cons = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]  # Weights sum to 1

        # Bounds
        bounds = tuple((0.0, 1.0) for _ in range(n_assets))  # No short selling

        # Initial guess
        init_weights = np.array([1.0 / n_assets] * n_assets)

        # Optimize
        if target == 'sharpe':
            result = minimize(neg_sharpe_ratio, init_weights, method='SLSQP',
                            bounds=bounds, constraints=cons)
        elif target == 'min_volatility':
            result = minimize(portfolio_volatility, init_weights, method='SLSQP',
                            bounds=bounds, constraints=cons)
        elif target == 'max_return':
            result = minimize(lambda w: -portfolio_return(w), init_weights,
                            method='SLSQP', bounds=bounds, constraints=cons)
        else:
            return {'error': f'Unknown target: {target}'}

        if not result.success:
            return {'error': 'Optimization failed'}

        optimal_weights = result.x

        # Calculate optimal portfolio metrics
        opt_return = portfolio_return(optimal_weights) * 100
        opt_vol = portfolio_volatility(optimal_weights) * 100
        opt_sharpe = (opt_return - 5) / opt_vol if opt_vol > 0 else 0

        return {
            'target': target,
            'optimal_weights': {t: round(w * 100, 2) for t, w in zip(tickers, optimal_weights)},
            'expected_return': round(opt_return, 2),
            'expected_volatility': round(opt_vol, 2),
            'sharpe_ratio': round(opt_sharpe, 3),
            'individual_stats': {
                t: {
                    'expected_return': round(mean_returns[t] * 100, 2),
                    'volatility': round(np.sqrt(cov_matrix.loc[t, t]) * 100, 2)
                }
                for t in tickers
            }
        }

    def efficient_frontier(self, tickers: List[str], period: str = '2y',
                           n_portfolios: int = 50) -> Dict:
        """
        计算有效前沿

        Args:
            tickers: 股票代码列表
            period: 历史数据期间
            n_portfolios: 前沿点数量

        Returns:
            有效前沿数据
        """
        if yf is None:
            return {'error': 'yfinance not available'}

        try:
            data = yf.download(tickers, period=period)['Adj Close']
            if data.empty:
                return {'error': 'No data available'}
        except Exception as e:
            return {'error': f'Data fetch failed: {e}'}

        returns = data.pct_change().dropna()
        mean_returns = returns.mean() * 252
        cov_matrix = returns.cov() * 252
        n_assets = len(tickers)

        # Generate random portfolios
        results = []

        for _ in range(n_portfolios * 10):  # Generate more, keep efficient ones
            weights = np.random.random(n_assets)
            weights /= weights.sum()

            ret = np.dot(weights, mean_returns) * 100
            vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * 100
            sharpe = (ret - 5) / vol if vol > 0 else 0

            results.append({
                'return': round(ret, 2),
                'volatility': round(vol, 2),
                'sharpe': round(sharpe, 3),
                'weights': {t: round(w * 100, 2) for t, w in zip(tickers, weights)}
            })

        # Sort by Sharpe ratio
        results.sort(key=lambda x: x['sharpe'], reverse=True)

        # Find key portfolios
        max_sharpe = results[0]
        min_vol = min(results, key=lambda x: x['volatility'])
        max_return = max(results, key=lambda x: x['return'])

        return {
            'max_sharpe_portfolio': max_sharpe,
            'min_volatility_portfolio': min_vol,
            'max_return_portfolio': max_return,
            'frontier_points': results[:n_portfolios]
        }

    def performance_attribution(self, tickers: List[str], weights: List[float],
                                benchmark: str = 'SPY', period: str = '1y') -> Dict:
        """
        业绩归因分析

        Args:
            tickers: 持仓列表
            weights: 权重列表
            benchmark: 基准
            period: 分析期间

        Returns:
            归因结果
        """
        if yf is None:
            return {'error': 'yfinance not available'}

        all_tickers = tickers + [benchmark]
        weights = np.array(weights)

        try:
            data = yf.download(all_tickers, period=period)['Adj Close']
            if data.empty:
                return {'error': 'No data available'}
        except Exception as e:
            return {'error': f'Data fetch failed: {e}'}

        returns = data.pct_change().dropna()

        # Portfolio returns
        portfolio_returns = returns[tickers].dot(weights)
        benchmark_returns = returns[benchmark]

        # Calculate excess returns
        excess_returns = portfolio_returns - benchmark_returns

        # Attribution by asset
        attribution = {}
        for i, ticker in enumerate(tickers):
            asset_contrib = returns[ticker] * weights[i]
            benchmark_contrib = benchmark_returns * weights[i]
            selection_effect = (asset_contrib - benchmark_contrib).sum() * 100

            attribution[ticker] = {
                'weight': round(weights[i] * 100, 2),
                'asset_return': round(returns[ticker].sum() * 100, 2),
                'contribution': round(asset_contrib.sum() * 100, 2),
                'selection_effect': round(selection_effect, 2)
            }

        # Summary
        total_portfolio_return = portfolio_returns.sum() * 100
        total_benchmark_return = benchmark_returns.sum() * 100
        alpha = total_portfolio_return - total_benchmark_return

        return {
            'portfolio_return': round(total_portfolio_return, 2),
            'benchmark_return': round(total_benchmark_return, 2),
            'alpha': round(alpha, 2),
            'attribution': attribution,
            'interpretation': 'Positive alpha indicates outperformance vs benchmark'
        }

    def rebalancing_analysis(self, tickers: List[str], target_weights: List[float],
                            current_values: List[float]) -> Dict:
        """
        再平衡分析

        Args:
            tickers: 持仓列表
            target_weights: 目标权重
            current_values: 当前市值

        Returns:
            再平衡建议
        """
        total_value = sum(current_values)
        current_weights = [v / total_value for v in current_values]
        target_weights = list(target_weights)

        trades = []
        for i, ticker in enumerate(tickers):
            current_val = current_values[i]
            target_val = total_value * target_weights[i]
            diff = target_val - current_val
            diff_pct = (target_weights[i] - current_weights[i]) * 100

            action = 'Buy' if diff > 0 else 'Sell' if diff < 0 else 'Hold'

            trades.append({
                'ticker': ticker,
                'current_weight': round(current_weights[i] * 100, 2),
                'target_weight': round(target_weights[i] * 100, 2),
                'drift': round(diff_pct, 2),
                'current_value': round(current_val, 2),
                'target_value': round(target_val, 2),
                'action': action,
                'trade_amount': round(abs(diff), 2)
            })

        # Calculate total turnover
        turnover = sum(abs(t['trade_amount']) for t in trades) / (2 * total_value) * 100

        return {
            'total_portfolio_value': round(total_value, 2),
            'trades': trades,
            'turnover': round(turnover, 2),
            'estimated_costs': round(turnover * total_value / 100 * 0.001, 2),  # Assume 0.1% cost
            'needs_rebalance': any(abs(t['drift']) > 5 for t in trades)
        }

    def correlation_analysis(self, tickers: List[str], period: str = '1y') -> Dict:
        """
        相关性分析

        Args:
            tickers: 股票列表
            period: 分析期间

        Returns:
            相关性矩阵
        """
        if yf is None:
            return {'error': 'yfinance not available'}

        try:
            data = yf.download(tickers, period=period)['Adj Close']
            if data.empty:
                return {'error': 'No data available'}
        except Exception as e:
            return {'error': f'Data fetch failed: {e}'}

        returns = data.pct_change().dropna()
        corr_matrix = returns.corr()

        # Find high correlations
        high_corr_pairs = []
        for i in range(len(tickers)):
            for j in range(i + 1, len(tickers)):
                corr = corr_matrix.iloc[i, j]
                if abs(corr) > 0.7:
                    high_corr_pairs.append({
                        'pair': f"{tickers[i]}-{tickers[j]}",
                        'correlation': round(corr, 4)
                    })

        return {
            'correlation_matrix': corr_matrix.round(4).to_dict(),
            'high_correlations': high_corr_pairs,
            'avg_correlation': round(corr_matrix.values[np.triu_indices_from(corr_matrix.values, 1)].mean(), 4),
            'diversification_note': 'Lower average correlation indicates better diversification'
        }


def main():
    parser = argparse.ArgumentParser(description="Portfolio Analytics Tool")
    parser.add_argument("action", choices=["backtest", "optimize", "frontier", "attribution", "rebalance", "correlation"],
                       help="Action to perform")
    parser.add_argument("--tickers", help="Comma-separated tickers")
    parser.add_argument("--weights", help="Comma-separated weights")
    parser.add_argument("--start", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", help="End date (YYYY-MM-DD)")
    parser.add_argument("--period", default="1y", help="Period for analysis")
    parser.add_argument("--initial", type=float, default=100000, help="Initial value")
    parser.add_argument("--target", default="sharpe", choices=["sharpe", "min_volatility", "max_return"])
    parser.add_argument("--benchmark", default="SPY", help="Benchmark ticker")
    parser.add_argument("--output", choices=["json", "text"], default="text")

    args = parser.parse_args()

    analyzer = PortfolioAnalyzer()

    if not args.tickers:
        args.tickers = "AAPL,MSFT,GOOGL,AMZN"  # Default

    tickers = [t.strip() for t in args.tickers.split(',')]

    if args.weights:
        weights = [float(w.strip()) for w in args.weights.split(',')]
    else:
        weights = [1.0 / len(tickers)] * len(tickers)  # Equal weight

    if args.action == "backtest":
        if not args.start:
            args.start = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        data = analyzer.backtest_portfolio(tickers, weights, args.start, args.end, args.initial)

    elif args.action == "optimize":
        data = analyzer.optimize_portfolio(tickers, args.period, args.target)

    elif args.action == "frontier":
        data = analyzer.efficient_frontier(tickers, args.period)

    elif args.action == "attribution":
        data = analyzer.performance_attribution(tickers, weights, args.benchmark, args.period)

    elif args.action == "rebalance":
        # Example current values
        current_values = [25000, 25000, 25000, 25000][:len(tickers)]
        data = analyzer.rebalancing_analysis(tickers, weights, current_values)

    elif args.action == "correlation":
        data = analyzer.correlation_analysis(tickers, args.period)

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2, default=str))
    else:
        print(f"\n=== Portfolio Analytics: {args.action.title()} ===\n")
        for k, v in data.items():
            if isinstance(v, dict):
                print(f"\n{k}:")
                for k2, v2 in v.items():
                    if isinstance(v2, dict):
                        print(f"  {k2}: {v2}")
                    else:
                        print(f"  {k2}: {v2}")
            elif isinstance(v, list):
                print(f"\n{k}:")
                for item in v[:10]:  # Limit output
                    print(f"  {item}")
            else:
                print(f"{k}: {v}")


if __name__ == "__main__":
    main()
