#!/usr/bin/env python3
"""
Options Analysis Module
Provides Greeks calculation, Black-Scholes pricing, and strategy analysis.
"""

import argparse
import json
import sys
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path

try:
    import numpy as np
    from scipy.stats import norm
    from scipy.optimize import brentq
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install numpy scipy")
    sys.exit(1)


class OptionsAnalyzer:
    """
    Options Analysis Engine

    Features:
    - Black-Scholes pricing
    - Greeks calculation (Delta, Gamma, Theta, Vega, Rho)
    - Implied volatility calculation
    - Strategy payoff analysis
    """

    def __init__(self):
        pass

    def black_scholes(self, S: float, K: float, T: float, r: float,
                      sigma: float, option_type: str = 'call') -> Dict:
        """
        Black-Scholes期权定价

        Args:
            S: 标的资产当前价格
            K: 行权价
            T: 到期时间（年）
            r: 无风险利率
            sigma: 波动率
            option_type: 'call' 或 'put'

        Returns:
            期权价格和希腊字母
        """
        if T <= 0:
            # At expiration
            if option_type == 'call':
                return {'price': max(S - K, 0), 'intrinsic': max(S - K, 0), 'time_value': 0}
            else:
                return {'price': max(K - S, 0), 'intrinsic': max(K - S, 0), 'time_value': 0}

        # Calculate d1 and d2
        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)

        # Calculate option price
        if option_type == 'call':
            price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
            intrinsic = max(S - K, 0)
        else:
            price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
            intrinsic = max(K - S, 0)

        time_value = price - intrinsic

        # Calculate Greeks
        greeks = self._calculate_greeks(S, K, T, r, sigma, d1, d2, option_type)

        return {
            'price': round(price, 4),
            'intrinsic_value': round(intrinsic, 4),
            'time_value': round(time_value, 4),
            'greeks': greeks,
            'inputs': {
                'spot': S,
                'strike': K,
                'time_to_expiry': T,
                'risk_free_rate': r,
                'volatility': sigma,
                'option_type': option_type
            }
        }

    def _calculate_greeks(self, S: float, K: float, T: float, r: float,
                          sigma: float, d1: float, d2: float,
                          option_type: str) -> Dict:
        """计算希腊字母"""
        sqrt_T = math.sqrt(T)

        # Delta
        if option_type == 'call':
            delta = norm.cdf(d1)
        else:
            delta = norm.cdf(d1) - 1

        # Gamma (same for call and put)
        gamma = norm.pdf(d1) / (S * sigma * sqrt_T)

        # Theta
        theta_common = -(S * norm.pdf(d1) * sigma) / (2 * sqrt_T)
        if option_type == 'call':
            theta = theta_common - r * K * math.exp(-r * T) * norm.cdf(d2)
        else:
            theta = theta_common + r * K * math.exp(-r * T) * norm.cdf(-d2)
        theta = theta / 365  # Daily theta

        # Vega (same for call and put)
        vega = S * sqrt_T * norm.pdf(d1) / 100  # Per 1% change in vol

        # Rho
        if option_type == 'call':
            rho = K * T * math.exp(-r * T) * norm.cdf(d2) / 100
        else:
            rho = -K * T * math.exp(-r * T) * norm.cdf(-d2) / 100

        return {
            'delta': round(delta, 4),
            'gamma': round(gamma, 6),
            'theta': round(theta, 4),
            'vega': round(vega, 4),
            'rho': round(rho, 4)
        }

    def implied_volatility(self, market_price: float, S: float, K: float,
                           T: float, r: float, option_type: str = 'call') -> Dict:
        """
        计算隐含波动率

        Args:
            market_price: 期权市场价格
            S: 标的价格
            K: 行权价
            T: 到期时间（年）
            r: 无风险利率
            option_type: 期权类型

        Returns:
            隐含波动率
        """
        if T <= 0:
            return {'error': 'Option has expired'}

        def objective(sigma):
            bs = self.black_scholes(S, K, T, r, sigma, option_type)
            return bs['price'] - market_price

        try:
            # Use Brent's method to find IV
            iv = brentq(objective, 0.001, 5.0)

            return {
                'implied_volatility': round(iv * 100, 2),
                'iv_decimal': round(iv, 4),
                'market_price': market_price,
                'theoretical_price': round(self.black_scholes(S, K, T, r, iv, option_type)['price'], 4),
                'annualized_iv': f"{iv * 100:.2f}%"
            }
        except ValueError:
            return {'error': 'Could not converge to IV solution'}

    def analyze_strategy(self, strategy: str, S: float, positions: List[Dict],
                         price_range: Tuple[float, float] = None) -> Dict:
        """
        分析期权策略

        Args:
            strategy: 策略名称
            S: 当前标的价格
            positions: 持仓列表
            price_range: 价格范围

        Returns:
            策略分析
        """
        if price_range is None:
            price_range = (S * 0.7, S * 1.3)

        # Generate price points
        prices = np.linspace(price_range[0], price_range[1], 50)

        # Calculate payoff at each price
        payoffs = []
        for price in prices:
            total_payoff = 0
            for pos in positions:
                payoff = self._position_payoff(
                    price,
                    pos['strike'],
                    pos['premium'],
                    pos['type'],
                    pos['quantity']
                )
                total_payoff += payoff
            payoffs.append(total_payoff)

        payoffs = np.array(payoffs)

        # Find breakeven points
        breakevens = self._find_breakevens(prices, payoffs)

        # Calculate max profit/loss
        max_profit = max(payoffs)
        max_loss = min(payoffs)

        # Risk/reward ratio
        if max_loss < 0:
            risk_reward = abs(max_profit / max_loss) if max_loss != 0 else float('inf')
        else:
            risk_reward = float('inf')

        return {
            'strategy': strategy,
            'current_price': S,
            'positions': positions,
            'breakeven_points': [round(b, 2) for b in breakevens],
            'max_profit': round(max_profit, 2) if max_profit != float('inf') else 'Unlimited',
            'max_loss': round(max_loss, 2) if max_loss != float('-inf') else 'Unlimited',
            'risk_reward_ratio': round(risk_reward, 2) if risk_reward != float('inf') else 'Unlimited',
            'profit_probability': self._estimate_profit_probability(payoffs),
            'payoff_at_current': round(payoffs[len(payoffs) // 2], 2)
        }

    def _position_payoff(self, S_T: float, K: float, premium: float,
                         option_type: str, quantity: int) -> float:
        """计算单个持仓到期盈亏"""
        if option_type == 'call':
            intrinsic = max(S_T - K, 0)
        elif option_type == 'put':
            intrinsic = max(K - S_T, 0)
        else:
            return 0

        payoff = (intrinsic - premium) * quantity * 100  # 100 shares per contract
        return payoff

    def _find_breakevens(self, prices: np.ndarray, payoffs: np.ndarray) -> List[float]:
        """找到盈亏平衡点"""
        breakevens = []

        for i in range(len(payoffs) - 1):
            if payoffs[i] * payoffs[i + 1] < 0:  # Sign change
                # Linear interpolation
                be = prices[i] - payoffs[i] * (prices[i + 1] - prices[i]) / (payoffs[i + 1] - payoffs[i])
                breakevens.append(be)

        return breakevens

    def _estimate_profit_probability(self, payoffs: np.ndarray) -> str:
        """估计盈利概率"""
        profitable = sum(1 for p in payoffs if p > 0)
        prob = profitable / len(payoffs) * 100
        return f"{prob:.1f}%"

    def get_strategy_templates(self) -> Dict:
        """获取常见策略模板"""
        return {
            'covered_call': {
                'description': 'Long stock + Short call',
                'sentiment': 'Neutral to slightly bullish',
                'risk': 'Limited profit, substantial downside',
                'positions': [
                    {'type': 'stock', 'quantity': 100},
                    {'type': 'call', 'quantity': -1, 'delta_from_atm': 1}
                ]
            },
            'protective_put': {
                'description': 'Long stock + Long put',
                'sentiment': 'Bullish with downside protection',
                'risk': 'Limited loss, unlimited profit potential',
                'positions': [
                    {'type': 'stock', 'quantity': 100},
                    {'type': 'put', 'quantity': 1, 'delta_from_atm': -1}
                ]
            },
            'bull_call_spread': {
                'description': 'Long lower strike call + Short higher strike call',
                'sentiment': 'Moderately bullish',
                'risk': 'Limited profit and loss',
                'positions': [
                    {'type': 'call', 'quantity': 1, 'delta_from_atm': 0},
                    {'type': 'call', 'quantity': -1, 'delta_from_atm': 2}
                ]
            },
            'bear_put_spread': {
                'description': 'Long higher strike put + Short lower strike put',
                'sentiment': 'Moderately bearish',
                'risk': 'Limited profit and loss',
                'positions': [
                    {'type': 'put', 'quantity': 1, 'delta_from_atm': 0},
                    {'type': 'put', 'quantity': -1, 'delta_from_atm': -2}
                ]
            },
            'iron_condor': {
                'description': 'Bull put spread + Bear call spread',
                'sentiment': 'Neutral, expecting low volatility',
                'risk': 'Limited profit and loss',
                'positions': [
                    {'type': 'put', 'quantity': 1, 'delta_from_atm': -2},
                    {'type': 'put', 'quantity': -1, 'delta_from_atm': -1},
                    {'type': 'call', 'quantity': -1, 'delta_from_atm': 1},
                    {'type': 'call', 'quantity': 1, 'delta_from_atm': 2}
                ]
            },
            'straddle': {
                'description': 'Long ATM call + Long ATM put',
                'sentiment': 'Expecting big move, direction unknown',
                'risk': 'Limited loss (premium paid), unlimited profit',
                'positions': [
                    {'type': 'call', 'quantity': 1, 'delta_from_atm': 0},
                    {'type': 'put', 'quantity': 1, 'delta_from_atm': 0}
                ]
            },
            'strangle': {
                'description': 'Long OTM call + Long OTM put',
                'sentiment': 'Expecting big move, cheaper than straddle',
                'risk': 'Limited loss, unlimited profit potential',
                'positions': [
                    {'type': 'call', 'quantity': 1, 'delta_from_atm': 1},
                    {'type': 'put', 'quantity': 1, 'delta_from_atm': -1}
                ]
            },
            'butterfly': {
                'description': 'Long 1 lower + Short 2 middle + Long 1 higher',
                'sentiment': 'Neutral, expecting price to stay near middle strike',
                'risk': 'Limited profit and loss',
                'positions': [
                    {'type': 'call', 'quantity': 1, 'delta_from_atm': -1},
                    {'type': 'call', 'quantity': -2, 'delta_from_atm': 0},
                    {'type': 'call', 'quantity': 1, 'delta_from_atm': 1}
                ]
            }
        }

    def analyze_iv_percentile(self, current_iv: float, historical_ivs: List[float]) -> Dict:
        """
        分析IV百分位

        Args:
            current_iv: 当前IV
            historical_ivs: 历史IV列表

        Returns:
            IV分析
        """
        if not historical_ivs:
            return {'error': 'No historical data'}

        historical = np.array(historical_ivs)
        percentile = (historical < current_iv).sum() / len(historical) * 100

        return {
            'current_iv': round(current_iv, 2),
            'iv_percentile': round(percentile, 1),
            'iv_rank': round((current_iv - historical.min()) / (historical.max() - historical.min()) * 100, 1),
            'historical_mean': round(historical.mean(), 2),
            'historical_median': round(np.median(historical), 2),
            'historical_min': round(historical.min(), 2),
            'historical_max': round(historical.max(), 2),
            'interpretation': self._interpret_iv_percentile(percentile)
        }

    def _interpret_iv_percentile(self, percentile: float) -> str:
        """解读IV百分位"""
        if percentile > 80:
            return 'High IV - Consider selling premium strategies'
        elif percentile > 50:
            return 'Above average IV - Neutral to premium selling'
        elif percentile > 20:
            return 'Below average IV - Consider buying premium'
        else:
            return 'Low IV - Good time to buy options'


def main():
    parser = argparse.ArgumentParser(description="Options Analysis Tool")
    parser.add_argument("action", choices=["price", "iv", "strategy", "greeks", "templates"],
                       help="Action to perform")
    parser.add_argument("--spot", "-S", type=float, help="Spot price")
    parser.add_argument("--strike", "-K", type=float, help="Strike price")
    parser.add_argument("--time", "-T", type=float, help="Time to expiry (years)")
    parser.add_argument("--rate", "-r", type=float, default=0.05, help="Risk-free rate")
    parser.add_argument("--vol", "-v", type=float, help="Volatility (decimal)")
    parser.add_argument("--type", choices=["call", "put"], default="call", help="Option type")
    parser.add_argument("--market-price", type=float, help="Market price for IV calculation")
    parser.add_argument("--output", choices=["json", "text"], default="text")

    args = parser.parse_args()

    analyzer = OptionsAnalyzer()

    if args.action == "price" or args.action == "greeks":
        if not all([args.spot, args.strike, args.time, args.vol]):
            print("Error: --spot, --strike, --time, and --vol required")
            sys.exit(1)
        data = analyzer.black_scholes(args.spot, args.strike, args.time, args.rate, args.vol, args.type)

    elif args.action == "iv":
        if not all([args.spot, args.strike, args.time, args.market_price]):
            print("Error: --spot, --strike, --time, and --market-price required")
            sys.exit(1)
        data = analyzer.implied_volatility(args.market_price, args.spot, args.strike, args.time, args.rate, args.type)

    elif args.action == "strategy":
        # Example strategy analysis
        positions = [
            {'strike': 100, 'premium': 5.0, 'type': 'call', 'quantity': 1},
            {'strike': 110, 'premium': 2.0, 'type': 'call', 'quantity': -1}
        ]
        S = args.spot or 100
        data = analyzer.analyze_strategy("Bull Call Spread", S, positions)

    elif args.action == "templates":
        data = analyzer.get_strategy_templates()

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2, default=str))
    else:
        print(f"\n=== Options Analysis ===\n")
        for k, v in data.items():
            if isinstance(v, dict):
                print(f"\n{k}:")
                for k2, v2 in v.items():
                    print(f"  {k2}: {v2}")
            else:
                print(f"{k}: {v}")


if __name__ == "__main__":
    main()
