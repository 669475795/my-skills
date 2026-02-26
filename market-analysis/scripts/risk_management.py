#!/usr/bin/env python3
"""
Risk Management Module for Market Analysis
Provides position sizing, VaR calculation, stress testing, and risk metrics.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
    from scipy import stats
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install pandas numpy scipy")
    sys.exit(1)

try:
    import yfinance as yf
except ImportError:
    yf = None


class RiskManager:
    """
    Risk Management Engine

    Features:
    - Position sizing calculator
    - Value at Risk (VaR) calculation
    - Risk-adjusted return metrics
    - Portfolio stress testing
    - Maximum drawdown analysis
    """

    def __init__(self):
        pass

    def calculate_position_size(self, account_value: float, risk_percent: float,
                                entry_price: float, stop_loss: float) -> Dict:
        """
        计算仓位大小

        Args:
            account_value: 账户总值
            risk_percent: 每笔交易风险比例 (e.g., 0.02 = 2%)
            entry_price: 入场价格
            stop_loss: 止损价格

        Returns:
            仓位计算结果
        """
        # Calculate risk per share
        risk_per_share = abs(entry_price - stop_loss)

        if risk_per_share == 0:
            return {'error': 'Stop loss cannot equal entry price'}

        # Calculate maximum risk amount
        max_risk_amount = account_value * risk_percent

        # Calculate position size
        shares = int(max_risk_amount / risk_per_share)
        position_value = shares * entry_price
        position_percent = (position_value / account_value) * 100

        # Risk-reward calculations
        return {
            'account_value': account_value,
            'risk_percent': risk_percent * 100,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'risk_per_share': round(risk_per_share, 2),
            'max_risk_amount': round(max_risk_amount, 2),
            'recommended_shares': shares,
            'position_value': round(position_value, 2),
            'position_percent': round(position_percent, 2),
            'max_loss_if_stopped': round(shares * risk_per_share, 2)
        }

    def calculate_var(self, returns: pd.Series, confidence: float = 0.95,
                      method: str = 'historical', holding_period: int = 1) -> Dict:
        """
        计算风险价值 (VaR)

        Args:
            returns: 收益率序列
            confidence: 置信水平 (e.g., 0.95, 0.99)
            method: 计算方法 ('historical', 'parametric', 'monte_carlo')
            holding_period: 持有期（天数）

        Returns:
            VaR计算结果
        """
        if len(returns) < 30:
            return {'error': 'Insufficient data for VaR calculation'}

        results = {
            'confidence': confidence,
            'holding_period': holding_period,
            'method': method,
            'data_points': len(returns)
        }

        if method == 'historical':
            var = self._historical_var(returns, confidence)
        elif method == 'parametric':
            var = self._parametric_var(returns, confidence)
        elif method == 'monte_carlo':
            var = self._monte_carlo_var(returns, confidence)
        else:
            return {'error': f'Unknown method: {method}'}

        # Adjust for holding period (square root of time rule)
        var_adjusted = var * np.sqrt(holding_period)

        results['var_1day'] = round(var * 100, 4)
        results['var_adjusted'] = round(var_adjusted * 100, 4)
        results['interpretation'] = (
            f"With {confidence*100:.0f}% confidence, the portfolio will not lose more than "
            f"{abs(var_adjusted)*100:.2f}% over {holding_period} day(s)"
        )

        # Calculate CVaR (Expected Shortfall)
        cvar = self._calculate_cvar(returns, confidence)
        results['cvar'] = round(cvar * 100, 4)

        return results

    def _historical_var(self, returns: pd.Series, confidence: float) -> float:
        """历史模拟法VaR"""
        return returns.quantile(1 - confidence)

    def _parametric_var(self, returns: pd.Series, confidence: float) -> float:
        """参数法VaR (假设正态分布)"""
        mean = returns.mean()
        std = returns.std()
        z_score = stats.norm.ppf(1 - confidence)
        return mean + z_score * std

    def _monte_carlo_var(self, returns: pd.Series, confidence: float,
                         simulations: int = 10000) -> float:
        """蒙特卡洛VaR"""
        mean = returns.mean()
        std = returns.std()
        simulated = np.random.normal(mean, std, simulations)
        return np.percentile(simulated, (1 - confidence) * 100)

    def _calculate_cvar(self, returns: pd.Series, confidence: float) -> float:
        """计算条件VaR (Expected Shortfall)"""
        var = self._historical_var(returns, confidence)
        return returns[returns <= var].mean()

    def calculate_risk_metrics(self, returns: pd.Series,
                               risk_free_rate: float = 0.05) -> Dict:
        """
        计算风险调整收益指标

        Args:
            returns: 日收益率序列
            risk_free_rate: 无风险利率 (年化)

        Returns:
            风险指标
        """
        if len(returns) < 30:
            return {'error': 'Insufficient data'}

        # Annualization factor
        trading_days = 252

        # Basic statistics
        mean_daily = returns.mean()
        std_daily = returns.std()

        # Annualized metrics
        annual_return = mean_daily * trading_days
        annual_volatility = std_daily * np.sqrt(trading_days)

        # Sharpe Ratio
        excess_return = annual_return - risk_free_rate
        sharpe_ratio = excess_return / annual_volatility if annual_volatility > 0 else 0

        # Sortino Ratio (only downside deviation)
        negative_returns = returns[returns < 0]
        downside_std = negative_returns.std() * np.sqrt(trading_days)
        sortino_ratio = excess_return / downside_std if downside_std > 0 else 0

        # Calmar Ratio
        max_dd = self._calculate_max_drawdown(returns)
        calmar_ratio = annual_return / abs(max_dd) if max_dd != 0 else 0

        # Information Ratio (vs benchmark, using 0 as benchmark)
        info_ratio = mean_daily / std_daily * np.sqrt(trading_days) if std_daily > 0 else 0

        return {
            'annualized_return': round(annual_return * 100, 2),
            'annualized_volatility': round(annual_volatility * 100, 2),
            'sharpe_ratio': round(sharpe_ratio, 3),
            'sortino_ratio': round(sortino_ratio, 3),
            'calmar_ratio': round(calmar_ratio, 3),
            'information_ratio': round(info_ratio, 3),
            'max_drawdown': round(max_dd * 100, 2),
            'risk_free_rate': risk_free_rate,
            'interpretation': self._interpret_risk_metrics(sharpe_ratio, sortino_ratio)
        }

    def _calculate_max_drawdown(self, returns: pd.Series) -> float:
        """计算最大回撤"""
        cumulative = (1 + returns).cumprod()
        rolling_max = cumulative.expanding().max()
        drawdown = (cumulative - rolling_max) / rolling_max
        return drawdown.min()

    def _interpret_risk_metrics(self, sharpe: float, sortino: float) -> str:
        """解读风险指标"""
        if sharpe > 2:
            return 'Excellent risk-adjusted performance'
        elif sharpe > 1:
            return 'Good risk-adjusted performance'
        elif sharpe > 0.5:
            return 'Acceptable risk-adjusted performance'
        elif sharpe > 0:
            return 'Below average risk-adjusted performance'
        else:
            return 'Poor risk-adjusted performance - negative excess returns'

    def stress_test(self, portfolio_value: float, positions: List[Dict],
                    scenarios: List[str] = None) -> Dict:
        """
        压力测试

        Args:
            portfolio_value: 组合价值
            positions: 持仓列表 [{'ticker': 'AAPL', 'weight': 0.3}, ...]
            scenarios: 测试场景

        Returns:
            压力测试结果
        """
        if scenarios is None:
            scenarios = ['market_crash', 'interest_rate_shock', 'volatility_spike']

        # Predefined scenario shocks
        scenario_shocks = {
            'market_crash': {
                'description': '2008-style market crash (-40%)',
                'equity_shock': -0.40,
                'bond_shock': 0.05,
                'volatility_multiplier': 3.0
            },
            'interest_rate_shock': {
                'description': 'Interest rate spike (+200bp)',
                'equity_shock': -0.15,
                'bond_shock': -0.10,
                'volatility_multiplier': 1.5
            },
            'volatility_spike': {
                'description': 'VIX spike to 80',
                'equity_shock': -0.25,
                'bond_shock': 0.02,
                'volatility_multiplier': 4.0
            },
            'mild_correction': {
                'description': 'Typical correction (-10%)',
                'equity_shock': -0.10,
                'bond_shock': 0.01,
                'volatility_multiplier': 1.5
            },
            'stagflation': {
                'description': 'Stagflation scenario',
                'equity_shock': -0.20,
                'bond_shock': -0.15,
                'volatility_multiplier': 2.0
            }
        }

        results = {
            'portfolio_value': portfolio_value,
            'positions': positions,
            'scenarios': {}
        }

        for scenario in scenarios:
            if scenario not in scenario_shocks:
                continue

            shock = scenario_shocks[scenario]

            # Calculate portfolio impact
            total_loss = 0
            for pos in positions:
                weight = pos.get('weight', 0)
                asset_type = pos.get('type', 'equity')

                if asset_type in ['equity', 'stock']:
                    loss = weight * shock['equity_shock']
                elif asset_type == 'bond':
                    loss = weight * shock['bond_shock']
                else:
                    loss = weight * shock['equity_shock'] * 0.5  # Default

                total_loss += loss

            scenario_loss = portfolio_value * total_loss

            results['scenarios'][scenario] = {
                'description': shock['description'],
                'portfolio_loss_percent': round(total_loss * 100, 2),
                'portfolio_loss_value': round(scenario_loss, 2),
                'remaining_value': round(portfolio_value + scenario_loss, 2)
            }

        return results

    def calculate_portfolio_var(self, tickers: List[str], weights: List[float],
                                portfolio_value: float, period: str = '1y',
                                confidence: float = 0.95) -> Dict:
        """
        计算组合VaR

        Args:
            tickers: 股票代码列表
            weights: 权重列表
            portfolio_value: 组合价值
            period: 历史数据期间
            confidence: 置信水平

        Returns:
            组合VaR结果
        """
        if yf is None:
            return {'error': 'yfinance not available'}

        if len(tickers) != len(weights):
            return {'error': 'Tickers and weights must have same length'}

        if abs(sum(weights) - 1.0) > 0.01:
            return {'error': 'Weights must sum to 1'}

        # Fetch historical data
        returns_data = {}
        for ticker in tickers:
            try:
                t = yf.Ticker(ticker)
                hist = t.history(period=period)
                if not hist.empty:
                    returns_data[ticker] = hist['Close'].pct_change().dropna()
            except Exception as e:
                return {'error': f'Failed to fetch {ticker}: {e}'}

        if len(returns_data) != len(tickers):
            return {'error': 'Could not fetch all ticker data'}

        # Align data
        returns_df = pd.DataFrame(returns_data)
        returns_df = returns_df.dropna()

        # Calculate portfolio returns
        weights_array = np.array(weights)
        portfolio_returns = returns_df.dot(weights_array)

        # Calculate VaR
        var_result = self.calculate_var(portfolio_returns, confidence)

        # Calculate component VaR
        component_var = {}
        for i, ticker in enumerate(tickers):
            ticker_returns = returns_df[ticker]
            ticker_var = self._historical_var(ticker_returns, confidence)
            component_var[ticker] = {
                'weight': weights[i],
                'var': round(ticker_var * 100, 4),
                'contribution': round(ticker_var * weights[i] * 100, 4)
            }

        var_result['portfolio_value'] = portfolio_value
        var_result['var_amount'] = round(portfolio_value * abs(var_result['var_1day']) / 100, 2)
        var_result['component_var'] = component_var
        var_result['correlation_matrix'] = returns_df.corr().round(4).to_dict()

        return var_result

    def kelly_criterion(self, win_rate: float, win_loss_ratio: float) -> Dict:
        """
        凯利公式计算最优仓位

        Args:
            win_rate: 胜率 (0-1)
            win_loss_ratio: 盈亏比

        Returns:
            凯利仓位
        """
        if win_rate <= 0 or win_rate >= 1:
            return {'error': 'Win rate must be between 0 and 1'}

        if win_loss_ratio <= 0:
            return {'error': 'Win/loss ratio must be positive'}

        # Kelly formula: f* = (bp - q) / b
        # where b = win_loss_ratio, p = win_rate, q = 1 - p
        b = win_loss_ratio
        p = win_rate
        q = 1 - p

        kelly = (b * p - q) / b

        # Half-Kelly is often recommended for more conservative approach
        half_kelly = kelly / 2
        quarter_kelly = kelly / 4

        return {
            'win_rate': win_rate,
            'win_loss_ratio': win_loss_ratio,
            'full_kelly': round(kelly * 100, 2),
            'half_kelly': round(half_kelly * 100, 2),
            'quarter_kelly': round(quarter_kelly * 100, 2),
            'recommendation': 'Half Kelly' if kelly > 0 else 'Do not trade',
            'interpretation': self._interpret_kelly(kelly)
        }

    def _interpret_kelly(self, kelly: float) -> str:
        """解读凯利值"""
        if kelly <= 0:
            return 'Negative edge - do not trade this strategy'
        elif kelly < 0.1:
            return 'Small edge - use conservative position sizing'
        elif kelly < 0.25:
            return 'Moderate edge - Half Kelly recommended'
        else:
            return 'Strong edge - consider Quarter to Half Kelly'


def main():
    parser = argparse.ArgumentParser(description="Risk Management Tool")
    parser.add_argument("action", choices=["position", "var", "metrics", "stress", "kelly"],
                       help="Action to perform")
    parser.add_argument("--account", type=float, help="Account value")
    parser.add_argument("--risk", type=float, default=0.02, help="Risk per trade (decimal)")
    parser.add_argument("--entry", type=float, help="Entry price")
    parser.add_argument("--stop", type=float, help="Stop loss price")
    parser.add_argument("--ticker", help="Ticker for VaR calculation")
    parser.add_argument("--tickers", help="Comma-separated tickers for portfolio VaR")
    parser.add_argument("--weights", help="Comma-separated weights")
    parser.add_argument("--value", type=float, default=100000, help="Portfolio value")
    parser.add_argument("--confidence", type=float, default=0.95, help="VaR confidence level")
    parser.add_argument("--period", default="1y", help="Historical period")
    parser.add_argument("--win-rate", type=float, help="Win rate for Kelly")
    parser.add_argument("--win-loss-ratio", type=float, help="Win/loss ratio for Kelly")
    parser.add_argument("--output", choices=["json", "text"], default="text")

    args = parser.parse_args()

    rm = RiskManager()

    if args.action == "position":
        if not all([args.account, args.entry, args.stop]):
            print("Error: --account, --entry, and --stop required")
            sys.exit(1)
        data = rm.calculate_position_size(args.account, args.risk, args.entry, args.stop)

    elif args.action == "var":
        if args.tickers and args.weights:
            tickers = [t.strip() for t in args.tickers.split(',')]
            weights = [float(w.strip()) for w in args.weights.split(',')]
            data = rm.calculate_portfolio_var(tickers, weights, args.value, args.period, args.confidence)
        elif args.ticker and yf:
            t = yf.Ticker(args.ticker)
            hist = t.history(period=args.period)
            returns = hist['Close'].pct_change().dropna()
            data = rm.calculate_var(returns, args.confidence)
        else:
            print("Error: --ticker or (--tickers and --weights) required")
            sys.exit(1)

    elif args.action == "metrics":
        if not args.ticker or not yf:
            print("Error: --ticker required")
            sys.exit(1)
        t = yf.Ticker(args.ticker)
        hist = t.history(period=args.period)
        returns = hist['Close'].pct_change().dropna()
        data = rm.calculate_risk_metrics(returns)

    elif args.action == "stress":
        positions = [{'ticker': 'SPY', 'weight': 0.6, 'type': 'equity'},
                     {'ticker': 'TLT', 'weight': 0.4, 'type': 'bond'}]
        data = rm.stress_test(args.value, positions)

    elif args.action == "kelly":
        if not args.win_rate or not args.win_loss_ratio:
            print("Error: --win-rate and --win-loss-ratio required")
            sys.exit(1)
        data = rm.kelly_criterion(args.win_rate, args.win_loss_ratio)

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2, default=str))
    else:
        print(f"\n=== Risk Management: {args.action.title()} ===\n")
        for k, v in data.items():
            if isinstance(v, dict):
                print(f"\n{k}:")
                for k2, v2 in v.items():
                    print(f"  {k2}: {v2}")
            else:
                print(f"{k}: {v}")


if __name__ == "__main__":
    main()
