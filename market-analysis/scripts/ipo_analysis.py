#!/usr/bin/env python3
"""
IPO Analysis Module for Market Analysis
Provides scoring, prediction, and comparison for IPOs.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install pandas numpy")
    sys.exit(1)

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
try:
    from fetch_ipo_data import IPODataFetcher
except ImportError:
    IPODataFetcher = None


class IPOAnalyzer:
    """
    IPO Analysis Engine

    Features:
    - IPO scoring model
    - First day return prediction
    - Industry valuation comparison
    - Underwriter track record analysis
    """

    # Scoring weights
    SCORE_WEIGHTS = {
        'pe_comparison': 0.30,      # P/E vs industry
        'subscription_rate': 0.20,  # Historical correlation
        'market_sentiment': 0.15,   # Market mood
        'underwriter_quality': 0.10,# Underwriter track record
        'financials': 0.25          # Revenue growth, profitability
    }

    # Industry average P/E ratios (simplified)
    INDUSTRY_PE = {
        'technology': 35,
        'healthcare': 25,
        'finance': 12,
        'consumer': 20,
        'industrial': 18,
        'energy': 15,
        'materials': 14,
        'utilities': 16,
        'real_estate': 20,
        'default': 20
    }

    def __init__(self):
        self.fetcher = IPODataFetcher() if IPODataFetcher else None

    def score_ipo(self, ipo_data: Dict) -> Dict:
        """
        计算IPO综合评分

        Args:
            ipo_data: IPO数据字典

        Returns:
            评分结果
        """
        scores = {}

        # 1. P/E Comparison Score (0-100)
        pe_score = self._score_pe_ratio(
            ipo_data.get('pe_ratio'),
            ipo_data.get('industry_pe'),
            ipo_data.get('industry')
        )
        scores['pe_comparison'] = pe_score

        # 2. Subscription Rate Score (0-100)
        sub_score = self._score_subscription(ipo_data.get('subscription_rate'))
        scores['subscription_rate'] = sub_score

        # 3. Market Sentiment Score (0-100)
        sentiment_score = self._score_market_sentiment()
        scores['market_sentiment'] = sentiment_score

        # 4. Underwriter Quality Score (0-100)
        uw_score = self._score_underwriter(ipo_data.get('underwriter'))
        scores['underwriter_quality'] = uw_score

        # 5. Financial Score (0-100)
        fin_score = self._score_financials(ipo_data)
        scores['financials'] = fin_score

        # Calculate weighted total
        total_score = sum(
            scores[k] * self.SCORE_WEIGHTS[k]
            for k in self.SCORE_WEIGHTS
        )

        # Generate recommendation
        recommendation = self._generate_recommendation(total_score)

        return {
            'ticker': ipo_data.get('code', 'Unknown'),
            'name': ipo_data.get('name', 'Unknown'),
            'total_score': round(total_score, 1),
            'component_scores': {k: round(v, 1) for k, v in scores.items()},
            'weights': self.SCORE_WEIGHTS,
            'recommendation': recommendation,
            'score_interpretation': self._interpret_score(total_score),
            'risk_factors': self._identify_risks(scores, ipo_data)
        }

    def _score_pe_ratio(self, pe: float, industry_pe: float = None,
                        industry: str = None) -> float:
        """评估市盈率"""
        if pe is None:
            return 50  # Neutral if unknown

        # Get industry P/E
        if industry_pe is None:
            industry_key = (industry or 'default').lower()
            industry_pe = self.INDUSTRY_PE.get(industry_key, self.INDUSTRY_PE['default'])

        # Score based on discount/premium
        if pe <= 0:
            return 30  # Negative earnings is concerning

        ratio = pe / industry_pe

        if ratio < 0.5:
            return 95  # Significant discount
        elif ratio < 0.75:
            return 85
        elif ratio < 1.0:
            return 70
        elif ratio < 1.25:
            return 55
        elif ratio < 1.5:
            return 40
        else:
            return 25  # Significant premium

    def _score_subscription(self, rate: float) -> float:
        """评估申购倍数"""
        if rate is None:
            return 50

        # Historical correlation: higher subscription often means better returns
        # But extreme subscription might indicate overheating
        if rate < 1:
            return 20
        elif rate < 10:
            return 40
        elif rate < 50:
            return 60
        elif rate < 200:
            return 75
        elif rate < 500:
            return 85
        else:
            return 70  # Very high might indicate speculation

    def _score_market_sentiment(self) -> float:
        """评估市场情绪"""
        # Would ideally fetch real-time sentiment indicators
        # For now, return a moderate baseline
        try:
            import yfinance as yf
            vix = yf.Ticker('^VIX')
            hist = vix.history(period='5d')
            if not hist.empty:
                vix_level = hist['Close'].iloc[-1]
                # Lower VIX = better sentiment
                if vix_level < 15:
                    return 80
                elif vix_level < 20:
                    return 65
                elif vix_level < 25:
                    return 50
                elif vix_level < 30:
                    return 35
                else:
                    return 20
        except:
            pass

        return 50  # Neutral default

    def _score_underwriter(self, underwriter: str) -> float:
        """评估承销商质量"""
        if not underwriter:
            return 50

        # Top-tier underwriters
        top_tier = ['goldman sachs', 'morgan stanley', 'jpmorgan', 'jp morgan',
                    'bofa', 'bank of america', 'citi', 'citigroup',
                    '中金公司', '中信证券', '海通证券', '华泰证券', '国泰君安']

        second_tier = ['credit suisse', 'deutsche bank', 'barclays', 'ubs',
                       '招商证券', '广发证券', '申万宏源', '中银证券']

        underwriter_lower = underwriter.lower()

        for tier1 in top_tier:
            if tier1 in underwriter_lower:
                return 85

        for tier2 in second_tier:
            if tier2 in underwriter_lower:
                return 70

        return 55  # Unknown underwriter

    def _score_financials(self, ipo_data: Dict) -> float:
        """评估财务指标"""
        score = 50  # Base score

        # Revenue growth
        revenue_growth = ipo_data.get('revenue_growth')
        if revenue_growth is not None:
            if revenue_growth > 50:
                score += 20
            elif revenue_growth > 30:
                score += 15
            elif revenue_growth > 15:
                score += 10
            elif revenue_growth > 0:
                score += 5
            else:
                score -= 10

        # Profitability
        if ipo_data.get('profitable', None):
            score += 15
        elif ipo_data.get('profitable') is False:
            score -= 10

        # Funds raised (larger deals often more scrutinized)
        funds = ipo_data.get('funds_raised')
        if funds and funds > 1e9:  # > 1 billion
            score += 10

        return max(0, min(100, score))

    def _generate_recommendation(self, score: float) -> str:
        """生成投资建议"""
        if score >= 80:
            return 'Strong Buy - High probability of positive returns'
        elif score >= 65:
            return 'Buy - Favorable conditions for subscription'
        elif score >= 50:
            return 'Neutral - Consider other factors'
        elif score >= 35:
            return 'Caution - Below average prospects'
        else:
            return 'Avoid - Unfavorable risk/reward'

    def _interpret_score(self, score: float) -> str:
        """解读总分"""
        if score >= 80:
            return 'Excellent'
        elif score >= 65:
            return 'Good'
        elif score >= 50:
            return 'Average'
        elif score >= 35:
            return 'Below Average'
        else:
            return 'Poor'

    def _identify_risks(self, scores: Dict, ipo_data: Dict) -> List[str]:
        """识别风险因素"""
        risks = []

        if scores.get('pe_comparison', 50) < 40:
            risks.append('Valuation premium vs industry peers')

        if scores.get('market_sentiment', 50) < 40:
            risks.append('Weak market sentiment (elevated VIX)')

        if scores.get('financials', 50) < 40:
            risks.append('Weak financial metrics')

        if not ipo_data.get('underwriter'):
            risks.append('Unknown underwriter')

        if ipo_data.get('subscription_rate', 0) > 500:
            risks.append('Very high subscription - potential speculation')

        if not risks:
            risks.append('No major risk factors identified')

        return risks

    def predict_first_day_return(self, ipo_data: Dict) -> Dict:
        """
        预测首日涨幅

        Args:
            ipo_data: IPO数据

        Returns:
            预测结果
        """
        score_result = self.score_ipo(ipo_data)
        total_score = score_result['total_score']

        # Simple linear model based on score
        # Higher scores typically correlate with better returns
        base_return = (total_score - 50) * 0.5  # -25% to +25% base

        # Adjustments
        adjustment = 0

        # Subscription rate adjustment
        sub_rate = ipo_data.get('subscription_rate', 0)
        if sub_rate > 100:
            adjustment += min(sub_rate / 50, 10)  # Up to 10% additional

        # Market condition adjustment
        market_score = score_result['component_scores'].get('market_sentiment', 50)
        adjustment += (market_score - 50) * 0.2

        predicted_return = base_return + adjustment

        # Confidence interval (wider for lower scores)
        confidence_range = 30 - (total_score / 5)  # 24-10% range

        return {
            'ticker': ipo_data.get('code'),
            'predicted_return': round(predicted_return, 1),
            'confidence_interval': {
                'low': round(predicted_return - confidence_range, 1),
                'high': round(predicted_return + confidence_range, 1)
            },
            'confidence_level': 'Medium' if total_score > 50 else 'Low',
            'base_score': total_score,
            'disclaimer': 'Predictions are based on historical patterns and may not reflect actual outcomes'
        }

    def compare_to_industry(self, ipo_data: Dict) -> Dict:
        """
        与行业比较

        Args:
            ipo_data: IPO数据

        Returns:
            比较结果
        """
        industry = ipo_data.get('industry', 'default').lower()
        pe_ratio = ipo_data.get('pe_ratio')

        industry_pe = self.INDUSTRY_PE.get(industry, self.INDUSTRY_PE['default'])

        comparison = {
            'ticker': ipo_data.get('code'),
            'industry': industry,
            'ipo_pe': pe_ratio,
            'industry_avg_pe': industry_pe,
            'premium_discount': None,
            'valuation_assessment': None
        }

        if pe_ratio and industry_pe:
            premium = ((pe_ratio / industry_pe) - 1) * 100
            comparison['premium_discount'] = round(premium, 1)

            if premium < -20:
                comparison['valuation_assessment'] = 'Significant discount'
            elif premium < 0:
                comparison['valuation_assessment'] = 'Slight discount'
            elif premium < 20:
                comparison['valuation_assessment'] = 'In line with industry'
            elif premium < 50:
                comparison['valuation_assessment'] = 'Premium valuation'
            else:
                comparison['valuation_assessment'] = 'Significant premium'

        return comparison

    def analyze_underwriter_track_record(self, underwriter: str, market: str = 'A-SHARE') -> Dict:
        """
        分析承销商历史业绩

        Args:
            underwriter: 承销商名称
            market: 市场

        Returns:
            历史业绩分析
        """
        # Would typically query historical IPO data
        # For now, return template structure
        return {
            'underwriter': underwriter,
            'market': market,
            'note': 'Historical track record requires dedicated database',
            'general_reputation': self._assess_underwriter_reputation(underwriter)
        }

    def _assess_underwriter_reputation(self, underwriter: str) -> str:
        """评估承销商声誉"""
        if not underwriter:
            return 'Unknown'

        score = self._score_underwriter(underwriter)
        if score >= 80:
            return 'Top-tier'
        elif score >= 65:
            return 'Second-tier'
        else:
            return 'Other'


def main():
    parser = argparse.ArgumentParser(description="IPO Analysis Tool")
    parser.add_argument("code", nargs='?', help="Stock code")
    parser.add_argument("--market", choices=["A-SHARE", "HK", "US"], default="A-SHARE",
                       help="Market")
    parser.add_argument("--score", action="store_true",
                       help="Calculate IPO score")
    parser.add_argument("--predict", action="store_true",
                       help="Predict first day return")
    parser.add_argument("--compare", action="store_true",
                       help="Compare to industry")
    parser.add_argument("--underwriter", help="Analyze underwriter track record")
    parser.add_argument("--pe", type=float, help="P/E ratio")
    parser.add_argument("--industry-pe", type=float, help="Industry P/E ratio")
    parser.add_argument("--industry", help="Industry sector")
    parser.add_argument("--subscription-rate", type=float, help="Subscription rate")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format")

    args = parser.parse_args()

    analyzer = IPOAnalyzer()

    if args.underwriter:
        data = analyzer.analyze_underwriter_track_record(args.underwriter, args.market)
    else:
        # Build IPO data from arguments
        ipo_data = {
            'code': args.code or 'TEST',
            'name': args.code or 'Test IPO',
            'market': args.market,
            'pe_ratio': args.pe,
            'industry_pe': args.industry_pe,
            'industry': args.industry,
            'subscription_rate': args.subscription_rate,
            'underwriter': args.underwriter
        }

        if args.predict:
            data = analyzer.predict_first_day_return(ipo_data)
        elif args.compare:
            data = analyzer.compare_to_industry(ipo_data)
        else:
            data = analyzer.score_ipo(ipo_data)

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
    else:
        print(f"\n=== IPO Analysis ===\n")
        for k, v in data.items():
            if isinstance(v, dict):
                print(f"\n{k}:")
                for k2, v2 in v.items():
                    print(f"  {k2}: {v2}")
            elif isinstance(v, list):
                print(f"\n{k}:")
                for item in v:
                    print(f"  - {item}")
            else:
                print(f"{k}: {v}")


if __name__ == "__main__":
    main()
