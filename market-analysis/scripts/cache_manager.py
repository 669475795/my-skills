#!/usr/bin/env python3
"""
Cache Manager for Market Analysis
Provides memory cache (LRU) and file-based caching with TTL support.
"""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional, Dict
from functools import wraps

try:
    from cachetools import TTLCache, LRUCache
except ImportError:
    TTLCache = None
    LRUCache = None


class CacheManager:
    """
    Unified cache manager supporting both memory and file-based caching.

    Features:
    - In-memory LRU cache with TTL
    - File-based cache for persistence
    - Configurable TTL per data type
    - Thread-safe operations
    - Automatic cache cleanup
    """

    # Default TTL values in seconds
    DEFAULT_TTL = {
        'realtime_quote': 60,           # 1 minute
        'daily_ohlcv': 3600,            # 1 hour
        'historical_data': 86400,        # 24 hours
        'fundamental_data': 86400,       # 24 hours
        'news': 900,                     # 15 minutes
        'ipo_calendar': 3600,            # 1 hour
        'macro_data': 86400,             # 24 hours
        'options_chain': 300,            # 5 minutes
        'bond_yields': 3600,             # 1 hour
        'default': 3600                  # 1 hour default
    }

    def __init__(self, cache_dir: str = None, memory_max_size: int = 1000,
                 memory_ttl: int = 300, config_path: str = None):
        """
        Initialize cache manager.

        Args:
            cache_dir: Directory for file cache
            memory_max_size: Maximum items in memory cache
            memory_ttl: Default TTL for memory cache in seconds
            config_path: Path to cache config JSON
        """
        # Load config if provided
        self.config = self._load_config(config_path)

        # Set cache directory
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path(self.config.get('cache_directory', '.cache/market-analysis'))

        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Initialize memory cache
        self.memory_enabled = True
        self.memory_max_size = memory_max_size
        self.memory_ttl = memory_ttl

        if TTLCache:
            self._memory_cache = TTLCache(maxsize=memory_max_size, ttl=memory_ttl)
        else:
            # Fallback to simple dict with manual TTL check
            self._memory_cache = {}
            self._memory_timestamps = {}

        # TTL configuration
        self.ttl_config = {**self.DEFAULT_TTL, **self.config.get('ttl_by_data_type', {})}

        # Statistics
        self.stats = {
            'memory_hits': 0,
            'memory_misses': 0,
            'file_hits': 0,
            'file_misses': 0,
            'writes': 0
        }

    def _load_config(self, config_path: str = None) -> dict:
        """Load cache configuration from JSON file."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)

        # Try default config location
        default_path = Path(__file__).parent.parent / 'config' / 'cache_config.json'
        if default_path.exists():
            with open(default_path, 'r', encoding='utf-8') as f:
                return json.load(f)

        return {}

    def _generate_key(self, source: str, data_type: str, symbol: str,
                      params: dict = None) -> str:
        """
        Generate a unique cache key.

        Args:
            source: Data source name (e.g., 'yahoo', 'eastmoney')
            data_type: Type of data (e.g., 'quote', 'historical')
            symbol: Asset symbol
            params: Additional parameters

        Returns:
            Unique cache key string
        """
        key_parts = [source, data_type, symbol]

        if params:
            # Sort params for consistent hashing
            params_str = json.dumps(params, sort_keys=True)
            params_hash = hashlib.md5(params_str.encode()).hexdigest()[:8]
            key_parts.append(params_hash)

        return '_'.join(key_parts)

    def _get_ttl(self, data_type: str) -> int:
        """Get TTL for specific data type."""
        return self.ttl_config.get(data_type, self.ttl_config['default'])

    def _get_file_path(self, key: str) -> Path:
        """Get file path for cache key."""
        # Use subdirectories based on first part of key (source)
        parts = key.split('_')
        if len(parts) >= 2:
            subdir = self.cache_dir / parts[0]
            subdir.mkdir(exist_ok=True)
            return subdir / f"{key}.json"
        return self.cache_dir / f"{key}.json"

    def get(self, key: str, data_type: str = 'default') -> Optional[Any]:
        """
        Get value from cache (memory first, then file).

        Args:
            key: Cache key
            data_type: Data type for TTL lookup

        Returns:
            Cached value or None if not found/expired
        """
        # Try memory cache first
        value = self._get_from_memory(key)
        if value is not None:
            self.stats['memory_hits'] += 1
            return value
        self.stats['memory_misses'] += 1

        # Try file cache
        value = self._get_from_file(key, data_type)
        if value is not None:
            self.stats['file_hits'] += 1
            # Populate memory cache
            self._set_to_memory(key, value)
            return value
        self.stats['file_misses'] += 1

        return None

    def set(self, key: str, value: Any, data_type: str = 'default') -> None:
        """
        Set value in both memory and file cache.

        Args:
            key: Cache key
            value: Value to cache
            data_type: Data type for TTL
        """
        # Set in memory cache
        self._set_to_memory(key, value)

        # Set in file cache
        self._set_to_file(key, value, data_type)

        self.stats['writes'] += 1

    def _get_from_memory(self, key: str) -> Optional[Any]:
        """Get value from memory cache."""
        if TTLCache:
            return self._memory_cache.get(key)
        else:
            # Manual TTL check for fallback
            if key in self._memory_cache:
                timestamp = self._memory_timestamps.get(key, 0)
                if time.time() - timestamp < self.memory_ttl:
                    return self._memory_cache[key]
                else:
                    # Expired, remove it
                    del self._memory_cache[key]
                    del self._memory_timestamps[key]
        return None

    def _set_to_memory(self, key: str, value: Any) -> None:
        """Set value in memory cache."""
        if TTLCache:
            self._memory_cache[key] = value
        else:
            self._memory_cache[key] = value
            self._memory_timestamps[key] = time.time()
            # Simple LRU: remove oldest if over limit
            if len(self._memory_cache) > self.memory_max_size:
                oldest_key = min(self._memory_timestamps,
                                key=self._memory_timestamps.get)
                del self._memory_cache[oldest_key]
                del self._memory_timestamps[oldest_key]

    def _get_from_file(self, key: str, data_type: str) -> Optional[Any]:
        """Get value from file cache."""
        file_path = self._get_file_path(key)

        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                cached = json.load(f)

            # Check TTL
            cached_time = cached.get('_cached_at', 0)
            ttl = self._get_ttl(data_type)

            if time.time() - cached_time > ttl:
                # Expired, remove file
                file_path.unlink(missing_ok=True)
                return None

            return cached.get('data')
        except (json.JSONDecodeError, IOError):
            return None

    def _set_to_file(self, key: str, value: Any, data_type: str) -> None:
        """Set value in file cache."""
        file_path = self._get_file_path(key)

        cached = {
            '_cached_at': time.time(),
            '_data_type': data_type,
            '_ttl': self._get_ttl(data_type),
            'data': value
        }

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(cached, f, default=str, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Failed to write cache file: {e}", file=sys.stderr)

    def delete(self, key: str) -> None:
        """Delete entry from both caches."""
        # Remove from memory
        if TTLCache:
            self._memory_cache.pop(key, None)
        else:
            self._memory_cache.pop(key, None)
            self._memory_timestamps.pop(key, None)

        # Remove from file
        file_path = self._get_file_path(key)
        file_path.unlink(missing_ok=True)

    def clear(self, source: str = None) -> int:
        """
        Clear cache entries.

        Args:
            source: If provided, only clear entries from this source

        Returns:
            Number of entries cleared
        """
        count = 0

        if source:
            # Clear specific source
            source_dir = self.cache_dir / source
            if source_dir.exists():
                for f in source_dir.glob('*.json'):
                    f.unlink()
                    count += 1

            # Clear from memory
            keys_to_remove = [k for k in self._memory_cache if k.startswith(f"{source}_")]
            for k in keys_to_remove:
                if TTLCache:
                    self._memory_cache.pop(k, None)
                else:
                    self._memory_cache.pop(k, None)
                    self._memory_timestamps.pop(k, None)
                count += 1
        else:
            # Clear all
            for f in self.cache_dir.rglob('*.json'):
                f.unlink()
                count += 1

            if TTLCache:
                self._memory_cache.clear()
            else:
                self._memory_cache.clear()
                self._memory_timestamps.clear()

        return count

    def cleanup_expired(self) -> int:
        """
        Remove expired entries from file cache.

        Returns:
            Number of entries removed
        """
        count = 0
        current_time = time.time()

        for cache_file in self.cache_dir.rglob('*.json'):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached = json.load(f)

                cached_time = cached.get('_cached_at', 0)
                ttl = cached.get('_ttl', self.ttl_config['default'])

                if current_time - cached_time > ttl:
                    cache_file.unlink()
                    count += 1
            except (json.JSONDecodeError, IOError):
                # Remove corrupted files
                cache_file.unlink(missing_ok=True)
                count += 1

        return count

    def get_stats(self) -> dict:
        """Get cache statistics."""
        memory_size = len(self._memory_cache)
        file_count = sum(1 for _ in self.cache_dir.rglob('*.json'))

        total_hits = self.stats['memory_hits'] + self.stats['file_hits']
        total_requests = total_hits + self.stats['memory_misses']
        hit_rate = (total_hits / total_requests * 100) if total_requests > 0 else 0

        return {
            **self.stats,
            'memory_size': memory_size,
            'file_count': file_count,
            'hit_rate': f"{hit_rate:.1f}%"
        }


def cached(cache_manager: CacheManager, data_type: str = 'default',
           key_func=None):
    """
    Decorator for caching function results.

    Args:
        cache_manager: CacheManager instance
        data_type: Data type for TTL
        key_func: Optional function to generate cache key from args

    Usage:
        @cached(cache, 'quote', key_func=lambda s, **kw: f"yahoo_quote_{s}")
        def get_quote(symbol, **kwargs):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                key = key_func(*args, **kwargs)
            else:
                key = f"{func.__name__}_{args}_{kwargs}"

            # Try to get from cache
            result = cache_manager.get(key, data_type)
            if result is not None:
                return result

            # Call function and cache result
            result = func(*args, **kwargs)
            if result is not None:
                cache_manager.set(key, result, data_type)

            return result
        return wrapper
    return decorator


# Global cache instance
_cache_instance: Optional[CacheManager] = None


def get_cache() -> CacheManager:
    """Get or create global cache instance."""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = CacheManager()
    return _cache_instance


def main():
    parser = argparse.ArgumentParser(description="Market Analysis Cache Manager")
    parser.add_argument("action", choices=["stats", "cleanup", "clear"],
                       help="Action to perform")
    parser.add_argument("--source", help="Source to clear (for clear action)")
    parser.add_argument("--cache-dir", help="Cache directory path")
    parser.add_argument("--output", choices=["json", "text"], default="text",
                       help="Output format")

    args = parser.parse_args()

    cache = CacheManager(cache_dir=args.cache_dir)

    if args.action == "stats":
        stats = cache.get_stats()
        if args.output == "json":
            print(json.dumps(stats, indent=2))
        else:
            print("\n=== Cache Statistics ===\n")
            print(f"Memory Hits: {stats['memory_hits']}")
            print(f"Memory Misses: {stats['memory_misses']}")
            print(f"File Hits: {stats['file_hits']}")
            print(f"File Misses: {stats['file_misses']}")
            print(f"Total Writes: {stats['writes']}")
            print(f"Memory Size: {stats['memory_size']} items")
            print(f"File Count: {stats['file_count']} files")
            print(f"Hit Rate: {stats['hit_rate']}")

    elif args.action == "cleanup":
        count = cache.cleanup_expired()
        print(f"Removed {count} expired cache entries")

    elif args.action == "clear":
        count = cache.clear(source=args.source)
        if args.source:
            print(f"Cleared {count} cache entries for source: {args.source}")
        else:
            print(f"Cleared all {count} cache entries")


if __name__ == "__main__":
    main()
