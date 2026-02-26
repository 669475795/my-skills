#!/usr/bin/env python3
"""
Cyclomatic Complexity Checker

This script analyzes Java and Python files for cyclomatic complexity.
It can be used standalone or as part of CI/CD pipelines.

Requirements:
    pip install radon lizard PyYAML

Usage:
    python check_complexity.py <path> [--config config.yaml]
    python check_complexity.py src/main/java --max-complexity 10
    python check_complexity.py . --format json
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    import yaml
except ImportError:
    yaml = None

try:
    import lizard
    LIZARD_AVAILABLE = True
except ImportError:
    LIZARD_AVAILABLE = False
    print("Warning: lizard not installed. Install with: pip install lizard", file=sys.stderr)

try:
    from radon.complexity import cc_visit
    from radon.raw import analyze
    RADON_AVAILABLE = True
except ImportError:
    RADON_AVAILABLE = False
    print("Warning: radon not installed. Install with: pip install radon", file=sys.stderr)


class ComplexityChecker:
    """Main class for checking code complexity."""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize with configuration."""
        self.config = config or self.default_config()
        self.results = []
        self.violations = []

    @staticmethod
    def default_config() -> Dict:
        """Return default configuration."""
        return {
            'thresholds': {
                'method': 10,
                'class': 50,
                'file': 100
            },
            'languages': {
                'java': {
                    'extensions': ['.java'],
                    'enabled': True
                },
                'python': {
                    'extensions': ['.py'],
                    'enabled': True
                }
            },
            'exclude_patterns': [
                '*/test/*',
                '*/tests/*',
                '*Test.java',
                'test_*.py'
            ]
        }

    def should_exclude(self, filepath: Path) -> bool:
        """Check if file should be excluded."""
        filepath_str = str(filepath).replace('\\', '/')

        for pattern in self.config.get('exclude_patterns', []):
            pattern = pattern.replace('*/', '')
            if pattern.startswith('*') and filepath_str.endswith(pattern[1:]):
                return True
            if pattern.endswith('*') and pattern[:-1] in filepath_str:
                return True
            if pattern in filepath_str:
                return True

        return False

    def check_file(self, filepath: Path) -> Optional[Dict]:
        """Check complexity of a single file."""
        if self.should_exclude(filepath):
            return None

        ext = filepath.suffix

        # Determine language
        language = None
        for lang, lang_config in self.config['languages'].items():
            if ext in lang_config['extensions'] and lang_config['enabled']:
                language = lang
                break

        if not language:
            return None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)
            return None

        if language == 'python' and RADON_AVAILABLE:
            return self._check_python(filepath, content)
        elif LIZARD_AVAILABLE:
            return self._check_with_lizard(filepath, content, language)

        return None

    def _check_python(self, filepath: Path, content: str) -> Dict:
        """Check Python file using radon."""
        result = {
            'file': str(filepath),
            'language': 'python',
            'functions': [],
            'file_complexity': 0,
            'violations': []
        }

        try:
            # Get complexity for each function
            complexity_results = cc_visit(content)

            for item in complexity_results:
                func_info = {
                    'name': item.name,
                    'line': item.lineno,
                    'complexity': item.complexity,
                    'type': item.classname if item.classname else 'function'
                }
                result['functions'].append(func_info)
                result['file_complexity'] += item.complexity

                # Check thresholds
                threshold = self.config['thresholds']['method']
                if item.complexity > threshold:
                    violation = {
                        'file': str(filepath),
                        'function': item.name,
                        'line': item.lineno,
                        'complexity': item.complexity,
                        'threshold': threshold,
                        'message': f"Complexity {item.complexity} exceeds threshold {threshold}"
                    }
                    result['violations'].append(violation)
                    self.violations.append(violation)

            # Check file-level threshold
            file_threshold = self.config['thresholds']['file']
            if result['file_complexity'] > file_threshold:
                violation = {
                    'file': str(filepath),
                    'function': '<file>',
                    'line': 0,
                    'complexity': result['file_complexity'],
                    'threshold': file_threshold,
                    'message': f"File complexity {result['file_complexity']} exceeds threshold {file_threshold}"
                }
                result['violations'].append(violation)
                self.violations.append(violation)

        except Exception as e:
            print(f"Error analyzing {filepath}: {e}", file=sys.stderr)

        return result

    def _check_with_lizard(self, filepath: Path, content: str, language: str) -> Dict:
        """Check file using lizard (works for Java and Python)."""
        result = {
            'file': str(filepath),
            'language': language,
            'functions': [],
            'file_complexity': 0,
            'violations': []
        }

        try:
            analyzed = lizard.analyze_file.analyze_source_code(str(filepath), content)

            for func in analyzed.function_list:
                func_info = {
                    'name': func.name,
                    'line': func.start_line,
                    'complexity': func.cyclomatic_complexity,
                    'type': 'function'
                }
                result['functions'].append(func_info)
                result['file_complexity'] += func.cyclomatic_complexity

                # Check thresholds
                threshold = self.config['thresholds']['method']
                if func.cyclomatic_complexity > threshold:
                    violation = {
                        'file': str(filepath),
                        'function': func.name,
                        'line': func.start_line,
                        'complexity': func.cyclomatic_complexity,
                        'threshold': threshold,
                        'message': f"Complexity {func.cyclomatic_complexity} exceeds threshold {threshold}"
                    }
                    result['violations'].append(violation)
                    self.violations.append(violation)

            # Check file-level threshold
            file_threshold = self.config['thresholds']['file']
            if result['file_complexity'] > file_threshold:
                violation = {
                    'file': str(filepath),
                    'function': '<file>',
                    'line': 0,
                    'complexity': result['file_complexity'],
                    'threshold': file_threshold,
                    'message': f"File complexity {result['file_complexity']} exceeds threshold {file_threshold}"
                }
                result['violations'].append(violation)
                self.violations.append(violation)

        except Exception as e:
            print(f"Error analyzing {filepath}: {e}", file=sys.stderr)

        return result

    def check_directory(self, directory: Path) -> List[Dict]:
        """Recursively check all files in directory."""
        for item in directory.rglob('*'):
            if item.is_file():
                result = self.check_file(item)
                if result:
                    self.results.append(result)

        return self.results

    def format_results(self, format_type: str = 'text') -> str:
        """Format results for output."""
        if format_type == 'json':
            return json.dumps({
                'summary': {
                    'total_files': len(self.results),
                    'total_violations': len(self.violations),
                    'thresholds': self.config['thresholds']
                },
                'results': self.results
            }, indent=2)

        # Text format
        output = []
        output.append("=" * 80)
        output.append("Cyclomatic Complexity Report")
        output.append("=" * 80)
        output.append(f"Total files analyzed: {len(self.results)}")
        output.append(f"Total violations: {len(self.violations)}")
        output.append(f"Thresholds: Method={self.config['thresholds']['method']}, "
                     f"File={self.config['thresholds']['file']}")
        output.append("")

        if self.violations:
            output.append("Violations:")
            output.append("-" * 80)

            for v in self.violations:
                output.append(f"{v['file']}:{v['line']}")
                output.append(f"  Function: {v['function']}")
                output.append(f"  Complexity: {v['complexity']} (threshold: {v['threshold']})")
                output.append(f"  {v['message']}")
                output.append("")

        else:
            output.append("No violations found! ✓")

        return '\n'.join(output)


def load_config(config_path: Optional[Path]) -> Dict:
    """Load configuration from file."""
    if not config_path or not config_path.exists():
        return ComplexityChecker.default_config()

    if not yaml:
        print("Warning: PyYAML not installed, using default config", file=sys.stderr)
        return ComplexityChecker.default_config()

    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}, using default", file=sys.stderr)
        return ComplexityChecker.default_config()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Check cyclomatic complexity of Java and Python code'
    )
    parser.add_argument('path', help='File or directory to analyze')
    parser.add_argument('--config', type=Path, help='Configuration file (YAML)')
    parser.add_argument('--max-complexity', type=int, help='Maximum allowed complexity for methods')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='Output format')
    parser.add_argument('--fail-on-violation', action='store_true',
                       help='Exit with error code if violations found')

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Override with command-line arguments
    if args.max_complexity:
        config['thresholds']['method'] = args.max_complexity

    # Check if required tools are available
    if not LIZARD_AVAILABLE and not RADON_AVAILABLE:
        print("Error: Neither lizard nor radon is installed.", file=sys.stderr)
        print("Install with: pip install lizard radon", file=sys.stderr)
        sys.exit(1)

    # Run checker
    checker = ComplexityChecker(config)
    path = Path(args.path)

    if path.is_file():
        result = checker.check_file(path)
        if result:
            checker.results.append(result)
    elif path.is_dir():
        checker.check_directory(path)
    else:
        print(f"Error: {path} is not a valid file or directory", file=sys.stderr)
        sys.exit(1)

    # Output results
    print(checker.format_results(args.format))

    # Exit with error if violations found and flag is set
    if args.fail_on_violation and checker.violations:
        sys.exit(1)


if __name__ == '__main__':
    main()
