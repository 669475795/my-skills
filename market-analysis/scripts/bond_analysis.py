#!/usr/bin/env python3
"""
Bond Analysis Module
Provides duration, convexity, yield curve analysis, and bond pricing.
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
    from scipy.optimize import brentq
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install numpy scipy")
    sys.exit(1)


class BondAnalyzer:
    """
    Bond Analysis Engine

    Features:
    - Bond pricing (present value)
    - Yield to maturity calculation
    - Duration (Macaulay and Modified)
    - Convexity
    - Yield curve analysis
    """

    def __init__(self):
        pass

    def price_bond(self, face_value: float, coupon_rate: float, ytm: float,
                   years_to_maturity: float, frequency: int = 2) -> Dict:
        """
        计算债券价格

        Args:
            face_value: 面值
            coupon_rate: 票面利率 (年化)
            ytm: 到期收益率 (年化)
            years_to_maturity: 到期年限
            frequency: 付息频率 (1=年付, 2=半年付, 4=季付)

        Returns:
            债券定价结果
        """
        coupon = face_value * coupon_rate / frequency
        periods = int(years_to_maturity * frequency)
        period_ytm = ytm / frequency

        # Present value of coupons
        pv_coupons = 0
        for t in range(1, periods + 1):
            pv_coupons += coupon / ((1 + period_ytm) ** t)

        # Present value of face value
        pv_face = face_value / ((1 + period_ytm) ** periods)

        price = pv_coupons + pv_face

        # Premium/Discount status
        if price > face_value:
            status = 'Premium'
        elif price < face_value:
            status = 'Discount'
        else:
            status = 'Par'

        return {
            'price': round(price, 2),
            'face_value': face_value,
            'coupon_rate': f"{coupon_rate * 100:.2f}%",
            'ytm': f"{ytm * 100:.2f}%",
            'years_to_maturity': years_to_maturity,
            'frequency': frequency,
            'pv_coupons': round(pv_coupons, 2),
            'pv_face_value': round(pv_face, 2),
            'status': status,
            'current_yield': f"{(coupon * frequency / price) * 100:.2f}%"
        }

    def calculate_ytm(self, price: float, face_value: float, coupon_rate: float,
                      years_to_maturity: float, frequency: int = 2) -> Dict:
        """
        计算到期收益率

        Args:
            price: 当前价格
            face_value: 面值
            coupon_rate: 票面利率
            years_to_maturity: 到期年限
            frequency: 付息频率

        Returns:
            YTM结果
        """
        coupon = face_value * coupon_rate / frequency
        periods = int(years_to_maturity * frequency)

        def bond_price_diff(ytm):
            period_ytm = ytm / frequency
            pv = 0
            for t in range(1, periods + 1):
                pv += coupon / ((1 + period_ytm) ** t)
            pv += face_value / ((1 + period_ytm) ** periods)
            return pv - price

        try:
            ytm = brentq(bond_price_diff, -0.5, 1.0)

            return {
                'ytm': round(ytm * 100, 4),
                'ytm_decimal': round(ytm, 6),
                'price': price,
                'face_value': face_value,
                'coupon_rate': f"{coupon_rate * 100:.2f}%",
                'interpretation': self._interpret_ytm(ytm, coupon_rate)
            }
        except ValueError:
            return {'error': 'Could not calculate YTM'}

    def _interpret_ytm(self, ytm: float, coupon_rate: float) -> str:
        """解读YTM"""
        if ytm > coupon_rate:
            return 'YTM > Coupon: Bond trading at discount'
        elif ytm < coupon_rate:
            return 'YTM < Coupon: Bond trading at premium'
        else:
            return 'YTM = Coupon: Bond trading at par'

    def calculate_duration(self, face_value: float, coupon_rate: float, ytm: float,
                           years_to_maturity: float, frequency: int = 2) -> Dict:
        """
        计算久期

        Args:
            face_value: 面值
            coupon_rate: 票面利率
            ytm: 到期收益率
            years_to_maturity: 到期年限
            frequency: 付息频率

        Returns:
            久期结果
        """
        coupon = face_value * coupon_rate / frequency
        periods = int(years_to_maturity * frequency)
        period_ytm = ytm / frequency

        # Calculate bond price
        price = 0
        for t in range(1, periods + 1):
            price += coupon / ((1 + period_ytm) ** t)
        price += face_value / ((1 + period_ytm) ** periods)

        # Macaulay Duration
        weighted_cf = 0
        for t in range(1, periods + 1):
            pv_cf = coupon / ((1 + period_ytm) ** t)
            weighted_cf += (t / frequency) * pv_cf

        # Add final payment
        pv_face = face_value / ((1 + period_ytm) ** periods)
        weighted_cf += (periods / frequency) * pv_face

        macaulay_duration = weighted_cf / price

        # Modified Duration
        modified_duration = macaulay_duration / (1 + period_ytm)

        # Dollar Duration
        dollar_duration = modified_duration * price / 100  # Per 1% change

        return {
            'macaulay_duration': round(macaulay_duration, 4),
            'modified_duration': round(modified_duration, 4),
            'dollar_duration': round(dollar_duration, 2),
            'price': round(price, 2),
            'interpretation': self._interpret_duration(modified_duration),
            'price_sensitivity': f"For 1% rate change: ~${round(dollar_duration, 2)} price change"
        }

    def _interpret_duration(self, duration: float) -> str:
        """解读久期"""
        if duration < 3:
            return 'Short duration - Low interest rate sensitivity'
        elif duration < 7:
            return 'Medium duration - Moderate rate sensitivity'
        elif duration < 12:
            return 'Long duration - High rate sensitivity'
        else:
            return 'Very long duration - Very high rate sensitivity'

    def calculate_convexity(self, face_value: float, coupon_rate: float, ytm: float,
                            years_to_maturity: float, frequency: int = 2) -> Dict:
        """
        计算凸性

        Args:
            face_value: 面值
            coupon_rate: 票面利率
            ytm: 到期收益率
            years_to_maturity: 到期年限
            frequency: 付息频率

        Returns:
            凸性结果
        """
        coupon = face_value * coupon_rate / frequency
        periods = int(years_to_maturity * frequency)
        period_ytm = ytm / frequency

        # Calculate price
        price = 0
        for t in range(1, periods + 1):
            price += coupon / ((1 + period_ytm) ** t)
        price += face_value / ((1 + period_ytm) ** periods)

        # Calculate convexity
        convexity_sum = 0
        for t in range(1, periods + 1):
            pv_cf = coupon / ((1 + period_ytm) ** t)
            convexity_sum += t * (t + 1) * pv_cf

        # Add face value component
        pv_face = face_value / ((1 + period_ytm) ** periods)
        convexity_sum += periods * (periods + 1) * pv_face

        convexity = convexity_sum / (price * ((1 + period_ytm) ** 2) * (frequency ** 2))

        return {
            'convexity': round(convexity, 4),
            'price': round(price, 2),
            'interpretation': 'Higher convexity is better - price rises more when rates fall, falls less when rates rise',
            'convexity_adjustment': f"For 1% rate change: ~{round(0.5 * convexity * 0.01 ** 2 * 100, 4)}% additional price change"
        }

    def price_change_estimate(self, modified_duration: float, convexity: float,
                              yield_change: float) -> Dict:
        """
        估计价格变化

        Args:
            modified_duration: 修正久期
            convexity: 凸性
            yield_change: 收益率变化 (如 0.01 = 1%)

        Returns:
            价格变化估计
        """
        # Duration effect
        duration_effect = -modified_duration * yield_change

        # Convexity effect
        convexity_effect = 0.5 * convexity * (yield_change ** 2)

        # Total effect
        total_effect = duration_effect + convexity_effect

        return {
            'yield_change': f"{yield_change * 100:.2f}%",
            'duration_effect': f"{duration_effect * 100:.4f}%",
            'convexity_effect': f"{convexity_effect * 100:.4f}%",
            'total_price_change': f"{total_effect * 100:.4f}%",
            'note': 'Positive = price increase, Negative = price decrease'
        }

    def analyze_yield_curve(self, yields: Dict[str, float]) -> Dict:
        """
        分析收益率曲线

        Args:
            yields: {maturity: yield} 字典，如 {'1y': 0.05, '10y': 0.06}

        Returns:
            曲线分析
        """
        if len(yields) < 2:
            return {'error': 'Need at least 2 points'}

        # Sort by maturity
        maturity_order = ['1m', '3m', '6m', '1y', '2y', '3y', '5y', '7y', '10y', '20y', '30y']
        sorted_yields = []
        for m in maturity_order:
            if m in yields:
                sorted_yields.append((m, yields[m]))

        if len(sorted_yields) < 2:
            return {'error': 'Invalid maturity keys'}

        # Calculate spreads
        maturities = [y[0] for y in sorted_yields]
        yield_values = [y[1] for y in sorted_yields]

        # Curve shape
        spread_2_10 = None
        if '2y' in yields and '10y' in yields:
            spread_2_10 = yields['10y'] - yields['2y']

        spread_3m_10y = None
        if '3m' in yields and '10y' in yields:
            spread_3m_10y = yields['10y'] - yields['3m']

        # Determine shape
        if yield_values[-1] > yield_values[0]:
            shape = 'Normal (upward sloping)'
            if spread_2_10 and spread_2_10 > 0.01:
                shape = 'Normal/Steep'
        elif yield_values[-1] < yield_values[0]:
            shape = 'Inverted (downward sloping)'
        else:
            shape = 'Flat'

        # Inversion warning
        warnings = []
        if spread_2_10 and spread_2_10 < 0:
            warnings.append('2Y-10Y spread inverted - historically a recession indicator')
        if spread_3m_10y and spread_3m_10y < 0:
            warnings.append('3M-10Y spread inverted - strong recession signal')

        return {
            'shape': shape,
            'yields': dict(sorted_yields),
            'spread_2y_10y': round(spread_2_10 * 100, 2) if spread_2_10 else None,
            'spread_3m_10y': round(spread_3m_10y * 100, 2) if spread_3m_10y else None,
            'steepness': round((yield_values[-1] - yield_values[0]) * 100, 2),
            'warnings': warnings if warnings else ['No warnings'],
            'interpretation': self._interpret_curve_shape(shape)
        }

    def _interpret_curve_shape(self, shape: str) -> str:
        """解读曲线形态"""
        if 'Normal' in shape:
            return 'Healthy economy expected - longer-term rates higher reflecting growth expectations'
        elif 'Inverted' in shape:
            return 'Potential recession signal - short-term rates higher reflecting tight monetary policy'
        else:
            return 'Uncertainty in economic outlook'

    def compare_bonds(self, bonds: List[Dict]) -> Dict:
        """
        比较多个债券

        Args:
            bonds: 债券列表

        Returns:
            比较结果
        """
        results = []

        for bond in bonds:
            try:
                price_result = self.price_bond(
                    bond['face_value'],
                    bond['coupon_rate'],
                    bond['ytm'],
                    bond['years_to_maturity'],
                    bond.get('frequency', 2)
                )

                duration_result = self.calculate_duration(
                    bond['face_value'],
                    bond['coupon_rate'],
                    bond['ytm'],
                    bond['years_to_maturity'],
                    bond.get('frequency', 2)
                )

                results.append({
                    'name': bond.get('name', 'Bond'),
                    'price': price_result['price'],
                    'ytm': bond['ytm'] * 100,
                    'coupon': bond['coupon_rate'] * 100,
                    'duration': duration_result['modified_duration'],
                    'years': bond['years_to_maturity']
                })
            except Exception as e:
                results.append({
                    'name': bond.get('name', 'Bond'),
                    'error': str(e)
                })

        return {
            'bonds': results,
            'recommendation': self._recommend_bond(results)
        }

    def _recommend_bond(self, bonds: List[Dict]) -> str:
        """推荐债券"""
        valid_bonds = [b for b in bonds if 'error' not in b]
        if not valid_bonds:
            return 'No valid bonds to compare'

        # Simple recommendation: highest yield for given duration category
        highest_yield = max(valid_bonds, key=lambda x: x['ytm'])
        return f"Highest yield: {highest_yield['name']} at {highest_yield['ytm']:.2f}%"


def main():
    parser = argparse.ArgumentParser(description="Bond Analysis Tool")
    parser.add_argument("action", choices=["price", "ytm", "duration", "convexity", "curve", "sensitivity"],
                       help="Action to perform")
    parser.add_argument("--face", type=float, default=1000, help="Face value")
    parser.add_argument("--coupon", type=float, help="Coupon rate (decimal)")
    parser.add_argument("--ytm", type=float, help="Yield to maturity (decimal)")
    parser.add_argument("--years", type=float, help="Years to maturity")
    parser.add_argument("--price", type=float, help="Current price")
    parser.add_argument("--frequency", type=int, default=2, help="Coupon frequency")
    parser.add_argument("--yield-change", type=float, help="Yield change for sensitivity")
    parser.add_argument("--output", choices=["json", "text"], default="text")

    args = parser.parse_args()

    analyzer = BondAnalyzer()

    if args.action == "price":
        if not all([args.coupon, args.ytm, args.years]):
            print("Error: --coupon, --ytm, and --years required")
            sys.exit(1)
        data = analyzer.price_bond(args.face, args.coupon, args.ytm, args.years, args.frequency)

    elif args.action == "ytm":
        if not all([args.price, args.coupon, args.years]):
            print("Error: --price, --coupon, and --years required")
            sys.exit(1)
        data = analyzer.calculate_ytm(args.price, args.face, args.coupon, args.years, args.frequency)

    elif args.action == "duration":
        if not all([args.coupon, args.ytm, args.years]):
            print("Error: --coupon, --ytm, and --years required")
            sys.exit(1)
        data = analyzer.calculate_duration(args.face, args.coupon, args.ytm, args.years, args.frequency)

    elif args.action == "convexity":
        if not all([args.coupon, args.ytm, args.years]):
            print("Error: --coupon, --ytm, and --years required")
            sys.exit(1)
        data = analyzer.calculate_convexity(args.face, args.coupon, args.ytm, args.years, args.frequency)

    elif args.action == "curve":
        # Example yield curve
        yields = {'3m': 0.05, '1y': 0.045, '2y': 0.04, '5y': 0.042, '10y': 0.045, '30y': 0.05}
        data = analyzer.analyze_yield_curve(yields)

    elif args.action == "sensitivity":
        if not all([args.coupon, args.ytm, args.years, args.yield_change]):
            print("Error: --coupon, --ytm, --years, and --yield-change required")
            sys.exit(1)
        duration = analyzer.calculate_duration(args.face, args.coupon, args.ytm, args.years, args.frequency)
        convexity = analyzer.calculate_convexity(args.face, args.coupon, args.ytm, args.years, args.frequency)
        data = analyzer.price_change_estimate(duration['modified_duration'], convexity['convexity'], args.yield_change)

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2, default=str))
    else:
        print(f"\n=== Bond Analysis: {args.action.title()} ===\n")
        for k, v in data.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
