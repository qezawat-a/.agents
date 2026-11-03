# Bitunix API Review Checklist

Use this checklist when reviewing or debugging Bitunix API integrations.

---

## Request Authenticity

- [ ] **Signing correct?**
  - [ ] nonce = 32-char hex (16 bytes random)
  - [ ] timestamp in milliseconds (REST)
  - [ ] query string sorted by key ASCII, concatenated key+value
  - [ ] digest = SHA256(nonce + timestamp + apiKey + queryParams + body)
  - [ ] sign = SHA256(digest + secretKey)
  - [ ] Headers: api-key, nonce, timestamp, sign, language: en-US, Content-Type: application/json

- [ ] **API Key permissions**
  - [ ] Read/Write access enabled as needed
  - [ ] Futures trade permissions enabled

---

## Parameter Validation

### Common Required Fields
- [ ] `symbol` = uppercase, e.g., "BTCUSDT" (not "btcusdt")
- [ ] `marginCoin` = "USDT" (MUST be sent on all trade endpoints)
- [ ] `qty` = base coin units
- [ ] `leverage` = integer 1-125

### Order Placement
- [ ] `side` = "BUY" or "SELL" (names POSITION, not direction)
- [ ] `orderType` = "LIMIT" or "MARKET"
- [ ] `price` provided for LIMIT orders
- [ ] In HEDGE mode: `tradeSide` = "OPEN" or "CLOSE" + `positionId` for closes

### Kline Data
- [ ] Parameter name is `type` (NOT `klineType`)
- [ ] `type` = "LAST_PRICE" or "MARK_PRICE"
- [ ] Interval has `min` suffix for WebSocket: `market_kline_1min`

### TP/SL
- [ ] Position-level TP/SL: use `/tpsl/position/` endpoints
- [ ] Partial TP/SL: use `/tpsl/` endpoints with `qty`
- [ ] `tpStopType`/`slStopType` = "MARK_PRICE" or "LAST_PRICE"

---

## Error Handling

### Retryable Codes (4xx-like)
- [ ] Code 10001: Network Error → retry with exponential backoff
- [ ] Code 10005: Too many requests → wait before retry
- [ ] Code 10006: Rate limited → back off
- [ ] Code 40007: Settlement in progress → wait and retry

### Non-Retryable Errors
- [ ] Code 10002: Parameter Error → fix request
- [ ] Code 10007: Signature error → regenerate sign
- [ ] Code 20005: Invalid leverage → check limits
- [ ] Code 30002/30003: Liquidation constraint → adjust stop

---

## Position & Trade Checks

- [ ] **Leverage valid?**
  - [ ] Between 1-125
  - [ ] Within position tier ceiling
  - [ ] ATR stop fits inside liquidation distance

- [ ] **Order feasibility**
  - [ ] qty >= minimum order size for symbol
  - [ ] Margin sufficient at configured leverage
  - [ ] Not at exchange pair limit

- [ ] **Position mode consistency**
  - [ ] ONE_WAY: single position, opposite side closes
  - [ ] HEDGE: BUY open long, SELL open short; CLOSE requires positionId

---

## Stop Loss & Liquidation

### Liquidation Formula (Isolated Margin)
```
Long:  Liq = Entry × (1 - 1/Leverage + MMR)
Short: Liq = Entry × (1 + 1/Leverage - MMR)
```

- [ ] Stop is clamped inside liquidation price
- [ ] Stop respects fee-band floor (`min_stop_pct`)
- [ ] If stop can't fit → REFUSE trade (don't de-lever automatically)

### TP/SL Placement Order
- [ ] Place TP/SL immediately after order fills
- [ ] Use `marginCoin` in TP/SL endpoints
- [ ] Verify TP/SL order status

---

## WebSocket Notes

- [ ] Ping every 5 seconds to keep connection alive
- [ ] Batch subscriptions of 20 max
- [ ] Max 4 outbound messages per second
- [ ] Max 300 subscriptions at once
- [ ] Minute klines use `1min` suffix (not `1m`)

---

## Common Bugs to Check

- [ ] Forgetting `marginCoin` on trade endpoints
- [ ] Using `klineType` instead of `type`
- [ ] `side` direction confusion in HEDGE mode
- [ ] Not sending `tradeSide` for hedge mode closes
- [ ] Wrong URL: spot vs futures base URL
- [ ] Timestamp drift (should sync with server time)
- [ ] Using float for qty (should be string)
- [ ] Not handling PART_FILLED_CANCELED as a real fill

---

## Test Cases Required

- [ ] Place and fill order at market price
- [ ] Place and partially fill limit order
- [ ] Cancel order successfully
- [ ] Cancel all orders for symbol
- [ ] Get pending positions
- [ ] Adjust isolated margin
- [ ] Place position-level TP/SL
- [ ] Modify position TP/SL
- [ ] Get pending TP/SL orders
- [ ] Handle all retryable error codes
- [ ] Sign verification (client-side test)