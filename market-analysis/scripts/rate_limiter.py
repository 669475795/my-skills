#!/usr/bin/env python3
"""
Rate Limiter for Market Analysis
Implements token bucket algorithm with exponential backoff retry logic.
"""

import argparse
import json
import sys
import threading
import time
from dataclasses import dataclass, field
from typing import Dict, Optional, Callable, Any
from functools import wraps

try:
    from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
    TENACITY_AVAILABLE = True
except ImportError:
    TENACITY_AVAILABLE = False


@dataclass
class TokenBucket:
    """
    Token bucket for rate limiting.

    Attributes:
        rate: Tokens added per period
        period: Time period in seconds
        burst: Maximum tokens (bucket capacity)
        tokens: Current token count
        last_update: Last update timestamp
    """
    rate: int
    period: float = 1.0
    burst: Optional[int] = None
    tokens: float = field(init=False)
    last_update: float = field(init=False)
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def __post_init__(self):
        self.burst = self.burst or self.rate
        self.tokens = float(self.burst)
        self.last_update = time.time()

    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_update
        refill = elapsed * (self.rate / self.period)
        self.tokens = min(self.burst, self.tokens + refill)
        self.last_update = now

    def acquire(self, tokens: int = 1, blocking: bool = True,
                timeout: float = None) -> bool:
        """
        Acquire tokens from bucket.

        Args:
            tokens: Number of tokens to acquire
            blocking: If True, wait until tokens available
            timeout: Maximum wait time (None = infinite)

        Returns:
            True if tokens acquired, False otherwise
        """
        deadline = time.time() + timeout if timeout else None

        with self.lock:
            while True:
                self._refill()

                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True

                if not blocking:
                    return False

                if deadline and time.time() >= deadline:
                    return False

                # Calculate wait time for enough tokens
                tokens_needed = tokens - self.tokens
                wait_time = tokens_needed * self.period / self.rate

                if deadline:
                    wait_time = min(wait_time, deadline - time.time())

                if wait_time > 0:
                    # Release lock while waiting
                    self.lock.release()
                    try:
                        time.sleep(wait_time)
                    finally:
                        self.lock.acquire()

    def wait_time(self, tokens: int = 1) -> float:
        """Calculate wait time for acquiring tokens."""
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                return 0.0
            tokens_needed = tokens - self.tokens
            return tokens_needed * self.period / self.rate


class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded."""
    def __init__(self, source: str, wait_time: float):
        self.source = source
        self.wait_time = wait_time
        super().__init__(f"Rate limit exceeded for {source}. Wait {wait_time:.1f}s")


class RateLimiter:
    """
    Rate limiter manager for multiple data sources.

    Supports per-source rate limits with configurable rates and burst capacity.
    """

    # Default rate limits (requests per period)
    DEFAULT_LIMITS = {
        'yahoo_finance': {'rate': 2000, 'period': 3600},       # 2000/hour
        'coingecko': {'rate': 50, 'period': 60},               # 50/minute
        'eastmoney': {'rate': 100, 'period': 60},              # 100/minute
        'sina_finance': {'rate': 100, 'period': 60},           # 100/minute
        'cninfo': {'rate': 30, 'period': 60},                  # 30/minute
        'hkex': {'rate': 30, 'period': 60},                    # 30/minute
        'sec_edgar': {'rate': 10, 'period': 1},                # 10/second
        'fred': {'rate': 120, 'period': 60},                   # 120/minute
        'nasdaq_ipo': {'rate': 30, 'period': 60},              # 30/minute
        'alpha_vantage': {'rate': 5, 'period': 60},            # 5/minute
        'default': {'rate': 60, 'period': 60}                  # 60/minute
    }

    # Minimum delay between requests (seconds)
    MIN_DELAYS = {
        'yahoo_finance': 0.5,
        'coingecko': 1.2,
        'eastmoney': 0.5,
        'sina_finance': 0.3,
        'cninfo': 2.0,
        'hkex': 2.0,
        'sec_edgar': 0.1,
        'fred': 0.5,
        'nasdaq_ipo': 2.0,
        'alpha_vantage': 12.0,
        'default': 0.5
    }

    def __init__(self, config_path: str = None):
        """
        Initialize rate limiter.

        Args:
            config_path: Path to data sources config JSON
        """
        self.buckets: Dict[str, TokenBucket] = {}
        self.last_request: Dict[str, float] = {}
        self.config = self._load_config(config_path)
        self._lock = threading.Lock()

    def _load_config(self, config_path: str = None) -> dict:
        """Load configuration from JSON file."""
        from pathlib import Path

        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)

        # Try default config location
        default_path = Path(__file__).parent.parent / 'config' / 'data_sources.json'
        if default_path.exists():
            with open(default_path, 'r', encoding='utf-8') as f:
                return json.load(f)

        return {}

    def _get_bucket(self, source: str) -> TokenBucket:
        """Get or create token bucket for source."""
        if source not in self.buckets:
            with self._lock:
                if source not in self.buckets:
                    # Get limits from config or defaults
                    source_config = (
                        self.config.get('free_sources', {}).get(source, {}) or
                        self.config.get('paid_sources', {}).get(source, {}) or
                        {}
                    )

                    rate = source_config.get('rate_limit',
                                            self.DEFAULT_LIMITS.get(source,
                                            self.DEFAULT_LIMITS['default'])['rate'])

                    period_str = source_config.get('rate_limit_period', 'minute')
                    period_map = {'second': 1, 'minute': 60, 'hour': 3600}
                    period = period_map.get(period_str, 60)

                    self.buckets[source] = TokenBucket(rate=rate, period=period)

        return self.buckets[source]

    def _get_min_delay(self, source: str) -> float:
        """Get minimum delay between requests for source."""
        source_config = (
            self.config.get('free_sources', {}).get(source, {}) or
            self.config.get('paid_sources', {}).get(source, {}) or
            {}
        )
        return source_config.get('delay_between_requests',
                                self.MIN_DELAYS.get(source,
                                self.MIN_DELAYS['default']))

    def acquire(self, source: str, blocking: bool = True,
                timeout: float = None) -> bool:
        """
        Acquire permission to make a request.

        Args:
            source: Data source name
            blocking: If True, wait until allowed
            timeout: Maximum wait time

        Returns:
            True if request is allowed

        Raises:
            RateLimitExceeded: If non-blocking and rate limit exceeded
        """
        bucket = self._get_bucket(source)
        min_delay = self._get_min_delay(source)

        # Check minimum delay
        last = self.last_request.get(source, 0)
        elapsed = time.time() - last
        if elapsed < min_delay:
            if blocking:
                time.sleep(min_delay - elapsed)
            else:
                wait_time = min_delay - elapsed
                raise RateLimitExceeded(source, wait_time)

        # Acquire from bucket
        if not bucket.acquire(blocking=blocking, timeout=timeout):
            wait_time = bucket.wait_time()
            raise RateLimitExceeded(source, wait_time)

        self.last_request[source] = time.time()
        return True

    def wait_time(self, source: str) -> float:
        """
        Get wait time before next request is allowed.

        Args:
            source: Data source name

        Returns:
            Seconds to wait (0 if ready now)
        """
        bucket = self._get_bucket(source)
        bucket_wait = bucket.wait_time()

        min_delay = self._get_min_delay(source)
        last = self.last_request.get(source, 0)
        delay_wait = max(0, min_delay - (time.time() - last))

        return max(bucket_wait, delay_wait)

    def get_stats(self) -> dict:
        """Get rate limiter statistics."""
        stats = {}
        for source, bucket in self.buckets.items():
            stats[source] = {
                'tokens_available': round(bucket.tokens, 1),
                'capacity': bucket.burst,
                'rate': f"{bucket.rate}/{bucket.period}s",
                'wait_time': round(self.wait_time(source), 2)
            }
        return stats


def with_rate_limit(limiter: RateLimiter, source: str,
                    max_retries: int = 3, base_delay: float = 1.0):
    """
    Decorator for rate-limited functions with exponential backoff.

    Args:
        limiter: RateLimiter instance
        source: Data source name
        max_retries: Maximum retry attempts
        base_delay: Base delay for exponential backoff

    Usage:
        @with_rate_limit(limiter, 'yahoo_finance')
        def fetch_data(symbol):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    # Acquire rate limit permission
                    limiter.acquire(source)

                    # Call the function
                    return func(*args, **kwargs)

                except RateLimitExceeded as e:
                    last_exception = e
                    if attempt < max_retries:
                        wait = e.wait_time + (base_delay * (2 ** attempt))
                        print(f"Rate limited for {source}, waiting {wait:.1f}s "
                              f"(attempt {attempt + 1}/{max_retries + 1})",
                              file=sys.stderr)
                        time.sleep(wait)

                except Exception as e:
                    # For other exceptions, use exponential backoff
                    last_exception = e
                    if attempt < max_retries:
                        wait = base_delay * (2 ** attempt)
                        print(f"Request failed for {source}: {e}, "
                              f"retrying in {wait:.1f}s "
                              f"(attempt {attempt + 1}/{max_retries + 1})",
                              file=sys.stderr)
                        time.sleep(wait)

            # All retries exhausted
            raise last_exception

        return wrapper
    return decorator


def exponential_backoff_retry(max_attempts: int = 3,
                              base_delay: float = 1.0,
                              max_delay: float = 60.0,
                              exceptions: tuple = (Exception,)):
    """
    Decorator for exponential backoff retry.

    Args:
        max_attempts: Maximum retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exceptions: Tuple of exceptions to catch
    """
    if TENACITY_AVAILABLE:
        def decorator(func):
            return retry(
                stop=stop_after_attempt(max_attempts),
                wait=wait_exponential(multiplier=base_delay, max=max_delay),
                retry=retry_if_exception_type(exceptions)
            )(func)
        return decorator
    else:
        # Fallback implementation
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None

                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        if attempt < max_attempts - 1:
                            delay = min(base_delay * (2 ** attempt), max_delay)
                            time.sleep(delay)

                raise last_exception
            return wrapper
        return decorator


# Global rate limiter instance
_limiter_instance: Optional[RateLimiter] = None


def get_limiter() -> RateLimiter:
    """Get or create global rate limiter instance."""
    global _limiter_instance
    if _limiter_instance is None:
        _limiter_instance = RateLimiter()
    return _limiter_instance


def main():
    parser = argparse.ArgumentParser(description="Market Analysis Rate Limiter")
    parser.add_argument("action", choices=["stats", "wait"],
                       help="Action to perform")
    parser.add_argument("--source", default="all",
                       help="Data source name")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format")

    args = parser.parse_args()

    limiter = get_limiter()

    if args.action == "stats":
        stats = limiter.get_stats()
        if args.output == "json":
            print(json.dumps(stats, indent=2))
        else:
            print("\n=== Rate Limiter Statistics ===\n")
            if not stats:
                print("No active rate limiters")
            else:
                for source, info in stats.items():
                    print(f"{source}:")
                    print(f"  Tokens available: {info['tokens_available']}")
                    print(f"  Capacity: {info['capacity']}")
                    print(f"  Rate: {info['rate']}")
                    print(f"  Wait time: {info['wait_time']}s")
                    print()

    elif args.action == "wait":
        if args.source == "all":
            sources = list(limiter.DEFAULT_LIMITS.keys())
        else:
            sources = [args.source]

        for source in sources:
            wait = limiter.wait_time(source)
            print(f"{source}: {wait:.2f}s")


if __name__ == "__main__":
    main()
