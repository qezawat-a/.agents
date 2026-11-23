---
name: bitunix-official-docs
description: Verify any Bitunix Futures API call (REST or WebSocket) against the official exchange docs — endpoint paths, HTTP methods, request/response/push parameter names, types, required flags, enum values, rate limits, error codes, signing, liquidation/tiered risk limits, order units and the four TP/SL methods. Use before writing or debugging Bitunix trading code.
provider: Bitunix
---

# Bitunix Futures API — Official Reference

Generated from the official Bitunix documentation on 2026-11-23. Base URL: `https://fapi.bitunix.com`. Source pages: 50.

The [Endpoint Index](#endpoint-index) below gives the HTTP method, path and rate limit for every endpoint; the full request / response / push parameter tables are in [`references/endpoints.md`](references/endpoints.md). Use both to verify agent-generated code before you call the API: if a parameter name, type or required flag differs from these files, fix the code.

> Parameter names, types, enum values and required flags are taken verbatim from the official docs. Do not invent alternatives.

## Reference files

| File | Contents |
|---|---|
| `SKILL.md` (this file) | Conventions, signing, enums, endpoint index, WebSocket guide, error codes, order units, TP/SL methods, liquidation, debugging checklist |
| `references/endpoints.md` | Full request / response / push parameter tables for all 50 endpoints |

## How to use this skill

1. **Find the endpoint** in the [Endpoint Index](#endpoint-index) — match on the path, not the page title (two pages are both called "Get Funding Rate").
2. **Check the method and path** against the table. A wrong path is the most common failure: e.g. leverage/margin mode is `/api/v1/futures/account/get_leverage_margin_mode` (not `get_leverage_and_margin_mode`), and TP/SL lives under `/api/v1/futures/tpsl/...` (not `tp_sl`).
3. **Check every request parameter** — name, type, required flag. Required parameters that are missing produce `10002 Parameter Error`; unknown parameters are silently ignored, which is worse because the call "succeeds" with defaults.
4. **Check enum values** against [Conventions → Enumerations](#enumerations). `side` is `BUY`/`SELL`; `tradeSide` is `OPEN`/`CLOSE`; `effect` is `GTC`/`IOC`/`FOK`/`POST_ONLY`.
5. **Check the response envelope** — `code` must be `0`; anything else is an error code from the [Error Code](#error-code) table.
6. **For WebSocket code**, check the URL, the `op` values and the channel names in the [WebSocket Guide](#websocket-guide).

## Conventions

### Base URL and transport

| Item | Value |
|---|---|
| REST base URL | `https://fapi.bitunix.com` |
| Public WebSocket | `wss://fapi.bitunix.com/public/` |
| Private WebSocket | `wss://fapi.bitunix.com/private/` |
| Content type | `application/json` |
| Timestamp unit | milliseconds for REST, **seconds** for WebSocket `login` / `ping` |

### Authentication (REST)

Every private endpoint requires four headers:

| Header | Meaning |
|---|---|
| `api-key` | Your API key |
| `nonce` | Random string, **max 64 characters** (a 32-char UUID without dashes is typical) |
| `timestamp` | Current Unix time in **milliseconds**; must be within 60,000 ms of server time |
| `sign` | Signature, see below |
| `language` | Optional, e.g. `en-US` |

Signature algorithm (two SHA-256 passes, hex output):

```
digest = SHA256(nonce + timestamp + api_key + query_params + body)
sign   = SHA256(digest + secret_key)
```

- `query_params` is the query string with keys sorted ascending and concatenated as `keyvalue` with **no** separators and no URL encoding.
- `body` is the raw JSON string with no extra whitespace. For GET requests the body is empty.
- Both `digest` and `sign` are lowercase hex.

Reference implementation (Python, from the official `open-api/Demo`):

```python
import hashlib, time, uuid

def get_nonce():
    return str(uuid.uuid4()).replace('-', '')

def get_timestamp():
    return str(int(time.time() * 1000))

def sort_params(params):
    return ''.join(f"{k}{v}" for k, v in sorted(params.items()))

def generate_signature(api_key, secret_key, nonce, timestamp, query_params="", body=""):
    digest = hashlib.sha256((nonce + timestamp + api_key + query_params + body).encode()).hexdigest()
    return hashlib.sha256((digest + secret_key).encode()).hexdigest()

def get_auth_headers(api_key, secret_key, query_params="", body=""):
    nonce, timestamp = get_nonce(), get_timestamp()
    return {
        "api-key": api_key,
        "sign": generate_signature(api_key, secret_key, nonce, timestamp, query_params, body),
        "nonce": nonce,
        "timestamp": timestamp,
    }
```

### Response envelope

```json
{"code": 0, "msg": "result.success", "data": {...}, "success": true}
```

`code == 0` means success. Any other value is an error — look it up in [Error Code](#error-code). `data` is an object for single results and an array for list results.

### Rate limits

Rate limits are per endpoint and are stated in each section header. They are either `req/sec/ip` (public market data) or `req/sec/uid` (private account and trading). Exceeding them returns `10005` / `10006`.

### Enumerations

| Field | Values |
|---|---|
| `side` (order direction) | `BUY`, `SELL` |
| `tradeSide` (hedge mode) | `OPEN`, `CLOSE` |
| `orderType` / `type` | `LIMIT`, `MARKET` |
| `effect` (time in force) | `GTC` (default), `IOC`, `FOK`, `POST_ONLY` |
| `positionMode` | `ONE_WAY`, `HEDGE` |
| `marginMode` / `positionType` | `ISOLATION`, `CROSS` |
| `tpStopType` / `slStopType` | `MARK_PRICE`, `LAST_PRICE` |
| `tpOrderType` / `slOrderType` | `LIMIT`, `MARKET` |
| kline `type` | `LAST_PRICE`, `MARK_PRICE` (default `LAST_PRICE`) |
| kline `interval` | `1m` `5m` `15m` `30m` `1h` `2h` `4h` `6h` `8h` `12h` `1d` `3d` `1w` `1M` |
| depth `limit` | `1` `5` `15` `50` `max` |
| `orderStatus` | `INIT`, `NEW`, `PART_FILLED`, `CANCELED`, `FILLED`, `PART_FILLED_CANCELED` |
| `positionSide` | `LONG`, `SHORT` |

### Pagination

List endpoints take `skip` (default `0`) and `limit` (default `100`) and return a page object containing the rows plus a total count. Time-bounded queries take `startTime` / `endTime` as millisecond timestamps.

## Endpoint Index

| # | Endpoint | Type | Method | Path | Doc |
|---|---|---|---|---|---|
| 1 | Get Tickers | rest | GET | /api/v1/futures/market/tickers | [doc](https://www.bitunix.com/api-docs/futures/market/get_tickers.html) |
| 2 | Change Log | article | - | - | [doc](https://www.bitunix.com/api-docs/futures/log/change_log.html) |
| 3 | Adjust Position Margin | rest | POST | /api/v1/futures/account/adjust_position_margin | [doc](https://www.bitunix.com/api-docs/futures/account/adjust_position_margin.html) |
| 4 | Change Leverage | rest | POST | /api/v1/futures/account/change_leverage | [doc](https://www.bitunix.com/api-docs/futures/account/change_leverage.html) |
| 5 | Change Margin Mode | rest | POST | /api/v1/futures/account/change_margin_mode | [doc](https://www.bitunix.com/api-docs/futures/account/change_margin_mode.html) |
| 6 | Change Position Mode | rest | POST | /api/v1/futures/account/change_position_mode | [doc](https://www.bitunix.com/api-docs/futures/account/change_position_mode.html) |
| 7 | Get Leverage and Margin Mode | rest | GET | /api/v1/futures/account/get_leverage_margin_mode | [doc](https://www.bitunix.com/api-docs/futures/account/get_leverage_and_margin_mode.html) |
| 8 | Get Single Account | rest | GET | /api/v1/futures/account | [doc](https://www.bitunix.com/api-docs/futures/account/get_single_account.html) |
| 9 | Asset Query | rest | GET | /api/v1/cp/asset/query | [doc](https://www.bitunix.com/api-docs/futures/copyTrading/asset/asset_query.html) |
| 10 | Error Code | error_code | - | - | [doc](https://www.bitunix.com/api-docs/futures/ErrorCode/error_code.html) |
| 11 | Get Depth | rest | GET | /api/v1/futures/market/depth | [doc](https://www.bitunix.com/api-docs/futures/market/get_depth.html) |
| 12 | Get Funding Rate Batch | rest | GET | /api/v1/futures/market/funding_rate/batch | [doc](https://www.bitunix.com/api-docs/futures/market/get_funding_rate_batch.html) |
| 13 | Get Funding Rate History | rest | GET | /api/v1/futures/market/get_funding_rate_history | [doc](https://www.bitunix.com/api-docs/futures/market/get_funding_rate_history.html) |
| 14 | Get Funding Rate | rest | GET | /api/v1/futures/market/funding_rate | [doc](https://www.bitunix.com/api-docs/futures/market/get_funding_rate.html) |
| 15 | Get Kline | rest | GET | /api/v1/futures/market/kline | [doc](https://www.bitunix.com/api-docs/futures/market/get_kline.html) |
| 16 | Get Trading Pairs | rest | GET | /api/v1/futures/market/trading_pairs | [doc](https://www.bitunix.com/api-docs/futures/market/get_trading_pairs.html) |
| 17 | Get History Positions | rest | GET | /api/v1/futures/position/get_history_positions | [doc](https://www.bitunix.com/api-docs/futures/position/get_history_positions.html) |
| 18 | Get Pending Positions | rest | GET | /api/v1/futures/position/get_pending_positions | [doc](https://www.bitunix.com/api-docs/futures/position/get_pending_positions.html) |
| 19 | Get Position Tiers | rest | GET | /api/v1/futures/position/get_position_tiers | [doc](https://www.bitunix.com/api-docs/futures/position/get_position_tiers.html) |
| 20 | Cancel TP/SL Order | rest | POST | /api/v1/futures/tpsl/cancel_order | [doc](https://www.bitunix.com/api-docs/futures/tp_sl/cancel_tp_sl_order.html) |
| 21 | Get History TP/SL Order | rest | GET | /api/v1/futures/tpsl/get_history_orders | [doc](https://www.bitunix.com/api-docs/futures/tp_sl/get_history_tp_sl_order.html) |
| 22 | Get Pending TP/SL Order | rest | GET | /api/v1/futures/tpsl/get_pending_orders | [doc](https://www.bitunix.com/api-docs/futures/tp_sl/get_pending_tp_sl_order.html) |
| 23 | Modify Position TP/SL Order | rest | POST | /api/v1/futures/tpsl/position/modify_order | [doc](https://www.bitunix.com/api-docs/futures/tp_sl/modify_position_tp_sl_order.html) |
| 24 | Modify TP/SL Order | rest | POST | /api/v1/futures/tpsl/modify_order | [doc](https://www.bitunix.com/api-docs/futures/tp_sl/modify_tp_sl_order.html) |
| 25 | Place Position TP/SL Order | rest | POST | /api/v1/futures/tpsl/position/place_order | [doc](https://www.bitunix.com/api-docs/futures/tp_sl/place_position_tp_sl_order.html) |
| 26 | Place TP/SL Order | rest | POST | /api/v1/futures/tpsl/place_order | [doc](https://www.bitunix.com/api-docs/futures/tp_sl/place_tp_sl_order.html) |
| 27 | Batch Order | rest | POST | /api/v1/futures/trade/batch_order | [doc](https://www.bitunix.com/api-docs/futures/trade/batch_order.html) |
| 28 | Cancel All Orders | rest | POST | /api/v1/futures/trade/cancel_all_orders | [doc](https://www.bitunix.com/api-docs/futures/trade/cancel_all_orders.html) |
| 29 | Cancel Orders | rest | POST | /api/v1/futures/trade/cancel_orders | [doc](https://www.bitunix.com/api-docs/futures/trade/cancel_orders.html) |
| 30 | Close All Position | rest | POST | /api/v1/futures/trade/close_all_position | [doc](https://www.bitunix.com/api-docs/futures/trade/close_all_position.html) |
| 31 | Flash Close Position | rest | POST | /api/v1/futures/trade/flash_close_position | [doc](https://www.bitunix.com/api-docs/futures/trade/flash_close_position.html) |
| 32 | Get History Orders | rest | GET | /api/v1/futures/trade/get_history_orders | [doc](https://www.bitunix.com/api-docs/futures/trade/get_history_orders.html) |
| 33 | Get History Trades | rest | GET | /api/v1/futures/trade/get_history_trades | [doc](https://www.bitunix.com/api-docs/futures/trade/get_history_trades.html) |
| 34 | Get Order Detail | rest | GET | /api/v1/futures/trade/get_order_detail | [doc](https://www.bitunix.com/api-docs/futures/trade/get_order_detail.html) |
| 35 | Get Pending Orders | rest | GET | /api/v1/futures/trade/get_pending_orders | [doc](https://www.bitunix.com/api-docs/futures/trade/get_pending_orders.html) |
| 36 | Modify Order | rest | POST | /api/v1/futures/trade/modify_order | [doc](https://www.bitunix.com/api-docs/futures/trade/modify_order.html) |
| 37 | Place Order | rest | POST | /api/v1/futures/trade/place_order | [doc](https://www.bitunix.com/api-docs/futures/trade/place_order.html) |
| 38 | WebSocket Guide | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/prepare/WebSocket.html) |
| 39 | Balance Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/private/Balance%20Channel.html) |
| 40 | Order Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/private/Order%20Channel.html) |
| 41 | Position Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/private/Position%20Channel.html) |
| 42 | TP/SL Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/private/Tp%20Sl%20Channel.html) |
| 43 | Depth Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/public/depth%20channel.html) |
| 44 | Kline Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/public/kline%20channel.html) |
| 45 | Market Price Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/public/MarketPrice%20Channel.html) |
| 46 | Ticker Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/public/Ticker%20Channel.html) |
| 47 | Tickers Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/public/Tickers%20Channel.html) |
| 48 | Trade Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/public/Trade%20Channel.html) |
| 49 | Order Units | article | - | - | [doc](https://www.bitunix.com/hub/helpcenter/article/explanation-of-the-order-units-in-futures-trading?id=170) |
| 50 | Four TP/SL Execution Methods | article | - | - | [doc](https://www.bitunix.com/hub/academy/essential-beginners-guide/futures-trading-guide/bitunix-futures-positions-guide-to-four-tp-sl-methods) |

## Error Code

**Type:** error_code · **Method:** `-` · **Path:** `-`

Global error codes returned in the response envelope's `code` field. `code == 0` is success; every other value is a failure and `msg` carries the human-readable text.

Official doc: [https://www.bitunix.com/api-docs/futures/ErrorCode/error_code.html](https://www.bitunix.com/api-docs/futures/ErrorCode/error_code.html)

### Error Codes

| Code | Meaning | Typical cause / fix |
|---|---|---|
| 0 | Success | — |
| 403 | This API key does not support this operation | Key lacks the permission for this endpoint |
| 10001 | Network Error | Retry |
| 10002 | Parameter Error | A required parameter is missing, or a type/enum value is wrong |
| 10003 | api-key can't be empty | Missing `api-key` header |
| 10004 | The current ip is not in the apikey ip whitelist | Add the caller IP to the key's whitelist |
| 10005 | Too many requests, please try again later | Back off; respect the endpoint rate limit |
| 10006 | Request too frequently | Same as 10005 |
| 10007 | Sign signature error | Wrong signing order, unsorted query params, or body whitespace |
| 10008 | {value} does not comply with the rule, optional [correctValue] | Enum or format violation |
| 10009 | Another order operation is in progress, please try again shortly | Serialise order operations |
| 10010 | Nonce's length must be less than 64 | Shorten `nonce` |
| 10011 | The request timestamp must be within 60,000 ms of the server time | Clock drift; resync the host clock |
| 20001 | Market not exists | Wrong `symbol` |
| 20002 | The current positions amount has exceeded the maximum open limit, please adjust the risk limit | Position exceeds the tier's nominal-value cap |
| 20003 | Insufficient balance | Fund the account or reduce size |
| 20004 | Insufficient Trader | Copy-trading only |
| 20005 | Invalid leverage | Leverage outside the tier's allowed range |
| 20006 | You can't change leverage or margin mode as there are open orders | Cancel orders first |
| 20007 | Order not found, please try it later | Wrong `orderId` / `clientId` |
| 20008 | Insufficient amount | — |
| 20009 | Position exists, so positions mode cannot be updated | Close positions before switching `positionMode` |
| 20010 | Activation failed, the available balance in the futures account does not meet the conditions for activation of the coupon | — |
| 20011 | Account not allowed to trade | — |
| 20012 | This futures does not allow trading | — |
| 20013 | Function disabled due tp pending account deletion request | — |
| 20014 | Account deleted | — |
| 20015 | This futures is not supported | — |
| 20016 | Batch order exceeded the max size | `orderList` max length is 5 |
| 30001 | Failed to order. Please adjust the order price or the leverage as the order price dealt may immediately liquidate | Price too close to liquidation |
| 30002 | Price below liquidated price | — |
| 30003 | Price above liquidated price | — |
| 30004 | Position not exist | — |
| 30005 | The trigger price is closer to the current price and may be triggered immediately | Move the TP/SL trigger away |
| 30006 | Please select TP or SL | — |
| 30007 | TP trigger price is greater than average entry price | Long TP must be above entry |
| 30008 | TP trigger price is less than average entry price | Short TP must be below entry |
| 30009 | SL trigger price is less than average entry price | Long SL must be below entry |
| 30010 | SL trigger price is greater than average entry price | Short SL must be above entry |
| 30011 | Abnormal order status | — |
| 30012 | Already added to favorite | — |
| 30013 | Exceeded the maximum order quantity | — |
| 30014 | Max Buy Order Price | — |
| 30015 | Mini Sell Order Price | — |
| 30016 | The qty should be larger than | Below the minimum notional |
| 30017 | The qty cannot be less than the minimum qty | — |
| 30018 | Order failed. No position opened. Cancel [Reduce-only] settings and retry later | — |
| 30019 | Order failed. A [Reduce-only] order can not be in the same direction as the open position | — |
| 30020 | Trigger price for TP should be higher than mark price | — |
| 30021 | Trigger price for TP should be lower than mark price | — |
| 30022 | Trigger price for SL should be higher than mark price | — |
| 30023 | Trigger price fo SL should be lower than mark price | — |
| 30024 | Trigger price for SL should be lower than liq price | — |
| 30025 | Trigger price for SL should be higher than liq price | — |
| 30026 | TP price must be greater than last price | — |
| 30027 | TP price must be greater than mark price | — |
| 30028 | SL price must be less than last price | — |
| 30029 | SL price must be less than mark price | — |
| 30030 | SL price must be greater than last price | — |
| 30031 | SL price must be greater than mark price | — |
| 30032 | TP price must be less than last price | — |
| 30033 | TP price must be less than mark price | — |
| 30034 | TP price must be less than mark price | — |
| 30035 | SL price must be greater than trigger price | — |
| 30036 | TP price must be greater than trigger price | — |
| 30037 | TP price must be greater than trigger price | — |
| 30038 | TP/SL amount must be less than the size of the position | `tpQty` / `slQty` too large |
| 30039 | The order qty can't be greater than the max order qty | — |
| 30040 | Futures trading is prohibited, please contact customer service | — |
| 30041 | Trigger price must be greater than 0 | — |
| 30042 | Client ID duplicate | `clientId` must be unique per account |
| 40001 | Please cancel open orders and close all positions before canceling lead trading | — |
| 40002 | Lead amount hast to be over the limits | — |
| 40003 | Lead order amount exceeds the limits | — |
| 40004 | Please do not repeat the operation | — |
| 40005 | Action is not available for the current user type | — |
| 40006 | Sub-account reaches the limit | — |
| 40007 | Share settlement is being processed, lease try again later | — |
| 40008 | After the transfer, the account balance will be less than the order amount, please enter again | — |

---

## WebSocket Guide

**Type:** ws · **Method:** `-` · **Path:** `-`

Bitunix exposes two WebSocket endpoints. Both use the same JSON envelope and the same `op` / `ch` dispatch.

| Endpoint | URL | Auth |
|---|---|---|
| Public | `wss://fapi.bitunix.com/public/` | none |
| Private | `wss://fapi.bitunix.com/private/` | `login` op required |

Official doc: [https://www.bitunix.com/api-docs/futures/websocket/prepare/WebSocket.html](https://www.bitunix.com/api-docs/futures/websocket/prepare/WebSocket.html)

### Connection lifecycle

1. Open the socket. The server sends `{"op":"connect","..."}` — on the private socket this is the signal to log in.
2. **Private only:** send `login` (see below) and wait for `{"op":"login", ...}` before subscribing.
3. Send `ping` every few seconds (the official demo uses 3 s) and expect a `pong`.
4. Send `subscribe` with the channels you want.
5. Send `unsubscribe` to stop a channel.

### Heartbeat

```json
{"op": "ping", "ping": 1700000000}
```

`ping` is the Unix timestamp in **seconds**. The server replies with `{"op":"pong","pong":...}`. If no pong arrives, reconnect.

### Login (private socket)

```json
{
  "op": "login",
  "args": [{
    "apiKey": "your-api-key",
    "timestamp": 1700000000,
    "nonce": "32-char-random-string",
    "sign": "hex-signature"
  }]
}
```

The WebSocket signature is **different from REST** — there is no query string and no body, and the timestamp is in **seconds**:

```
digest = SHA256(nonce + timestamp + api_key)
sign   = SHA256(digest + secret_key)
```

```python
import hashlib, random, string, time

def ws_sign(api_key, secret_key):
    nonce = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    ts = str(int(time.time()))
    digest = hashlib.sha256((nonce + ts + api_key).encode()).hexdigest()
    sign = hashlib.sha256((digest + secret_key).encode()).hexdigest()
    return {"apiKey": api_key, "timestamp": int(ts), "nonce": nonce, "sign": sign}
```

### Subscribe / unsubscribe

```json
{"op": "subscribe",   "args": [{"ch": "depth_books", "symbol": "BTCUSDT"}]}
{"op": "unsubscribe", "args": [{"ch": "depth_books", "symbol": "BTCUSDT"}]}
```

`args` is a list, so several channels can be subscribed in one message. `ch` is the channel name; `symbol` is required for symbol-scoped channels and omitted for account-scoped private channels.

### Channel names

| Channel `ch` | Scope | Doc section |
|---|---|---|
| `balance` | private | [Balance Channel](references/endpoints.md#balance-channel) |
| `order` | private | [Order Channel](references/endpoints.md#order-channel) |
| `position` | private | [Position Channel](references/endpoints.md#position-channel) |
| `tpsl` | private | [TP/SL Channel](references/endpoints.md#tpsl-channel) |
| `depth_books`, `depth_book1`, `depth_book5`, `depth_book15` | public | [Depth Channel](references/endpoints.md#depth-channel) |
| `market_kline_<interval>`, `mark_kline_<interval>` | public | [Kline Channel](references/endpoints.md#kline-channel) |
| `price` | public | [Market Price Channel](references/endpoints.md#market-price-channel) |
| `ticker` | public | [Ticker Channel](references/endpoints.md#ticker-channel) |
| `tickers` | public | [Tickers Channel](references/endpoints.md#tickers-channel) |
| `trade` | public | [Trade Channel](references/endpoints.md#trade-channel) |

> The channel names are **not** the page titles. Depth is `depth_books` / `depth_book1` / `depth_book5` / `depth_book15` (there is no plain `depth_book`), and kline is `market_kline_<interval>` or `mark_kline_<interval>` (there is no plain `kline`). Subscribing to `depth` or `kline` silently yields nothing.

**Kline intervals** in the channel name: `1min` `3min` `5min` `15min` `30min` `60min` `2h` `4h` `6h` `8h` `12h` `1day` `3day` `1week` `1month`. Note these differ from the REST `interval` values (`1m`, `1h`, `1d`, `1w`, `1M`). To change interval you must `unsubscribe` the old channel before subscribing the new one.

### Push message shape

Every push carries `ch` (channel name) and `ts` (gateway send time in milliseconds — not the business event time). The payload is under `data`, either an object (private channels) or a list (public channels).

### Reconnect

Reconnect with backoff, re-login on the private socket, and re-subscribe every channel. Treat the socket as lossy: after a reconnect, re-fetch REST snapshots (positions, open orders, balance) rather than assuming the missed pushes will be replayed.

---

## Order Units

**Type:** article · **Method:** `-` · **Path:** `-`

Bitunix lets you size a futures order in three different units. The API's `qty` field is always the **quantity unit** (base asset), so convert before you send.

Official doc: [https://www.bitunix.com/hub/helpcenter/article/explanation-of-the-order-units-in-futures-trading?id=170](https://www.bitunix.com/hub/helpcenter/article/explanation-of-the-order-units-in-futures-trading?id=170)

### The three units

| Unit | Definition | Formula |
|---|---|---|
| **Nominal Value** | Market value of the position, in USDT. No leverage or margin involved. | `nominal = qty × price` |
| **Cost Value** | What you actually pay to open: initial margin plus fees. | `cost = nominal / leverage` |
| **Quantity Unit** | Amount of the underlying asset. This is the API's `qty`. | `qty = nominal / price` |

### Worked examples (BTCUSDT, price 10,000 USDT, leverage 10x, fees ignored)

**Ordering by nominal value — 1,000 USDT:**

```
cost = 1000 / 10   = 100 USDT
qty  = 1000 / 10000 = 0.1 BTC
```

**Ordering by cost value — 1,000 USDT:**

```
qty = cost × leverage / price = 1000 × 10 / 10000 = 1 BTC
```

**Ordering by quantity — 1 BTC:**

```
cost    = qty × price / leverage = 1 × 10000 / 10 = 1,000 USDT
nominal = qty × price            = 1 × 10000    = 10,000 USDT
```

### Converting for the API

```python
def qty_from_nominal(nominal_usdt, price):
    return nominal_usdt / price

def qty_from_cost(cost_usdt, price, leverage):
    return cost_usdt * leverage / price

def nominal_from_qty(qty, price):
    return qty * price
```

Notes:

- `qty` must respect the symbol's minimum quantity and step size — fetch them from [Get Trading Pairs](references/endpoints.md#get-trading-pairs) and round down, or the order fails with `30016` / `30017`.
- Cost value normally includes the opening fee, so the real cost is slightly above `nominal / leverage`.
- Leverage raises the position size for the same margin, and raises the cost and the PnL risk with it.

---

## Four TP/SL Execution Methods

**Type:** article · **Method:** `-` · **Path:** `-`

Bitunix offers four take-profit / stop-loss methods. They differ in **what they control** and **what happens at the trigger** — pick the method first, then the API call.

Official doc: [https://www.bitunix.com/hub/academy/essential-beginners-guide/futures-trading-guide/bitunix-futures-positions-guide-to-four-tp-sl-methods](https://www.bitunix.com/hub/academy/essential-beginners-guide/futures-trading-guide/bitunix-futures-positions-guide-to-four-tp-sl-methods)

### Comparison

| Method | Control unit | At trigger | Best for |
|---|---|---|---|
| **Position TP/SL** | One open position | Entire position closes | Simple, all-in/all-out rules |
| **Partial TP/SL** | One open position | A defined % of the position closes | Scaling out in stages |
| **Trailing TP/SL** | One open position | Dynamic exit after trend + retracement | Trend following |
| **Account TP/SL** | Whole futures account | All futures positions close | Multi-coin portfolio risk |

### 1. Position TP/SL

Fixed trigger prices for one position; the whole position closes when hit.

*Example:* long BTC at 60,000, TP at 65,000, SL at 58,000. At either price the entire position is closed.

*API:* [Place Position TP/SL Order](references/endpoints.md#place-position-tpsl-order) (`/api/v1/futures/tpsl/position/place_order`) with `symbol`, `positionId`, `tpPrice`, `tpStopType`, `slPrice`, `slStopType`. Modify with [Modify Position TP/SL Order](references/endpoints.md#modify-position-tpsl-order).

### 2. Partial TP/SL

Several closing ratios on one position, executed in stages.

*Example:* close 30% at 65,000, another 40% at 68,000, leave the rest running.

*API:* [Place TP/SL Order](references/endpoints.md#place-tpsl-order) (`/api/v1/futures/tpsl/place_order`) — this is the variant that carries `tpQty` / `slQty`, the size to close at each trigger. `tpQty` and `slQty` must not exceed the position size (`30038`).

### 3. Trailing TP/SL

Activates at an activation price, then closes on a retracement measured either as a **Ratio** (callback %) or an **Interval**.

*Example:** long ETH at 2,000, activation 2,000, 5% callback. Price runs to 2,500; a 5% pullback from the peak (to 2,375) closes the position at market.

*Behaviour:** for a long, the exit follows the price up and fires on a pullback; for a short, it follows the price down and fires on a bounce.

*API:* trailing orders are configured in the UI / order `effect` and TP-SL fields; the REST TP/SL endpoints above cover fixed-price TP/SL. Do not assume a `trailing` parameter exists on the TP/SL endpoints — check the endpoint's parameter table.

### 4. Account TP/SL

One trigger for the whole account, measured on total account PnL.

*Example:** holding BTC, ETH and SOL, set account TP at +1,000 USDT and account SL at −500 USDT. When total PnL reaches either threshold, **all** futures positions close.

*API:* account-level TP/SL is a UI/account setting, not a per-order field. It is not exposed by the order endpoints in this file.

### Choosing

- One position, one rule → **Position**.
- Want to bank profit in pieces → **Partial**.
- Expecting a sustained trend → **Trailing**.
- Many positions, one risk budget → **Account**.

### Common TP/SL errors

| Code | Meaning |
|---|---|
| 30005 | Trigger price too close to the current price — would fire immediately |
| 30007 / 30008 | TP on the wrong side of the average entry price |
| 30009 / 30010 | SL on the wrong side of the average entry price |
| 30020–30025 | Trigger on the wrong side of the mark price or the liquidation price |
| 30038 | `tpQty` / `slQty` larger than the position |
| 30006 | Neither TP nor SL supplied |

---

## Liquidation Mechanism and Tiered Risk Limit

Bitunix applies a **tiered risk limit** to all futures trading. It exists so that a large position is reduced in steps instead of being liquidated in one hit, and it is what caps the leverage you may use at a given position size.

Source: [Bitunix Futures — Liquidation Mechanism and Tiered Risk Limit](https://support.bitunix.com/hc/en-us/articles/32152530856601-Bitunix-Futures-Liquidation-Mechanism-and-Tiered-Risk-Limit)

### The four tier factors

Each tier defines four values:

| Factor | Meaning |
|---|---|
| **Tier** | The risk-limit level (1 is the lowest) |
| **Nominal value** | The position-value range the tier covers, in USDT |
| **Max leverage** | The highest leverage allowed inside that range |
| **Maintenance margin rate** | The margin rate required to hold a position in that tier |

The tier is selected by the **leverage you choose**, and the order/position value must fall inside that tier's nominal-value range. Example for BTC perpetual: at 50x the position sits in tier 3, whose maximum value is 2,500,000 USDT.

### Where the tier bites

1. **Order placement** — an order whose resulting position value exceeds the tier's cap is rejected (`20002`).
2. **Liquidation** — the maintenance margin rate is taken from the tier matching the *actual* position value, and that rate drives the margin ratio and the liquidation price.

### Liquidation sequence

When a position enters forced liquidation, the system does **not** immediately close it:

1. **Cancel open orders** to release margin.
2. **Re-check
** the liquidation condition.
3. If still at risk and the tier is **above 1**, **partially reduce** the position to drop it into a lower tier, which lowers the required maintenance margin rate. Re-check after every reduction.
4. If the tier is **already 1** and the position still fails the maintenance-margin requirement, **force-liquidate*** it.

The partial close uses a **FOK (
Fill or Kill)** order. If the FOK fails, the whole position is liquidated.

**Cross margin:** the system checks whether *any* open position is above tier 1, reduces according to the reduction priority, and re-detects liquidation risk after each reduction. If every position is already at tier 1 and liquidation still triggers, forced liquidation runs.

**Isolated margin:** the system checks the tier of the affected position only, cascading reductions until it reaches tier 1, then force-liquidates.

### Position reduction priority

When several positions could be reduced, the order is:

1. Positions with the **higher risk-limit tier**.
2. Positions that **release more maintenance margin** when reduced.
3. Positions with the **higher nominal value**.

### Worked example

A position worth 5,000,000 USDT sits in tier 4. Liquidation triggers:

```
reduced value = position value − limit amount of the original tier
              = 5,000,000 − 2,500,000
              = 2,500,000 USDT
```

The position is cut to 2,500,000 USDT, which moves it to tier 3; the maintenance margin rate is recalculated and the position returns to normal. If it is still at risk, the reduction repeats until it is healthy or liquidated.

### Practical rules for trading code

- Read the live tiers from [Get Position Tiers](references/endpoints.md#get-position-tiers) (`GET /api/v1/futures/position/get_position_tiers?symbol=...`) before sizing a large order — do not hardcode the table, it changes per symbol.
- Compute the liquidation price from the **tier's** maintenance margin rate, not a single global rate.
- Treat `20002` as "reduce size or lower leverage", not as a transient error to retry.
- A `30001` on entry means the price is close enough to liquidation that the order would be liquidated on fill — widen the distance or cut leverage.

---

## Debugging checklist

Run through this before blaming the exchange:

1. **Path** — compare character by character with the [Endpoint Index](#endpoint-index). Frequent traps: `get_leverage_margin_mode` (not `get_leverage_and_margin_mode`), `/futures/tpsl/` (not `/futures/tp_sl/`), `/futures/trade/batch_order` (not `batch_orders`).
2. **Method** — every `get_*` is `GET`; every `place_*`, `cancel_*`, `modify_*`, `change_*`, `adjust_*`, `close_*`, `flash_*` is `POST`.
3. **Auth** — `api-key`, `nonce` (≤64 chars), `timestamp` in **milliseconds**, `sign` = `SHA256(SHA256(nonce+timestamp+api_key+query+body) + secret)`. Query params sorted, concatenated as `keyvalue`, no separators.
4. **Required params** — every row marked `yes` in the request table must be present. `10002` almost always means one is missing.
5. **Enums** — `BUY`/`SELL` for `side`, `OPEN`/`CLOSE` for `tradeSide`, `GTC`/`IOC`/`FOK`/`POST_ONLY` for `effect`.
6. **Types** — prices and quantities are **strings** in the request body, not numbers.
7. **Response** — check `code == 0`, then read `data`. A `200` HTTP status with `code != 0` is still a failure.
8. **WebSocket** — right URL (`/public/` vs `/private/`), `login` before subscribing on the private socket, channel names `depth_books` / `market_kline_<interval>` / `price` / `ticker` / `tickers` / `trade` / `balance` / `order` / `position` / `tpsl`, `ping` timestamp in **seconds**.
9. **Rate limit** — respect the per-endpoint limit in the section header; `10005`/`10006` mean back off.
10. **Risk** — a `20002` or `30001` is a risk-limit problem, not a bug: see [Liquidation Mechanism and Tiered Risk Limit](#liquidation-mechanism-and-tiered-risk-limit).
