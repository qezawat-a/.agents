# WebSocket Channels

Part of the Bitunix Futures API reference. Conventions, signing, the endpoint index and the WebSocket guide live in `SKILL.md`.

## Balance Channel

Balance

### Push Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| ch | string | - | Channel name: balance |
| ts | number | - | Time stamp |
| data | <object> | - |  |
| coin | string | - | coin |
| available | string | - | available |
| frozen | string | - | frozen = isolationFrozen + crossFrozen |
| isolationFrozen | string | - | Freeze on a per warehouse basis |
| crossFrozen | string | - | Full warehouse entrusted freeze |
| margin | string | - | Margin |
| isolationMargin | string | - | Warehouse by warehouse margin. |
| crossMargin | string | - | Full warehouse margin. |
| expMoney | string | - | Experience Money. |

---

## Order Channel

Subscribe the order channel<br><br>Data will be pushed when the following events occured:<br><br>Open/Close orders are created<br><br>Open/Close orders are filled<br><br>Orders canceled

### Push Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| ch | string | - | Channel name: order |
| ts | number | - | Gateway send time in milliseconds. Not business event time; do not confuse with ctime / mtime. |
| data | <object> | - | Subscription data |
| event | string | - | Event，CREATE/UPDATE/CLOSE |
| orderId | string | - | order Id |
| symbol | string | - | Symbol |
| positionType | string | - | Margin mode,ISOLATION/CROSS |
| positionMode | string | - | Position mode,ONE_WAY/HEDGE |
| side | string | - | Sell,BUY/SELL |
| effect | string | - | Order expiration date.Required if the orderType is limit.IOC: Immediate or cancel;FOK: Fill or kill;GTC: Good till canceled(default value);POST_ONLY: POST only; |
| type | string | - | LIMIT/MARKET |
| qty | string | - | Amount (base coin) |
| price | string | - | Price of the order. Required if the order type is LIMIT |
| ctime | string | - | Create time, ISO-8601 nanosecond string, e.g. 2024-05-16T08:13:09.123456789Z |
| mtime | string | - | Last modify time, ISO-8601 nanosecond string. Same format as ctime. REST order APIs use millisecond integers. |
| leverage | string | - | Leverage |
| orderStatus | string | - | INIT:prepare status;NEW:pending;PART_FILLED:partially filled;CANCELED:canceled;FILLEDAll filled;PART_FILLED_CANCELED:part filled canceled; |
| fee | string | - | Deducted transaction fees: transaction fees deducted during the position |
| averagePrice | string | - | Average price |
| dealAmount | string | - | Deal amount |
| clientId | string | - | Client ID |
| tpStopType | string | - | Take profit trigger type.MARK_PRICE/LAST_PRICE |
| tpPrice | string | - | Take profit trigger price |
| tpOrderType | string | - | Take profit trigger place order type.LIMIT/MARKET |
| tpOrderPrice | string | - | Take profit trigger place order price.LIMIT/MARKET |
| slStopType | string | - | Stop loss trigger type.MARK_PRICE/LAST_PRICE |
| slPrice | string | - | Stop loss trigger price |
| slOrderType | string | - | Stop loss trigger place order type.LIMIT/MARKET |
| slOrderPrice | string | - | Stop loss trigger place order price.LIMIT/MARKET |

---

## Position Channel

Subscribe the position channel<br><br>Data will be pushed when the following events occurred:<br><br>Open/Close orders are created<br><br>Open/Close orders are filled<br><br>Orders are canceled

### Push Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| ch | string | - | Channel name: position |
| ts | number | - | Time stamp |
| data | <object> | - | Subscription data |
| event | string | - | Event，OPEN/UPDATE/CLOSE |
| positionId | string | - | position Id |
| marginMode | string | - | Margin mode,ISOLATION/CROSS |
| positionMode | string | - | Position mode,ONE_WAY/HEDGE |
| side | string | - | Position direction,SHORT/LONG |
| leverage | string | - | Leverage |
| margin | string | - | margin |
| ctime | string | - | Create time |
| qty | string | - | Open position size |
| symbol | string | - | Symbol |
| realizedPNL | string | - | Realized PnL(exclude funding fee and transaction fee) |
| unrealizedPNL | string | - | Unrealized PnL |
| funding | string | - | total funding fee during the position |
| fee | string | - | Deducted transaction fees: transaction fees deducted during the position |

---

## TP/SL Channel

TP/SL Order<br><br>After private WebSocket login succeeds, this channel is pushed automatically. Channel name is tpsl. data is always an object, not an array.<br><br>CLOSE alone is not a final state. Always read event together with status. Partial fill / full fill of the child order is pushed on the order channel or queried via REST, not on tpsl.<br><br>FILLED means the TP/SL trigger succeeded and the child order was placed. It does not mean the child order is fully filled.<br><br>Statuses that are not pushed: INIT, PENDING_CANCEL, TRIGGER_WAIT_PLACE. Do not document PART_FILLED on this channel.

### Push Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| ch | string | - | Channel name: tpsl |
| ts | number | - | Gateway send time, Unix milliseconds. Do not use this field to order business events. |
| data | <object> | - | Always an object (not an array) |
| event | string | - | CREATE / UPDATE / CLOSE |
| positionId | string | - | position Id |
| orderId | string | - | order Id |
| symbol | string | - | Symbol |
| leverage | string | - | Leverage |
| side | string | - | BUY/SELL |
| positionMode | string | - | Position mode, ONE_WAY/HEDGE |
| status | string | - | NEW / CANCELED / SYSTEM_CANCELED / FILLED / FAILED. See event-status table below. |
| ctime | string | - | Create time, ISO-8601 nanosecond string, e.g. 2024-05-16T08:13:09.123456789Z. REST history APIs use millisecond integers instead. |
| type | string | - | LIMIT/MARKET |
| tpQty | string | - | Take-profit order quantity (base coin). Omitted if unused. |
| slQty | string | - | Stop-loss order quantity (base coin). Omitted if unused. Never Boolean. Never JSON null. "0" is sent as "0". |
| tpStopType | string | - | take profit trigger type. MARK_PRICE/LAST_PRICE |
| tpPrice | string | - | take profit trigger price |
| tpOrderType | string | - | take profit trigger place order type. LIMIT/MARKET |
| tpOrderPrice | string | - | take profit trigger place order price |
| slStopType | string | - | stop loss trigger type. MARK_PRICE/LAST_PRICE |
| slPrice | string | - | stop loss trigger price |
| slOrderType | string | - | stop loss trigger place order type. LIMIT/MARKET |
| slOrderPrice | string | - | stop loss trigger place order price |

---

## Depth Channel

Use books for snapshot data, book1 for 1 depth level, book5 for 5 depth levels, book15 for 15 depth levels.<br><br>books: Push the full snapshot data for the first time, push all afterwards, that is, if there is a change in depth, the depth data that has changed will be pushed.<br><br>book1: 1 depth level will be pushed every time.<br><br>book5: 5 depth levels will be pushed every time.<br><br>book15: 15 depth levels will be pushed every time.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| op | string | yes | Operation, subscribe unsubscribe |
| args | list<object> | yes | List of channels to request subscription |
| ch | string | yes | Channel name: depth_books,depth_book1,depth_book5,depth_book15 |
| symbol | string | yes | Product ID |

### Push Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| ch | object | - | Channel name |
| symbol | string | - | Product ID |
| ts | number | - | Time stamp |
| data | string | - | Subscription data |
| a | list<string> | - | Seller depth |
| b | list<string> | - | Buyer depth |

---

## Kline Channel

Retrieve the candlesticks data of a symbol. Data will be pushed every 500 ms.<br><br>The channel will push a snapshot after successful subscription, followed by subsequent updates.<br><br>To switch K-line intervals without disconnecting the WebSocket, you must first send an "unsubscribe" command to cancel the previous K-line subscription before subscribing to the new interval. For example, if you are currently subscribed to mark_kline_1min and want to switch to mark_kline_15min, you must first unsubscribe from mark_kline_1min and then subscribe to mark_kline_15min.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| op | string | yes | Operation, subscribe unsubscribe |
| args | list<object> | yes | List of channels to request subscription |
| ch | string | yes | Channel name, The subscription channel is: Price TypeklineTime Interval；The price types include market price and marked price；market_kline_1min,mark_kline_1min,market_kline_3min,mark_kline_3min,market_kline_5min,mark_kline_5min,market_kline_15min,mark_kline_15min,market_kline_30min,mark_kline_30min,market_kline_60min,mark_kline_60min,market_kline_2h,mark_kline_2h,market_kline_4h,mark_kline_4h,market_kline_6h,mark_kline_6h,market_kline_8h,mark_kline_8h,market_kline_12h,mark_kline_12h,market_kline_1day,mark_kline_1day,market_kline_3day,mark_kline_3day,market_kline_1week,mark_kline_1week,market_kline_1month,mark_kline_1month |
| symbol | string | yes | Product ID E.g. ETHUSDT |

### Push Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| ch | string | - | Channel name |
| symbol | string | - | Product ID E.g. ETHUSDT |
| ts | number | - | Time stamp |
| data | list<string> | - | Subscription data |
| o | string | - | Opening price |
| h | string | - | Highest price |
| l | string | - | Lowest price |
| c | string | - | Closing price |
| b | string | - | Trading volume of the coin |
| q | string | - | Trading volume of quote currency |

---

## Market Price Channel

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| op | string | yes | Operation, subscribe unsubscribe |
| args | list<object> | yes | op list |
| symbol | string | yes | Product ID e.g: ETHUSDT |
| ch | string | yes | Channel, price |

### Push Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| ch | string | - | Channel name |
| symbol | string | - | Product ID E.g. ETHUSDT |
| ts | number | - | Time stamp |
| data | list<string> | - | Subscription data |
| mp | string | - | Market price |
| ip | string | - | Index price |
| fr | string | - | Funding rate |
| ft | string | - | Funding rate settlement time |
| nft | string | - | Next funding rate settlement time |

---

## Ticker Channel

24hr rolling window mini-ticker statistics for all symbols. These are NOT the statistics of the UTC day, but a 24hr rolling window from requestTime to 24hrs before.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| op | string | yes | Operation, subscribe unsubscribe |
| args | list<object> | yes |  |
| symbol | string | yes | Product ID e.g: ETHUSDT |
| ch | string | yes | Channel, ticker |

### Push Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| ch | string | - | Channel name |
| symbol | string | - | Product ID E.g. ETHUSDT |
| ts | number | - | Time stamp |
| data | list<string> | - | Subscription data |
| s | string | - | Symbol, Product ID E.g. ETHUSDT |
| o | string | - | Opening price |
| h | string | - | Highest price |
| l | string | - | Lowest price |
| la | string | - | Last price |
| b | string | - | Trading volume of the coin |
| q | string | - | Trading volume of quote currency |
| r | string | - | 24-hour fluctuations |

---

## Tickers Channel

24-hour rolling window mini-ticker statistics for all symbols (this is aggregated stream ticker data, with a different data structure compared to individual ticker subscription). These statistics are not based on UTC daily data, but rather a 24-hour rolling window from the request time backward.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| op | string | yes | Operation, subscribe unsubscribe |
| args | list<object> | yes |  |
| symbol | string | yes | Product ID e.g: ETHUSDT |
| ch | string | yes | Channel, tickers |

### Push Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| ch | string | - | Channel name |
| ts | number | - | Time stamp |
| data | list<string> | - | Subscription data |
| s | string | - | symbol, Product ID E.g. ETHUSDT |
| o | string | - | Opening price |
| h | string | - | Highest price |
| l | string | - | Lowest price |
| la | string | - | Last price |
| b | string | - | Trading volume of the coin |
| q | string | - | Trading volume of quote currency |
| r | string | - | 24-hour fluctuations |
| bd | string | - | Best Bid Price |
| ak | string | - | Best Ask Price |
| bv | string | - | Best Bid Volume |
| av | string | - | Best Ask Volume |

---

## Trade Channel

Get the public trade data

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| op | string | yes | Operation, subscribe unsubscribe |
| args | list<object> | yes | op list |
| symbol | string | yes | Product ID e.g: ETHUSDT |
| ch | string | yes | Channel, trade |

### Push Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| ch | string | - | Channel, trade |
| symbol | string | - | Symbol: ETHUSDT |
| ts | string | - | Time stamp |
| data | list<object> | - | Data |
| p | string | - | Filled price |
| v | string | - | Filled amount |
| s | string | - | Filled side, sell/buy |
| t | string | - | Time stamp |

---
