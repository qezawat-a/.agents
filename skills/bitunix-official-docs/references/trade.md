# Trade Endpoints

Part of the Bitunix Futures API reference. Conventions, signing, the endpoint index and the WebSocket guide live in `SKILL.md`.

## Batch Order

Place order

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | Trading pair |
| orderList | array | yes | Order list, maximum length: 5 |
| qty | string | yes | Amount (base coin) |
| price | string | no | Price of the order.<br>Required if the order type is LIMIT |
| side | string | yes | Order direction<br>buy: BUY<br>sell: SELL |
| tradeSide | string | yes | Direction<br>Only required in hedge-mode<br>Open and Close Notes:<br>For open long, side fill in"BUY"; tradeSide should be "OPEN"<br>For open short, side fill in "SELL"; tradeSide should be "OPEN"<br>For close long, side fill in "BUY"; tradeSide should be "CLOSE"<br>For close short, side fill in "SELL";tradeSide should be "CLOSE" |
| positionId | string | no | Position ID<br>Only required when "tradeSide" is "CLOSE" |
| orderType | string | yes | Order type<br>LIMIT: limit orders<br>MARKET: market orders |
| effect | string | no | Order expiration date.<br>Required if the orderType is limit<br>IOC: Immediate or cancel<br>FOK: Fill or kill<br>GTC: Good till canceled(default value)<br>POST_ONLY: POST only |
| clientId | string | no | Customize order ID |
| reduceOnly | boolean | no | Whether or not to just reduce the position |
| tpPrice | string | no | take profit trigger price |
| tpStopType | string | no | take profit trigger type<br>MARK_PRICE<br>LAST_PRICE |
| tpOrderType | string | no | take profit trigger place order type<br>LIMIT<br>MARKET |
| tpOrderPrice | string | no | take profit trigger place order price<br>LIMIT<br>MARKET<br>required if tpOrderType is LIMIT |
| slPrice | string | no | stop loss trigger price |
| slStopType | string | no | stop loss trigger type<br>MARK_PRICE<br>LAST_PRICE |
| slOrderType | string | no | stop loss trigger place order type<br>LIMIT<br>MARKET |
| slOrderPrice | string | no | stop loss trigger place order price<br>LIMIT<br>MARKET<br>required if slOrderType is LIMIT |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| successList | array | - | Successful order list |
| id | string | - | order id |
| clientId | string | - | client id |
| failureList | array | - | Failed order list |
| clientId | string | - | client id |
| errorMsg | string | - | error msg |
| errorCode | string | - | error code |

---

## Cancel All Orders

cancel all orders Successful interface response is not necessarily equal to the success of the operation, please use the websocket push message as an accurate judgment of the success of the operation.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | no | Trading pair |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| successList | array | - | Successful order list |
| id | string | - | order id |
| clientId | string | - | client id |
| failureList | array | - | Failed order list |
| id | string | - | order id |
| clientId | string | - | client id |
| errorMsg | string | - | error msg |
| errorCode | string | - | error code |

---

## Cancel Orders

Cancel orders Successful interface response is not necessarily equal to the success of the operation, please use the websocket push message as an accurate judgment of the success of the operation.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | Trading pair |
| orderList | array | yes | order parameter list |
| orderId | string | no | Order ID<br>Either orderId or clientId is required. If both are entered, orderId prevails. |
| clientId | string | no | Customize order ID<br>Either orderId or clientId is required. If both are entered, orderId prevails. |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| successList | array | - | Successful order list |
| id | string | - | order id |
| clientId | string | - | client id |
| failureList | array | - | Failed order list |
| id | string | - | order id |
| clientId | string | - | client id |
| errorMsg | string | - | error msg |
| errorCode | string | - | error code |

---

## Close All Position

Close all positions

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | no | Trading pair |

### Response Parameters

None — the official docs define no response fields for this endpoint.

---

## Flash Close Position

Close position by position id

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| positionId | string | yes | position id |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| positionId | string | - | Position ID |

---

## Get History Orders

get history orders, sort by create time desc

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | no | Trading pair |
| orderId | string | no | order id |
| clientId | string | no | client id |
| status | string | no | Order status<br>FILLED CANCELEDPART_FILLED_CANCELEDEXPIRED |
| type | string | no | Order type<br>LIMIT<br>MARKET default all |
| startTime | number | no | Start timestamp<br>Unix timestamp in milliseconds format, e.g. 1597026383085 |
| endTime | number | no | Start timestamp<br>Unix timestamp in milliseconds format, e.g. 1597026683085 |
| skip | number | no | skip order count default: 0 |
| limit | number | no | Number of queries: Maximum: 100, default: 10 |
| subAccountId | number | no | With subAccountUid: returns historical orders for that sub-account only.<br>Without subAccountUid: returns historical orders for the main account. |
| queryCanceled | boolean | no | Whether to query canceled orders only. default: false<br>true: return canceled orders only, query range limited to the last 3 days<br>false: exclude canceled orders, query range limited to the last 90 days |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| orderList | array | - | order list |
| orderId | string | - | order id |
| symbol | string | - | Trading pair |
| qty | string | - | Amount (base coin) |
| tradeQty | string | - | Fill amount (base coin) |
| positionMode | string | - | ONE_WAY or HEDGE |
| marginMode | string | - | ISOLATION or CROSS |
| leverage | number | - | leverage |
| price | string | - | Price of the order.<br>Required if the order type is LIMIT |
| side | string | - | Order direction<br>buy: BUY<br>sell: SELL |
| orderType | string | - | Order type<br>LIMIT: limit orders<br>MARKET: market orders |
| effect | string | - | Order expiration date.<br>Required if the orderType is limit<br>IOC: Immediate or cancel<br>FOK: Fill or kill<br>GTC: Good till canceled(default value)<br>POST_ONLY: POST only |
| clientId | string | - | Customize order ID |
| reduceOnly | boolean | - | Whether or not to just reduce the position |
| status | string | - | INIT:prepare status<br>NEW:pending<br>PART_FILLED:partially filled<br>CANCELED:canceled<br>FILLEDAll filled |
| fee | string | - | fee |
| realizedPNL | string | - | realized pnl |
| tpPrice | string | - | take profit trigger price |
| tpStopType | string | - | take profit trigger type<br>MARK_PRICE<br>LAST_PRICE |
| tpOrderType | string | - | take profit trigger place order type<br>LIMIT<br>MARKET |
| tpOrderPrice | string | - | take profit trigger place order price<br>LIMIT<br>MARKET<br>required if tpOrderType is LIMIT |
| slPrice | string | - | stop loss trigger price |
| slStopType | string | - | stop loss trigger type<br>MARK_PRICE<br>LAST_PRICE |
| slOrderType | string | - | stop loss trigger place order type<br>LIMIT<br>MARKET |
| slOrderPrice | string | - | stop loss trigger place order price<br>LIMIT<br>MARKET<br>required if slOrderType is LIMIT |
| ctime | number | - | create timestamp |
| mtime | number | - | latest modify timestamp |
| subAccountId | number | - | order account id |
| total | number | - | total count |

---

## Get History Trades

get history trades, sort by create time desc

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | no | Trading pair |
| orderId | string | no | order id |
| positionId | string | no | position id |
| startTime | number | no | Start timestamp<br>Unix timestamp in milliseconds format, e.g. 1597026383085 |
| endTime | number | no | Start timestamp<br>Unix timestamp in milliseconds format, e.g. 1597026683085 |
| skip | number | no | skip order count default: 0 |
| limit | number | no | Number of queries: Maximum: 100, default: 10 |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| tradeList | array | - | trade list |
| tradeId | string | - | trade id |
| orderId | string | - | order id |
| symbol | string | - | Trading pair |
| qty | string | - | Amount (base coin) |
| positionMode | string | - | ONE_WAY or HEDGE |
| marginMode | string | - | ISOLATION or CROSS |
| leverage | number | - | leverage |
| price | string | - | Price of the order.<br>Required if the order type is LIMIT |
| side | string | - | Order direction<br>buy: BUY<br>sell: SELL |
| orderType | string | - | Order type<br>LIMIT: limit orders<br>MARKET: market orders |
| effect | string | - | Order expiration date.<br>Required if the orderType is limit<br>IOC: Immediate or cancel<br>FOK: Fill or kill<br>GTC: Good till canceled(default value)<br>POST_ONLY: POST only |
| clientId | string | - | Customize order ID |
| reduceOnly | boolean | - | Whether or not to just reduce the position |
| fee | string | - | fee |
| realizedPNL | string | - | realized pnl |
| ctime | number | - | create timestamp |
| roleType | string | - | Trader tag<br>TAKER: maker<br>MAKER: maker |
| total | number | - | total count |

---

## Get Order Detail

get Order Detail

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| orderId | string | no | order idAt least one of orderId or clientId is required. |
| clientId | string | no | client idAt least one of orderId or clientId is required. |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| orderId | string | - | order id |
| symbol | string | - | Trading pair |
| qty | string | - | Amount (base coin) |
| tradeQty | string | - | Fill amount (base coin) |
| positionMode | string | - | ONE_WAY or HEDGE |
| marginMode | string | - | ISOLATION or CROSS |
| leverage | number | - | leverage |
| price | string | - | Price of the order.<br>Required if the order type is LIMIT |
| side | string | - | Order direction<br>buy: BUY<br>sell: SELL |
| orderType | string | - | Order type<br>LIMIT: limit orders<br>MARKET: market orders |
| effect | string | - | Order expiration date.<br>Required if the orderType is limit<br>IOC: Immediate or cancel<br>FOK: Fill or kill<br>GTC: Good till canceled(default value)<br>POST_ONLY: POST only |
| clientId | string | - | Customize order ID |
| reduceOnly | boolean | - | Whether or not to just reduce the position |
| status | string | - | INIT:prepare status<br>NEW:pending<br>PART_FILLED:partially filled<br>CANCELED:canceled<br>FILLEDAll filled |
| fee | string | - | fee |
| realizedPNL | string | - | realized pnl |
| tpPrice | string | - | take profit trigger price |
| tpStopType | string | - | take profit trigger type<br>MARK_PRICE<br>LAST_PRICE |
| tpOrderType | string | - | take profit trigger place order type<br>LIMIT<br>MARKET |
| tpOrderPrice | string | - | take profit trigger place order price<br>LIMIT<br>MARKET<br>required if tpOrderType is LIMIT |
| slPrice | string | - | stop loss trigger price |
| slStopType | string | - | stop loss trigger type<br>MARK_PRICE<br>LAST_PRICE |
| slOrderType | string | - | stop loss trigger place order type<br>LIMIT<br>MARKET |
| slOrderPrice | string | - | stop loss trigger place order price<br>LIMIT<br>MARKET<br>required if slOrderType is LIMIT |
| ctime | number | - | create timestamp |
| mtime | number | - | latest modify timestamp |

---

## Get Pending Orders

get Pending orders, sort by create time desc

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | no | Trading pair |
| orderId | string | no | order id |
| clientId | string | no | client id |
| status | string | no | Order status<br>NEW or PART_FILLED |
| startTime | number | no | Start timestamp<br>Unix timestamp in milliseconds format, e.g. 1597026383085 |
| endTime | number | no | Start timestamp<br>Unix timestamp in milliseconds format, e.g. 1597026683085 |
| skip | number | no | skip order count default: 0 |
| limit | number | no | Number of queries: Maximum: 100, default: 10 |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| orderList | array | - | order list |
| orderId | string | - | order id |
| symbol | string | - | Trading pair |
| qty | string | - | Amount (base coin) |
| tradeQty | string | - | Fill amount (base coin) |
| positionMode | string | - | ONE_WAY or HEDGE |
| marginMode | string | - | ISOLATION or CROSS |
| leverage | number | - | leverage |
| price | string | - | Price of the order.<br>Required if the order type is LIMIT |
| side | string | - | Order direction<br>buy: BUY<br>sell: SELL |
| orderType | string | - | Order type<br>LIMIT: limit orders<br>MARKET: market orders |
| effect | string | - | Order expiration date.<br>Required if the orderType is limit<br>IOC: Immediate or cancel<br>FOK: Fill or kill<br>GTC: Good till canceled(default value)<br>POST_ONLY: POST only |
| clientId | string | - | Customize order ID |
| reduceOnly | boolean | - | Whether or not to just reduce the position |
| status | string | - | INIT:prepare status<br>NEW:pending<br>PART_FILLED:partially filled<br>CANCELED:canceled<br>FILLEDAll filled |
| fee | string | - | fee |
| realizedPNL | string | - | realized pnl |
| tpPrice | string | - | take profit trigger price |
| tpStopType | string | - | take profit trigger type<br>MARK_PRICE<br>LAST_PRICE |
| tpOrderType | string | - | take profit trigger place order type<br>LIMIT<br>MARKET |
| tpOrderPrice | string | - | take profit trigger place order price<br>LIMIT<br>MARKET<br>required if tpOrderType is LIMIT |
| slPrice | string | - | stop loss trigger price |
| slStopType | string | - | stop loss trigger type<br>MARK_PRICE<br>LAST_PRICE |
| slOrderType | string | - | stop loss trigger place order type<br>LIMIT<br>MARKET |
| slOrderPrice | string | - | stop loss trigger place order price<br>LIMIT<br>MARKET<br>required if slOrderType is LIMIT |
| ctime | number | - | create timestamp |
| mtime | number | - | latest modify timestamp |
| total | number | - | total count |

---

## Modify Order

Interface for order modification, used to modify an pending order, such as its TP/SL and/or price/qty.Attention!!Successful interface response is not necessarily equal to the success of the operation, please use the websocket push message as an accurate judgment of the success of the operation.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| orderId | string | no | Order ID<br>Either orderId or clientId is required. If both are entered, orderId prevails. |
| clientId | string | no | Customize order ID<br>Either orderId or clientId is required. If both are entered, orderId prevails. |
| qty | string | yes | Amount (base coin) |
| price | string | yes | Price of the order.<br>Required if the order type is LIMIT |
| tpPrice | string | no | take profit trigger price |
| tpStopType | string | no | take profit trigger type<br>MARK_PRICE<br>LAST_PRICE |
| tpOrderType | string | no | take profit trigger place order type<br>LIMIT<br>MARKET |
| tpOrderPrice | string | no | take profit trigger place order price<br>LIMIT<br>MARKET<br>required if tpOrderType is LIMIT |
| slPrice | string | no | stop loss trigger price |
| slStopType | string | no | stop loss trigger type<br>MARK_PRICE<br>LAST_PRICE |
| slOrderType | string | no | stop loss trigger place order type<br>LIMIT<br>MARKET |
| slOrderPrice | string | no | stop loss trigger place order price<br>LIMIT<br>MARKET<br>required if slOrderType is LIMIT |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| orderId | string | - | order id |
| clientId | string | - | client id |

---

## Place Order

Place order

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | Trading pair |
| qty | string | yes | Amount (base coin) |
| price | string | no | Price of the order.<br>Required if the order type is LIMIT |
| side | string | yes | Order direction<br>buy: BUY<br>sell: SELL |
| tradeSide | string | yes | Direction<br>Only required in hedge-mode<br>Open and Close Notes:<br>For open long, side fill in"BUY"; tradeSide should be "OPEN"<br>For open short, side fill in "SELL"; tradeSide should be "OPEN"<br>For close long, side fill in "BUY"; tradeSide should be "CLOSE"<br>For close short, side fill in "SELL";tradeSide should be "CLOSE" |
| positionId | string | no | Position ID<br>Only required when "tradeSide" is "CLOSE" |
| orderType | string | yes | Order type<br>LIMIT: limit orders<br>MARKET: market orders |
| effect | string | no | Order expiration date.<br>Required if the orderType is limit<br>IOC: Immediate or cancel<br>FOK: Fill or kill<br>GTC: Good till canceled(default value)<br>POST_ONLY: POST only |
| clientId | string | no | Customize order ID |
| reduceOnly | boolean | no | Whether or not to just reduce the position |
| tpPrice | string | no | take profit trigger price |
| tpStopType | string | no | take profit trigger type<br>MARK_PRICE<br>LAST_PRICE |
| tpOrderType | string | no | take profit trigger place order type<br>LIMIT<br>MARKET |
| tpOrderPrice | string | no | take profit trigger place order price<br>LIMIT<br>MARKET<br>required if tpOrderType is LIMIT |
| slPrice | string | no | stop loss trigger price |
| slStopType | string | no | stop loss trigger type<br>MARK_PRICE<br>LAST_PRICE |
| slOrderType | string | no | stop loss trigger place order type<br>LIMIT<br>MARKET |
| slOrderPrice | string | no | stop loss trigger place order price<br>LIMIT<br>MARKET<br>required if slOrderType is LIMIT |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| orderId | string | - | order id |
| clientId | string | - | client id |

---
