#!/usr/bin/env python3
"""
Paper Trading System for Market Analysis
Simulates trading with risk controls and performance tracking.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
import uuid

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
    from broker_interface import (
        BrokerFactory, Order, OrderSide, OrderType, OrderStatus,
        Position, AccountInfo
    )
except ImportError:
    BrokerFactory = None


@dataclass
class Trade:
    """Completed trade record"""
    trade_id: str
    symbol: str
    side: str
    quantity: int
    entry_price: float
    exit_price: float = None
    entry_time: str = None
    exit_time: str = None
    pnl: float = 0
    pnl_pct: float = 0
    holding_period: int = 0
    status: str = 'open'

    def to_dict(self) -> dict:
        return {
            'trade_id': self.trade_id,
            'symbol': self.symbol,
            'side': self.side,
            'quantity': self.quantity,
            'entry_price': self.entry_price,
            'exit_price': self.exit_price,
            'entry_time': self.entry_time,
            'exit_time': self.exit_time,
            'pnl': round(self.pnl, 2),
            'pnl_pct': round(self.pnl_pct, 2),
            'holding_period': self.holding_period,
            'status': self.status
        }


@dataclass
class RiskParameters:
    """Risk management parameters"""
    max_position_size: float = 0.1  # Max 10% per position
    max_portfolio_risk: float = 0.02  # Max 2% total risk
    max_drawdown: float = 0.15  # Stop trading at 15% drawdown
    daily_loss_limit: float = 0.03  # Max 3% daily loss
    max_open_positions: int = 10
    stop_loss_pct: float = 0.05  # Default 5% stop loss
    take_profit_pct: float = 0.10  # Default 10% take profit

    def to_dict(self) -> dict:
        return {
            'max_position_size': f"{self.max_position_size * 100}%",
            'max_portfolio_risk': f"{self.max_portfolio_risk * 100}%",
            'max_drawdown': f"{self.max_drawdown * 100}%",
            'daily_loss_limit': f"{self.daily_loss_limit * 100}%",
            'max_open_positions': self.max_open_positions,
            'stop_loss_pct': f"{self.stop_loss_pct * 100}%",
            'take_profit_pct': f"{self.take_profit_pct * 100}%"
        }


class PaperTradingSystem:
    """
    Paper Trading System

    Features:
    - Simulated order execution
    - Risk management controls
    - Performance tracking
    - Trade journaling
    """

    def __init__(self, initial_capital: float = 100000,
                 risk_params: RiskParameters = None,
                 data_dir: str = None):
        self.initial_capital = initial_capital
        self.risk_params = risk_params or RiskParameters()
        self.data_dir = Path(data_dir) if data_dir else Path.cwd() / 'paper_trading'
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Initialize broker
        if BrokerFactory:
            self.broker = BrokerFactory.create('simulated', {'initial_cash': initial_capital})
            self.broker.connect()
        else:
            self.broker = None

        # Trade history
        self.trades: List[Trade] = []
        self.daily_pnl: Dict[str, float] = {}
        self.equity_curve: List[Dict] = []

        # State
        self.high_water_mark = initial_capital
        self.trading_enabled = True

    def check_risk_limits(self, symbol: str, quantity: int, side: str) -> Dict:
        """
        检查风险限制

        Args:
            symbol: 交易标的
            quantity: 交易数量
            side: 买/卖方向

        Returns:
            风险检查结果
        """
        account = self.broker.get_account_info()
        positions = self.broker.get_positions()
        quote = self.broker.get_quote(symbol)

        checks = {
            'passed': True,
            'warnings': [],
            'errors': []
        }

        # 1. Check position size
        position_value = quantity * quote['last']
        position_pct = position_value / account.total_value

        if position_pct > self.risk_params.max_position_size:
            checks['passed'] = False
            checks['errors'].append(
                f"Position size {position_pct*100:.1f}% exceeds limit {self.risk_params.max_position_size*100}%"
            )

        # 2. Check number of positions
        if side == 'buy' and len(positions) >= self.risk_params.max_open_positions:
            checks['passed'] = False
            checks['errors'].append(
                f"Max open positions ({self.risk_params.max_open_positions}) reached"
            )

        # 3. Check daily loss limit
        today = datetime.now().strftime('%Y-%m-%d')
        daily_loss = self.daily_pnl.get(today, 0)
        daily_loss_pct = abs(daily_loss) / self.initial_capital

        if daily_loss < 0 and daily_loss_pct >= self.risk_params.daily_loss_limit:
            checks['passed'] = False
            checks['errors'].append(
                f"Daily loss limit {self.risk_params.daily_loss_limit*100}% reached"
            )

        # 4. Check max drawdown
        current_dd = (self.high_water_mark - account.total_value) / self.high_water_mark
        if current_dd >= self.risk_params.max_drawdown:
            checks['passed'] = False
            checks['errors'].append(
                f"Max drawdown {self.risk_params.max_drawdown*100}% reached"
            )

        # 5. Check buying power
        if side == 'buy' and position_value > account.buying_power:
            checks['passed'] = False
            checks['errors'].append(
                f"Insufficient buying power: ${account.buying_power:.2f} < ${position_value:.2f}"
            )

        # Warnings
        if position_pct > self.risk_params.max_position_size * 0.8:
            checks['warnings'].append("Position size approaching limit")

        if len(positions) >= self.risk_params.max_open_positions * 0.8:
            checks['warnings'].append("Approaching max positions limit")

        return checks

    def place_trade(self, symbol: str, quantity: int, side: str,
                    order_type: str = 'market', price: float = None,
                    stop_loss: float = None, take_profit: float = None) -> Dict:
        """
        下单交易

        Args:
            symbol: 交易标的
            quantity: 交易数量
            side: 'buy' 或 'sell'
            order_type: 'market' 或 'limit'
            price: 限价单价格
            stop_loss: 止损价
            take_profit: 止盈价

        Returns:
            交易结果
        """
        if not self.trading_enabled:
            return {'error': 'Trading is disabled due to risk limits'}

        # Check risk limits
        risk_check = self.check_risk_limits(symbol, quantity, side)
        if not risk_check['passed']:
            return {
                'error': 'Risk check failed',
                'details': risk_check['errors']
            }

        # Create and place order
        order = Order(
            order_id='',
            symbol=symbol,
            side=OrderSide.BUY if side == 'buy' else OrderSide.SELL,
            order_type=OrderType.MARKET if order_type == 'market' else OrderType.LIMIT,
            quantity=quantity,
            price=price
        )

        result = self.broker.place_order(order)

        if result.status == OrderStatus.FILLED:
            # Record trade
            trade = Trade(
                trade_id=str(uuid.uuid4())[:8],
                symbol=symbol,
                side=side,
                quantity=quantity,
                entry_price=result.filled_price,
                entry_time=datetime.now().isoformat()
            )
            self.trades.append(trade)

            # Update equity curve
            self._update_equity_curve()

            return {
                'status': 'filled',
                'trade': trade.to_dict(),
                'order': result.to_dict(),
                'warnings': risk_check['warnings']
            }
        else:
            return {
                'status': result.status.value,
                'order': result.to_dict()
            }

    def close_trade(self, trade_id: str, exit_price: float = None) -> Dict:
        """
        平仓交易

        Args:
            trade_id: 交易ID
            exit_price: 平仓价格（None则使用市价）

        Returns:
            平仓结果
        """
        # Find trade
        trade = next((t for t in self.trades if t.trade_id == trade_id and t.status == 'open'), None)
        if not trade:
            return {'error': f'Open trade not found: {trade_id}'}

        # Get current price if not specified
        if exit_price is None:
            quote = self.broker.get_quote(trade.symbol)
            exit_price = quote['bid'] if trade.side == 'buy' else quote['ask']

        # Place closing order
        close_side = 'sell' if trade.side == 'buy' else 'buy'
        order = Order(
            order_id='',
            symbol=trade.symbol,
            side=OrderSide.SELL if close_side == 'sell' else OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=trade.quantity
        )

        result = self.broker.place_order(order)

        if result.status == OrderStatus.FILLED:
            # Update trade
            trade.exit_price = result.filled_price
            trade.exit_time = datetime.now().isoformat()
            trade.status = 'closed'

            # Calculate P&L
            if trade.side == 'buy':
                trade.pnl = (trade.exit_price - trade.entry_price) * trade.quantity
            else:
                trade.pnl = (trade.entry_price - trade.exit_price) * trade.quantity

            trade.pnl_pct = trade.pnl / (trade.entry_price * trade.quantity) * 100

            # Calculate holding period
            entry = datetime.fromisoformat(trade.entry_time)
            exit_time = datetime.fromisoformat(trade.exit_time)
            trade.holding_period = (exit_time - entry).days

            # Update daily P&L
            today = datetime.now().strftime('%Y-%m-%d')
            self.daily_pnl[today] = self.daily_pnl.get(today, 0) + trade.pnl

            # Update equity curve
            self._update_equity_curve()

            return {
                'status': 'closed',
                'trade': trade.to_dict()
            }
        else:
            return {
                'status': 'failed',
                'error': f'Close order status: {result.status.value}'
            }

    def _update_equity_curve(self):
        """Update equity curve"""
        account = self.broker.get_account_info()
        self.equity_curve.append({
            'timestamp': datetime.now().isoformat(),
            'total_value': account.total_value,
            'cash': account.cash
        })

        # Update high water mark
        if account.total_value > self.high_water_mark:
            self.high_water_mark = account.total_value

    def get_performance(self) -> Dict:
        """
        获取绩效统计

        Returns:
            绩效数据
        """
        account = self.broker.get_account_info()

        closed_trades = [t for t in self.trades if t.status == 'closed']
        open_trades = [t for t in self.trades if t.status == 'open']

        if not closed_trades:
            return {
                'total_trades': 0,
                'open_trades': len(open_trades),
                'total_value': account.total_value,
                'note': 'No closed trades yet'
            }

        # Calculate metrics
        winning_trades = [t for t in closed_trades if t.pnl > 0]
        losing_trades = [t for t in closed_trades if t.pnl < 0]

        total_pnl = sum(t.pnl for t in closed_trades)
        total_return = (account.total_value / self.initial_capital - 1) * 100

        win_rate = len(winning_trades) / len(closed_trades) * 100 if closed_trades else 0

        avg_win = np.mean([t.pnl for t in winning_trades]) if winning_trades else 0
        avg_loss = np.mean([t.pnl for t in losing_trades]) if losing_trades else 0

        profit_factor = abs(sum(t.pnl for t in winning_trades) / sum(t.pnl for t in losing_trades)) if losing_trades and sum(t.pnl for t in losing_trades) != 0 else float('inf')

        # Drawdown
        current_dd = (self.high_water_mark - account.total_value) / self.high_water_mark * 100

        return {
            'initial_capital': self.initial_capital,
            'current_value': round(account.total_value, 2),
            'total_return': round(total_return, 2),
            'total_pnl': round(total_pnl, 2),
            'total_trades': len(closed_trades),
            'open_trades': len(open_trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': round(win_rate, 2),
            'avg_win': round(avg_win, 2),
            'avg_loss': round(avg_loss, 2),
            'profit_factor': round(profit_factor, 2) if profit_factor != float('inf') else 'Inf',
            'current_drawdown': round(current_dd, 2),
            'high_water_mark': round(self.high_water_mark, 2)
        }

    def get_open_positions(self) -> List[Dict]:
        """获取当前持仓"""
        positions = self.broker.get_positions()
        return [p.to_dict() for p in positions]

    def get_trade_history(self, limit: int = 50) -> List[Dict]:
        """获取交易历史"""
        return [t.to_dict() for t in self.trades[-limit:]]

    def export_trades(self, filename: str = None) -> str:
        """导出交易记录到CSV"""
        if not filename:
            filename = f"trades_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        filepath = self.data_dir / filename

        df = pd.DataFrame([t.to_dict() for t in self.trades])
        df.to_csv(filepath, index=False)

        return str(filepath)


def main():
    parser = argparse.ArgumentParser(description="Paper Trading System")
    parser.add_argument("action", choices=["buy", "sell", "close", "positions", "history", "performance", "risk-params", "export"],
                       help="Action to perform")
    parser.add_argument("--symbol", help="Trading symbol")
    parser.add_argument("--quantity", type=int, help="Trade quantity")
    parser.add_argument("--price", type=float, help="Limit price")
    parser.add_argument("--order-type", default="market", choices=["market", "limit"])
    parser.add_argument("--trade-id", help="Trade ID for close action")
    parser.add_argument("--initial-capital", type=float, default=100000)
    parser.add_argument("--output", choices=["json", "text"], default="text")

    args = parser.parse_args()

    system = PaperTradingSystem(initial_capital=args.initial_capital)

    if args.action in ["buy", "sell"]:
        if not args.symbol or not args.quantity:
            print("Error: --symbol and --quantity required")
            sys.exit(1)
        data = system.place_trade(args.symbol, args.quantity, args.action,
                                  args.order_type, args.price)

    elif args.action == "close":
        if not args.trade_id:
            print("Error: --trade-id required")
            sys.exit(1)
        data = system.close_trade(args.trade_id)

    elif args.action == "positions":
        data = {'positions': system.get_open_positions()}

    elif args.action == "history":
        data = {'trades': system.get_trade_history()}

    elif args.action == "performance":
        data = system.get_performance()

    elif args.action == "risk-params":
        data = system.risk_params.to_dict()

    elif args.action == "export":
        filepath = system.export_trades()
        data = {'exported_to': filepath}

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2, default=str))
    else:
        print(f"\n=== Paper Trading: {args.action.title()} ===\n")
        for k, v in data.items():
            if isinstance(v, list):
                print(f"\n{k}:")
                for item in v[:10]:
                    print(f"  {item}")
            else:
                print(f"{k}: {v}")


if __name__ == "__main__":
    main()
