# Broker Integration Guide

## Overview

The broker interface provides a unified API for:
- Order placement and management
- Position tracking
- Account information
- Real-time quotes

## Supported Brokers

### Simulated Broker (Default)
- No API key required
- Full functionality for testing
- Paper trading environment
- Uses Yahoo Finance for quotes

### Futu (富途证券)
- **Markets**: US, HK, A-Share (via connect)
- **Requirements**: Futu OpenD running locally
- **Install**: `pip install futu-api`
- **Note**: Implementation placeholder

### Tiger (老虎证券)
- **Markets**: US, HK, A-Share
- **Requirements**: Tiger Trade API credentials
- **Install**: `pip install tigeropen`
- **Note**: Implementation placeholder

### Interactive Brokers
- **Markets**: Global
- **Requirements**: TWS or IB Gateway running
- **Install**: `pip install ib_insync`
- **Note**: Implementation placeholder

## Quick Start

### Using Simulated Broker
```bash
# Connect and check account
python broker_interface.py connect --broker simulated

# Get account info
python broker_interface.py account --broker simulated

# Place a buy order
python broker_interface.py buy --symbol AAPL --quantity 100

# Check positions
python broker_interface.py positions

# Place a sell order
python broker_interface.py sell --symbol AAPL --quantity 50
```

### Paper Trading System
```bash
# Buy with risk checks
python paper_trading.py buy --symbol AAPL --quantity 100

# Check performance
python paper_trading.py performance

# View open positions
python paper_trading.py positions

# Close a trade
python paper_trading.py close --trade-id ABC123

# Export trade history
python paper_trading.py export
```

## API Reference

### Order Types
| Type | Description | Parameters |
|------|-------------|------------|
| Market | Execute immediately | symbol, quantity |
| Limit | Execute at price or better | symbol, quantity, price |
| Stop | Trigger at price | symbol, quantity, stop_price |
| Stop-Limit | Stop trigger + limit | symbol, quantity, stop_price, price |

### Order Status
| Status | Description |
|--------|-------------|
| pending | Order created, not submitted |
| submitted | Sent to broker |
| partial | Partially filled |
| filled | Fully executed |
| cancelled | Cancelled by user |
| rejected | Rejected by broker |

## Risk Controls

### Paper Trading Risk Parameters
```python
RiskParameters:
  max_position_size: 10%      # Max per position
  max_portfolio_risk: 2%      # Max total risk
  max_drawdown: 15%           # Stop trading trigger
  daily_loss_limit: 3%        # Daily max loss
  max_open_positions: 10      # Position count limit
  stop_loss_pct: 5%           # Default stop
  take_profit_pct: 10%        # Default target
```

### Risk Checks Before Trade
1. Position size vs limit
2. Number of open positions
3. Daily loss limit
4. Maximum drawdown
5. Buying power

## Implementing a New Broker

### Interface Methods
```python
class BrokerInterface(ABC):
    def connect(self) -> bool: ...
    def disconnect(self) -> bool: ...
    def get_account_info(self) -> AccountInfo: ...
    def get_positions(self) -> List[Position]: ...
    def get_orders(self, status=None) -> List[Order]: ...
    def place_order(self, order: Order) -> Order: ...
    def cancel_order(self, order_id: str) -> bool: ...
    def modify_order(self, order_id: str, ...) -> Order: ...
    def get_quote(self, symbol: str) -> Dict: ...
```

### Example Implementation
```python
class FutuBroker(BrokerInterface):
    def __init__(self, config):
        super().__init__(config)
        self.host = config.get('host', '127.0.0.1')
        self.port = config.get('port', 11111)

    def connect(self):
        from futu import OpenQuoteContext, OpenTradeContext
        self.quote_ctx = OpenQuoteContext(self.host, self.port)
        self.trade_ctx = OpenTradeContext(self.host, self.port)
        self.connected = True
        return True
```

## Data Classes

### Order
```python
@dataclass
class Order:
    order_id: str
    symbol: str
    side: OrderSide  # BUY or SELL
    order_type: OrderType  # MARKET, LIMIT, etc.
    quantity: int
    price: Optional[float]
    stop_price: Optional[float]
    status: OrderStatus
    filled_quantity: int
    filled_price: Optional[float]
    created_at: str
    updated_at: str
```

### Position
```python
@dataclass
class Position:
    symbol: str
    quantity: int
    avg_cost: float
    market_value: float
    unrealized_pnl: float
    unrealized_pnl_pct: float
```

### AccountInfo
```python
@dataclass
class AccountInfo:
    account_id: str
    currency: str
    cash: float
    buying_power: float
    total_value: float
    margin_used: float
    margin_available: float
```

## Environment Variables

For production brokers, set credentials via environment:

```bash
# Futu
export FUTU_HOST=127.0.0.1
export FUTU_PORT=11111

# Tiger
export TIGER_ID=your_tiger_id
export TIGER_PRIVATE_KEY=/path/to/key.pem

# Interactive Brokers
export IB_HOST=127.0.0.1
export IB_PORT=7497
export IB_CLIENT_ID=1
```

## Best Practices

### Testing
1. Always start with simulated broker
2. Test all order types
3. Verify risk controls work
4. Test edge cases (partial fills, rejections)

### Production
1. Use paper trading first
2. Start with small positions
3. Monitor logs closely
4. Have kill switch ready

### Error Handling
```python
try:
    order = broker.place_order(order)
    if order.status == OrderStatus.REJECTED:
        logger.error(f"Order rejected: {order}")
except ConnectionError:
    logger.error("Lost connection to broker")
    # Attempt reconnection
except Exception as e:
    logger.error(f"Unexpected error: {e}")
```

## Limitations

### Simulated Broker
- No real market data (uses Yahoo Finance)
- Instant fills (no slippage simulation)
- No partial fills
- No extended hours trading

### General
- Rate limits vary by broker
- Real-time data may have delays
- Weekend/holiday restrictions
- Account-specific limitations
