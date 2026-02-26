#!/usr/bin/env python3
"""
Broker Interface for Market Analysis
Abstract interface for broker integration (Futu, Tiger, Interactive Brokers).
"""

import argparse
import json
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderStatus(Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    PARTIAL = "partial"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


@dataclass
class Order:
    """Order data class"""
    order_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: int
    price: Optional[float] = None
    stop_price: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: int = 0
    filled_price: Optional[float] = None
    created_at: str = None
    updated_at: str = None

    def to_dict(self) -> dict:
        return {
            'order_id': self.order_id,
            'symbol': self.symbol,
            'side': self.side.value,
            'order_type': self.order_type.value,
            'quantity': self.quantity,
            'price': self.price,
            'stop_price': self.stop_price,
            'status': self.status.value,
            'filled_quantity': self.filled_quantity,
            'filled_price': self.filled_price,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


@dataclass
class Position:
    """Position data class"""
    symbol: str
    quantity: int
    avg_cost: float
    market_value: float
    unrealized_pnl: float
    unrealized_pnl_pct: float

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AccountInfo:
    """Account information"""
    account_id: str
    currency: str
    cash: float
    buying_power: float
    total_value: float
    margin_used: float = 0
    margin_available: float = 0

    def to_dict(self) -> dict:
        return asdict(self)


class BrokerInterface(ABC):
    """
    Abstract broker interface.

    Subclasses should implement specific broker APIs:
    - FutuBroker: Futu OpenD API
    - TigerBroker: Tiger Trade API
    - IBBroker: Interactive Brokers TWS/Gateway API
    """

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.connected = False

    @abstractmethod
    def connect(self) -> bool:
        """Connect to broker"""
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from broker"""
        pass

    @abstractmethod
    def get_account_info(self) -> AccountInfo:
        """Get account information"""
        pass

    @abstractmethod
    def get_positions(self) -> List[Position]:
        """Get current positions"""
        pass

    @abstractmethod
    def get_orders(self, status: OrderStatus = None) -> List[Order]:
        """Get orders"""
        pass

    @abstractmethod
    def place_order(self, order: Order) -> Order:
        """Place an order"""
        pass

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        pass

    @abstractmethod
    def modify_order(self, order_id: str, price: float = None,
                     quantity: int = None) -> Order:
        """Modify an order"""
        pass

    @abstractmethod
    def get_quote(self, symbol: str) -> Dict:
        """Get real-time quote"""
        pass


class SimulatedBroker(BrokerInterface):
    """
    Simulated broker for testing and paper trading.
    """

    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.initial_cash = config.get('initial_cash', 100000) if config else 100000
        self.cash = self.initial_cash
        self.positions: Dict[str, Position] = {}
        self.orders: Dict[str, Order] = {}
        self.order_counter = 0

    def connect(self) -> bool:
        self.connected = True
        return True

    def disconnect(self) -> bool:
        self.connected = False
        return True

    def get_account_info(self) -> AccountInfo:
        # Calculate total value
        positions_value = sum(p.market_value for p in self.positions.values())
        total_value = self.cash + positions_value

        return AccountInfo(
            account_id='SIM001',
            currency='USD',
            cash=self.cash,
            buying_power=self.cash,
            total_value=total_value
        )

    def get_positions(self) -> List[Position]:
        return list(self.positions.values())

    def get_orders(self, status: OrderStatus = None) -> List[Order]:
        orders = list(self.orders.values())
        if status:
            orders = [o for o in orders if o.status == status]
        return orders

    def place_order(self, order: Order) -> Order:
        self.order_counter += 1
        order.order_id = f"SIM{self.order_counter:06d}"
        order.created_at = datetime.now().isoformat()
        order.status = OrderStatus.SUBMITTED

        # Simulate immediate fill for market orders
        if order.order_type == OrderType.MARKET:
            quote = self.get_quote(order.symbol)
            fill_price = quote.get('ask', 100) if order.side == OrderSide.BUY else quote.get('bid', 100)
            order = self._fill_order(order, fill_price)

        self.orders[order.order_id] = order
        return order

    def _fill_order(self, order: Order, fill_price: float) -> Order:
        """Fill an order"""
        order.filled_price = fill_price
        order.filled_quantity = order.quantity
        order.status = OrderStatus.FILLED
        order.updated_at = datetime.now().isoformat()

        # Update position
        symbol = order.symbol
        cost = fill_price * order.quantity

        if order.side == OrderSide.BUY:
            if self.cash < cost:
                order.status = OrderStatus.REJECTED
                return order

            self.cash -= cost

            if symbol in self.positions:
                pos = self.positions[symbol]
                total_cost = pos.avg_cost * pos.quantity + cost
                total_qty = pos.quantity + order.quantity
                pos.avg_cost = total_cost / total_qty
                pos.quantity = total_qty
            else:
                self.positions[symbol] = Position(
                    symbol=symbol,
                    quantity=order.quantity,
                    avg_cost=fill_price,
                    market_value=cost,
                    unrealized_pnl=0,
                    unrealized_pnl_pct=0
                )

        else:  # SELL
            if symbol not in self.positions or self.positions[symbol].quantity < order.quantity:
                order.status = OrderStatus.REJECTED
                return order

            self.cash += cost
            pos = self.positions[symbol]
            pos.quantity -= order.quantity

            if pos.quantity == 0:
                del self.positions[symbol]

        return order

    def cancel_order(self, order_id: str) -> bool:
        if order_id in self.orders:
            order = self.orders[order_id]
            if order.status in [OrderStatus.PENDING, OrderStatus.SUBMITTED]:
                order.status = OrderStatus.CANCELLED
                order.updated_at = datetime.now().isoformat()
                return True
        return False

    def modify_order(self, order_id: str, price: float = None,
                     quantity: int = None) -> Order:
        if order_id not in self.orders:
            raise ValueError(f"Order not found: {order_id}")

        order = self.orders[order_id]
        if order.status not in [OrderStatus.PENDING, OrderStatus.SUBMITTED]:
            raise ValueError(f"Cannot modify order with status: {order.status}")

        if price:
            order.price = price
        if quantity:
            order.quantity = quantity
        order.updated_at = datetime.now().isoformat()

        return order

    def get_quote(self, symbol: str) -> Dict:
        """Get simulated quote"""
        # In production, this would fetch real data
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='1d')
            if not hist.empty:
                price = hist['Close'].iloc[-1]
                return {
                    'symbol': symbol,
                    'bid': round(price * 0.999, 2),
                    'ask': round(price * 1.001, 2),
                    'last': round(price, 2),
                    'volume': int(hist['Volume'].iloc[-1])
                }
        except:
            pass

        # Fallback to simulated data
        import random
        base_price = 100
        return {
            'symbol': symbol,
            'bid': base_price - 0.05,
            'ask': base_price + 0.05,
            'last': base_price,
            'volume': random.randint(10000, 1000000)
        }


class BrokerFactory:
    """Factory for creating broker instances"""

    @staticmethod
    def create(broker_type: str, config: Dict = None) -> BrokerInterface:
        """
        Create broker instance.

        Args:
            broker_type: 'simulated', 'futu', 'tiger', 'ib'
            config: Broker configuration

        Returns:
            BrokerInterface instance
        """
        if broker_type == 'simulated':
            return SimulatedBroker(config)
        elif broker_type == 'futu':
            # Placeholder for Futu implementation
            raise NotImplementedError("Futu broker not implemented. Install futu-api.")
        elif broker_type == 'tiger':
            # Placeholder for Tiger implementation
            raise NotImplementedError("Tiger broker not implemented. Install tigeropen.")
        elif broker_type == 'ib':
            # Placeholder for IB implementation
            raise NotImplementedError("IB broker not implemented. Install ib_insync.")
        else:
            raise ValueError(f"Unknown broker type: {broker_type}")


def main():
    parser = argparse.ArgumentParser(description="Broker Interface")
    parser.add_argument("action", choices=["connect", "account", "positions", "orders", "quote", "buy", "sell", "cancel"],
                       help="Action to perform")
    parser.add_argument("--broker", default="simulated", choices=["simulated", "futu", "tiger", "ib"],
                       help="Broker type")
    parser.add_argument("--symbol", help="Symbol for quote/order")
    parser.add_argument("--quantity", type=int, help="Order quantity")
    parser.add_argument("--price", type=float, help="Limit price")
    parser.add_argument("--order-type", default="market", choices=["market", "limit"],
                       help="Order type")
    parser.add_argument("--order-id", help="Order ID for cancel/modify")
    parser.add_argument("--initial-cash", type=float, default=100000,
                       help="Initial cash for simulated broker")
    parser.add_argument("--output", choices=["json", "text"], default="text")

    args = parser.parse_args()

    # Create broker
    config = {'initial_cash': args.initial_cash}
    broker = BrokerFactory.create(args.broker, config)
    broker.connect()

    if args.action == "connect":
        data = {'status': 'connected', 'broker': args.broker}

    elif args.action == "account":
        account = broker.get_account_info()
        data = account.to_dict()

    elif args.action == "positions":
        positions = broker.get_positions()
        data = {'positions': [p.to_dict() for p in positions]}

    elif args.action == "orders":
        orders = broker.get_orders()
        data = {'orders': [o.to_dict() for o in orders]}

    elif args.action == "quote":
        if not args.symbol:
            print("Error: --symbol required")
            sys.exit(1)
        data = broker.get_quote(args.symbol)

    elif args.action in ["buy", "sell"]:
        if not args.symbol or not args.quantity:
            print("Error: --symbol and --quantity required")
            sys.exit(1)

        order = Order(
            order_id='',
            symbol=args.symbol,
            side=OrderSide.BUY if args.action == "buy" else OrderSide.SELL,
            order_type=OrderType.MARKET if args.order_type == "market" else OrderType.LIMIT,
            quantity=args.quantity,
            price=args.price
        )
        result = broker.place_order(order)
        data = result.to_dict()

    elif args.action == "cancel":
        if not args.order_id:
            print("Error: --order-id required")
            sys.exit(1)
        success = broker.cancel_order(args.order_id)
        data = {'success': success, 'order_id': args.order_id}

    broker.disconnect()

    # Output
    if args.output == "json":
        print(json.dumps(data, indent=2))
    else:
        print(f"\n=== Broker: {args.broker.title()} ===\n")
        for k, v in data.items():
            if isinstance(v, list):
                print(f"\n{k}:")
                for item in v:
                    print(f"  {item}")
            else:
                print(f"{k}: {v}")


if __name__ == "__main__":
    main()
