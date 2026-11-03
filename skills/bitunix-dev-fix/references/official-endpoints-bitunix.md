# Official Bitunix Futures Endpoints

## Endpoint Categories

### 1. Market Data APIs (Public)
- `GET /api/v1/futures/market/tickers` - 24h ticker data
- `GET /api/v1/futures/market/depth` - Order book depth
- `GET /api/v1/futures/market/kline` - Candlestick data
- `GET /api/v1/futures/market/funding_rate` - Current funding rate
- `GET /api/v1/futures/market/funding_rate/batch` - Batch funding rates
- `GET /api/v1/futures/market/funding_rate/history` - Funding rate history
- `GET /api/v1/futures/market/index_price` - Index price
- `GET /api/v1/futures/market/mark_price` - Mark price
- `GET /api/v1/futures/market/trading_pairs` - Trading pairs info

### 2. Account APIs (Private - Auth Required)
- `GET /api/v1/futures/account` - Account balance
- `GET /api/v1/futures/account/get_leverage_margin_mode` - Get leverage/margin
- `POST /api/v1/futures/account/change_leverage` - Change leverage
- `POST /api/v1/futures/account/change_margin_mode` - Change margin mode
- `POST /api/v1/futures/account/change_position_mode` - Change position mode
- `POST /api/v1/futures/account/adjust_position_margin` - Adjust margin
- `GET /api/v1/cp/asset/query` - Copy trading assets

### 3. Position APIs (Private - Auth Required)
- `GET /api/v1/futures/position/get_pending_positions` - Open positions
- `GET /api/v1/futures/position/get_history_positions` - Historical positions
- `GET /api/v1/futures/position/get_position_tiers` - Risk tiers

### 4. Trade APIs (Private - Auth Required)
- `POST /api/v1/futures/trade/place_order` - Place order
- `POST /api/v1/futures/trade/batch_order` - Batch orders (max 20)
- `POST /api/v1/futures/trade/cancel_orders` - Cancel orders
- `POST /api/v1/futures/trade/cancel_all_orders` - Cancel all orders
- `POST /api/v1/futures/trade/close_all_position` - Close all positions
- `POST /api/v1/futures/trade/flash_close_position` - Flash close
- `GET /api/v1/futures/trade/get_pending_orders` - Open orders
- `GET /api/v1/futures/trade/get_history_orders` - Historical orders
- `GET /api/v1/futures/trade/get_history_trades` - Trade history
- `GET /api/v1/futures/trade/get_order_detail` - Order details

### 5. TP/SL APIs (Private - Auth Required)
- `POST /api/v1/futures/tpsl/position/place_order` - Place position-level TP/SL
- `POST /api/v1/futures/tpsl/position/modify_order` - Modify position TP/SL
- `POST /api/v1/futures/tpsl/place_order` - Place partial TP/SL
- `POST /api/v1/futures/tpsl/modify_order` - Modify partial TP/SL
- `POST /api/v1/futures/tpsl/cancel_order` - Cancel TP/SL
- `GET /api/v1/futures/tpsl/get_pending_orders` - Pending TP/SL
- `GET /api/v1/futures/tpsl/get_history_orders` - TP/SL history

---

## Rate Limits

- **Default**: 10 requests per second
- **Internal throttle**: 8 req/s (our implementation)
- **Retryable errors**: 10001, 10005, 10006, 40007

---

## Base URLs

| Environment | URL |
|-------------|-----|
| Futures | `https://fapi.bitunix.com` |
| Spot | `https://openapi.bitunix.com` |

---

## WebSocket URLs

| Channel Type | URL |
|--------------|-----|
| Futures | `wss://fstream.bitunix.com/ws` |
| Spot | `wss://stream.bitunix.com/ws` |

---

## Latest Documentation

Official API docs: https://www.bitunix.com/api-docs/futures/
Error codes: https://www.bitunix.com/api-docs/futures/ErrorCode/error_code.html