#!/usr/bin/env python3
"""
Data Validator for Market Analysis
Validates and sanitizes market data to ensure quality and consistency.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of data validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    sanitized_data: Optional[Dict] = None

    def to_dict(self) -> dict:
        return {
            'is_valid': self.is_valid,
            'errors': self.errors,
            'warnings': self.warnings,
            'error_count': len(self.errors),
            'warning_count': len(self.warnings)
        }


class TickerValidator:
    """Validate stock/crypto ticker symbols."""

    TICKER_PATTERNS = {
        'US': r'^[A-Z]{1,5}(\.[A-Z])?$',
        'HK': r'^\d{5}\.HK$',
        'CN_SH': r'^\d{6}\.SS$',
        'CN_SZ': r'^\d{6}\.SZ$',
        'CRYPTO': r'^[A-Z]{2,10}-USD$',
        'CRYPTO_SIMPLE': r'^[A-Z]{2,10}$',
        'JP': r'^\d{4}\.T$',
        'UK': r'^[A-Z]{2,4}\.L$',
        'DE': r'^[A-Z]{2,5}\.DE$',
        'INDEX': r'^\^[A-Z0-9]{2,10}$'
    }

    @classmethod
    def validate(cls, ticker: str) -> ValidationResult:
        """
        Validate a ticker symbol.

        Args:
            ticker: Ticker symbol to validate

        Returns:
            ValidationResult with market type if valid
        """
        errors = []
        warnings = []

        if not ticker:
            return ValidationResult(False, ['Ticker is empty'], [], None)

        ticker = ticker.strip().upper()

        # Try to match against patterns
        matched_market = None
        for market, pattern in cls.TICKER_PATTERNS.items():
            if re.match(pattern, ticker):
                matched_market = market
                break

        if not matched_market:
            errors.append(f"Invalid ticker format: {ticker}")
            # Try to suggest correct format
            if re.match(r'^\d{4}$', ticker):
                warnings.append("Did you mean HK stock? Use 5 digits with .HK suffix (e.g., 00700.HK)")
            elif re.match(r'^\d{6}$', ticker):
                warnings.append("Did you mean A-share? Add .SS or .SZ suffix (e.g., 600519.SS)")
            elif re.match(r'^[A-Z]{2,5}$', ticker) and len(ticker) <= 5:
                warnings.append("Assuming US stock format. For crypto, add -USD suffix")
                matched_market = 'US'  # Accept as US stock

        return ValidationResult(
            is_valid=bool(matched_market),
            errors=errors,
            warnings=warnings,
            sanitized_data={'ticker': ticker, 'market': matched_market}
        )

    @classmethod
    def normalize_ticker(cls, ticker: str, target_market: str = None) -> str:
        """
        Normalize ticker to standard format.

        Args:
            ticker: Raw ticker input
            target_market: Target market format

        Returns:
            Normalized ticker string
        """
        ticker = ticker.strip().upper()

        # Auto-detect and normalize
        if target_market == 'HK' and re.match(r'^\d{1,4}$', ticker):
            return ticker.zfill(5) + '.HK'
        elif target_market in ('CN_SH', 'CN_SZ') and re.match(r'^\d{6}$', ticker):
            if ticker.startswith(('6', '9')):
                return ticker + '.SS'
            else:
                return ticker + '.SZ'
        elif target_market == 'CRYPTO' and re.match(r'^[A-Z]{2,10}$', ticker):
            return ticker + '-USD'

        return ticker


class PriceDataValidator:
    """Validate OHLCV price data."""

    @classmethod
    def validate(cls, data: Dict) -> ValidationResult:
        """
        Validate price data dictionary.

        Args:
            data: Price data with OHLCV fields

        Returns:
            ValidationResult
        """
        errors = []
        warnings = []
        sanitized = data.copy()

        required_fields = ['open', 'high', 'low', 'close']
        optional_fields = ['volume', 'adj_close', 'current_price']

        # Check required fields
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
            elif data[field] is None:
                warnings.append(f"Field {field} is None")
            elif not isinstance(data[field], (int, float)):
                errors.append(f"Field {field} must be numeric, got {type(data[field])}")

        # Validate OHLC relationships
        if all(f in data and data[f] is not None for f in required_fields):
            o, h, l, c = data['open'], data['high'], data['low'], data['close']

            if h < l:
                errors.append(f"High ({h}) cannot be less than Low ({l})")

            if o > h or o < l:
                warnings.append(f"Open ({o}) is outside High-Low range ({l}-{h})")

            if c > h or c < l:
                warnings.append(f"Close ({c}) is outside High-Low range ({l}-{h})")

            # Check for unrealistic values
            if any(v <= 0 for v in [o, h, l, c]):
                errors.append("Price values must be positive")

            # Check for extreme price movements (>50% daily)
            if o > 0 and abs(c - o) / o > 0.5:
                warnings.append(f"Extreme price movement: {((c-o)/o)*100:.1f}%")

        # Validate volume
        if 'volume' in data and data['volume'] is not None:
            if not isinstance(data['volume'], (int, float)):
                errors.append("Volume must be numeric")
            elif data['volume'] < 0:
                errors.append("Volume cannot be negative")
                sanitized['volume'] = 0

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            sanitized_data=sanitized
        )


class QuoteDataValidator:
    """Validate real-time quote data."""

    REQUIRED_FIELDS = ['current_price', 'ticker']
    OPTIONAL_FIELDS = [
        'previous_close', 'open', 'day_high', 'day_low',
        'volume', 'market_cap', 'change', 'change_percent'
    ]

    @classmethod
    def validate(cls, data: Dict) -> ValidationResult:
        """
        Validate quote data.

        Args:
            data: Quote data dictionary

        Returns:
            ValidationResult
        """
        errors = []
        warnings = []
        sanitized = data.copy()

        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if field not in data or data[field] is None:
                errors.append(f"Missing required field: {field}")

        # Validate price
        if 'current_price' in data and data['current_price'] is not None:
            price = data['current_price']
            if not isinstance(price, (int, float)):
                errors.append("current_price must be numeric")
            elif price <= 0:
                errors.append("current_price must be positive")

        # Validate change calculations
        if all(k in data and data[k] is not None
               for k in ['current_price', 'previous_close']):
            expected_change = data['current_price'] - data['previous_close']
            if 'change' in data and data['change'] is not None:
                if abs(data['change'] - expected_change) > 0.01:
                    warnings.append("Change value doesn't match price difference")
                    sanitized['change'] = round(expected_change, 2)

        # Validate percentages
        if 'change_percent' in data and data['change_percent'] is not None:
            if abs(data['change_percent']) > 100:
                warnings.append(f"Unusual change_percent: {data['change_percent']}%")

        # Check data freshness
        if 'timestamp' in data:
            try:
                ts = datetime.fromisoformat(str(data['timestamp']).replace('Z', '+00:00'))
                age = datetime.now(ts.tzinfo if ts.tzinfo else None) - ts
                if age > timedelta(hours=24):
                    warnings.append(f"Data is {age.days} days old")
            except (ValueError, TypeError):
                warnings.append("Invalid timestamp format")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            sanitized_data=sanitized
        )


class IPODataValidator:
    """Validate IPO data."""

    REQUIRED_FIELDS = ['code', 'name', 'market']
    OPTIONAL_FIELDS = [
        'issue_price', 'issue_date', 'list_date', 'shares_offered',
        'funds_raised', 'subscription_rate', 'underwriter', 'pe_ratio'
    ]

    VALID_MARKETS = ['A-SHARE', 'HK', 'US']

    @classmethod
    def validate(cls, data: Dict) -> ValidationResult:
        """
        Validate IPO data.

        Args:
            data: IPO data dictionary

        Returns:
            ValidationResult
        """
        errors = []
        warnings = []
        sanitized = data.copy()

        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if field not in data or not data[field]:
                errors.append(f"Missing required field: {field}")

        # Validate market
        if 'market' in data and data['market'] not in cls.VALID_MARKETS:
            errors.append(f"Invalid market: {data['market']}. Must be one of {cls.VALID_MARKETS}")

        # Validate dates
        for date_field in ['issue_date', 'list_date', 'subscription_start', 'subscription_end']:
            if date_field in data and data[date_field]:
                try:
                    datetime.strptime(str(data[date_field]), '%Y-%m-%d')
                except ValueError:
                    warnings.append(f"Invalid date format for {date_field}: {data[date_field]}")

        # Validate numeric fields
        numeric_fields = ['issue_price', 'shares_offered', 'funds_raised',
                         'subscription_rate', 'pe_ratio', 'industry_pe']
        for field in numeric_fields:
            if field in data and data[field] is not None:
                if not isinstance(data[field], (int, float)):
                    warnings.append(f"{field} should be numeric")
                elif data[field] < 0:
                    errors.append(f"{field} cannot be negative")

        # Validate PE ratio reasonableness
        if 'pe_ratio' in data and data['pe_ratio'] is not None:
            pe = data['pe_ratio']
            if pe < 0:
                warnings.append("Negative P/E ratio indicates losses")
            elif pe > 1000:
                warnings.append(f"Very high P/E ratio: {pe}")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            sanitized_data=sanitized
        )


class DataValidator:
    """Main validator class combining all validators."""

    @staticmethod
    def validate_ticker(ticker: str) -> ValidationResult:
        return TickerValidator.validate(ticker)

    @staticmethod
    def validate_price_data(data: Dict) -> ValidationResult:
        return PriceDataValidator.validate(data)

    @staticmethod
    def validate_quote(data: Dict) -> ValidationResult:
        return QuoteDataValidator.validate(data)

    @staticmethod
    def validate_ipo_data(data: Dict) -> ValidationResult:
        return IPODataValidator.validate(data)

    @staticmethod
    def normalize_ticker(ticker: str, market: str = None) -> str:
        return TickerValidator.normalize_ticker(ticker, market)

    @staticmethod
    def sanitize_numeric(value: Any, default: float = 0.0) -> Optional[float]:
        """
        Sanitize a value to numeric type.

        Args:
            value: Input value
            default: Default value if conversion fails

        Returns:
            Float value or None
        """
        if value is None:
            return None

        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            # Remove common formatting
            cleaned = value.replace(',', '').replace('$', '').replace('%', '')
            cleaned = cleaned.replace('亿', 'e8').replace('万', 'e4')

            try:
                return float(cleaned)
            except ValueError:
                return default

        return default

    @staticmethod
    def sanitize_date(value: Any, format_str: str = '%Y-%m-%d') -> Optional[str]:
        """
        Sanitize a date value to standard format.

        Args:
            value: Input date value
            format_str: Output format string

        Returns:
            Formatted date string or None
        """
        if value is None:
            return None

        if isinstance(value, datetime):
            return value.strftime(format_str)

        if isinstance(value, str):
            # Try common formats
            formats = [
                '%Y-%m-%d', '%Y/%m/%d', '%d/%m/%Y', '%m/%d/%Y',
                '%Y-%m-%d %H:%M:%S', '%Y%m%d'
            ]
            for fmt in formats:
                try:
                    dt = datetime.strptime(value, fmt)
                    return dt.strftime(format_str)
                except ValueError:
                    continue

        return None


def main():
    parser = argparse.ArgumentParser(description="Market Data Validator")
    parser.add_argument("action", choices=["ticker", "price", "quote", "ipo"],
                       help="Type of validation")
    parser.add_argument("--data", help="JSON data to validate")
    parser.add_argument("--ticker", help="Ticker symbol to validate")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format")

    args = parser.parse_args()

    if args.action == "ticker":
        if not args.ticker:
            print("Error: --ticker required for ticker validation", file=sys.stderr)
            sys.exit(1)
        result = DataValidator.validate_ticker(args.ticker)

    else:
        if not args.data:
            print("Error: --data required", file=sys.stderr)
            sys.exit(1)

        try:
            data = json.loads(args.data)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)

        if args.action == "price":
            result = DataValidator.validate_price_data(data)
        elif args.action == "quote":
            result = DataValidator.validate_quote(data)
        elif args.action == "ipo":
            result = DataValidator.validate_ipo_data(data)

    # Output results
    if args.output == "json":
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"\n=== Validation Result ===\n")
        print(f"Valid: {result.is_valid}")

        if result.errors:
            print(f"\nErrors ({len(result.errors)}):")
            for err in result.errors:
                print(f"  ✗ {err}")

        if result.warnings:
            print(f"\nWarnings ({len(result.warnings)}):")
            for warn in result.warnings:
                print(f"  ⚠ {warn}")

        if result.sanitized_data:
            print(f"\nSanitized Data:")
            for k, v in result.sanitized_data.items():
                print(f"  {k}: {v}")

    sys.exit(0 if result.is_valid else 1)


if __name__ == "__main__":
    main()
