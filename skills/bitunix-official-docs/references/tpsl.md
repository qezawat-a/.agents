# TP/SL Endpoints

Part of the Bitunix Futures API reference. Conventions, signing, the endpoint index and the WebSocket guide live in `SKILL.md`.

## Cancel TP/SL Order

Cancel TP/SL Order Successful interface response is not necessarily equal to the success of the operation, please use the websocket push message as an accurate judgment of the success of the operation.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | coin Pair |
| orderId | string | yes | TP/SL Order ID |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| orderId | string | - | TP/SL Order ID |

---

## Get History TP/SL Order

Get History TP/SL Order

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | no | Trading pair |
| side | int32 | no | order side |
| positionMode | int32 | no | order position mode |
| startTime | number | no | Start timestamp<br>Unix timestamp in milliseconds format, e.g. 1597026383085 |
| endTime | number | no | Start timestamp<br>Unix timestamp in milliseconds format, e.g. 1597026683085 |
| skip | number | no | skip order count default: 0 |
| limit | number | no | Number of queries: Maximum: 100, default: 10 |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| orderList | array | - | TP/SL order List |
| id | string | - | order id |
| positionId | string | - | position id |
| symbol | string | - | coin pair |
| base | string | - | base |
| quote | string | - | quote |
| tpPrice | string | - | Take-profit trigger price |
| tpStopType | string | - | Take-profit trigger type<br>LAST_PRICE<br>MARK_PRICE |
| slPrice | string | - | Stop-loss trigger price |
| slStopType | string | - | Stop-loss trigger type<br>LAST_PRICE<br>MARK_PRICE |
| tpOrderType | string | - | Take-profit order type<br>LIMIT<br>MARKET<br>Default is market. |
| tpOrderPrice | string | - | Take-profit order price |
| slOrderType | string | - | Stop-loss order type<br>LIMIT<br>MARKET<br>Default is market. |
| slOrderPrice | string | - | Stop-loss order price |
| tpQty | string | - | Take-profit order quantity(base coin)<br>At least one of tpQty or slQty is required. |
| slQty | string | - | Stop-loss order quantity(base coin)<br>At least one of tpQty or slQty is required. |
| status | string | - | TP/SL order status |
| ctime | number | - | create timestamp |
| triggerTime | number | - | trigger time timestamp |
| total | number | - | total |

---

## Get Pending TP/SL Order

Get Pending TP/SL Order

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | no | Trading pair |
| positionId | string | no | position id |
| side | int32 | no | order side |
| positionMode | int32 | no | order position mode |
| skip | number | no | skip order count default: 0 |
| limit | number | no | Number of queries: Maximum: 100, default: 10 |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| id | string | - | order id |
| positionId | string | - | position id |
| symbol | string | - | coin pair |
| base | string | - | base |
| quote | string | - | quote |
| tpPrice | string | - | Take-profit trigger price |
| tpStopType | string | - | Take-profit trigger type<br>LAST_PRICE<br>MARK_PRICE |
| slPrice | string | - | Stop-loss trigger price |
| slStopType | string | - | Stop-loss trigger type<br>LAST_PRICE<br>MARK_PRICE |
| tpOrderType | string | - | Take-profit order type<br>LIMIT<br>MARKET<br>Default is market. |
| tpOrderPrice | string | - | Take-profit order price |
| slOrderType | string | - | Stop-loss order type<br>LIMIT<br>MARKET<br>Default is market. |
| slOrderPrice | string | - | Stop-loss order price |
| tpQty | string | - | Take-profit order quantity(base coin)<br>At least one of tpQty or slQty is required. |
| slQty | string | - | Stop-loss order quantity(base coin)<br>At least one of tpQty or slQty is required. |

---

## Modify Position TP/SL Order

Modify Position TP/SL Order

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | Trading pair |
| positionId | string | yes | Position ID associated with take-profit and stop-loss |
| tpPrice | string | no | Take-profit trigger price<br>At least one of tpPrice or slPrice is required. |
| tpStopType | string | no | Take-profit trigger type<br>LAST_PRICE<br>MARK_PRICE<br>Default is market price. |
| slPrice | string | no | Stop-loss trigger price<br>At least one of tpPrice or slPrice is required. |
| slStopType | string | no | Stop-loss trigger type<br>LAST_PRICE<br>MARK_PRICE<br>Default is market price. |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| orderId | string | - | TP/SL Order ID |

---

## Modify TP/SL Order

Modify TP/SL Order

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| orderId | string | yes | TP/SL Order ID |
| tpPrice | string | no | Take-profit trigger price<br>At least one of tpPrice or slPrice is required. |
| tpStopType | string | no | Take-profit trigger type<br>LAST_PRICE<br>MARK_PRICE<br>Default is market price. |
| slPrice | string | no | Stop-loss trigger price<br>At least one of tpPrice or slPrice is required. |
| slStopType | string | no | Stop-loss trigger type<br>LAST_PRICE<br>MARK_PRICE<br>Default is market price. |
| tpOrderType | string | no | Take-profit order type<br>LIMIT<br>MARKET<br>Default is market. |
| tpOrderPrice | string | no | Take-profit order price |
| slOrderType | string | no | Stop-loss order type<br>LIMIT<br>MARKET<br>Default is market. |
| slOrderPrice | string | no | Stop-loss order price |
| tpQty | string | no | Take-profit order quantity(base coin)<br>At least one of tpQty or slQty is required. |
| slQty | string | no | Stop-loss order quantity(base coin)<br>At least one of tpQty or slQty is required. |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| orderId | string | - | TP/SL Order ID |

---

## Place Position TP/SL Order

Place Position TP/SL OrderWhen triggered, it will close the position at market price based on the position quantity at that time.Each position can only have one Position TP/SL Order

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | Trading pair |
| positionId | string | yes | Position ID associated with take-profit and stop-loss |
| tpPrice | string | no | Take-profit trigger price<br>At least one of tpPrice or slPrice is required. |
| tpStopType | string | no | Take-profit trigger type<br>LAST_PRICE<br>MARK_PRICE<br>Default is market price. |
| slPrice | string | no | Stop-loss trigger price<br>At least one of tpPrice or slPrice is required. |
| slStopType | string | no | Stop-loss trigger type<br>LAST_PRICE<br>MARK_PRICE<br>Default is market price. |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| orderId | string | - | TP/SL Order ID |

---

## Place TP/SL Order

Place TP/SL Order

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | Trading pair |
| positionId | string | yes | Position ID associated with take-profit and stop-loss |
| tpPrice | string | no | Take-profit trigger price<br>At least one of tpPrice or slPrice is required. |
| tpStopType | string | no | Take-profit trigger type<br>LAST_PRICE<br>MARK_PRICE<br>Default is market price. |
| slPrice | string | no | Stop-loss trigger price<br>At least one of tpPrice or slPrice is required. |
| slStopType | string | no | Stop-loss trigger type<br>LAST_PRICE<br>MARK_PRICE<br>Default is market price. |
| tpOrderType | string | no | Take-profit order type<br>LIMIT<br>MARKET<br>Default is market. |
| tpOrderPrice | string | no | Take-profit order price |
| slOrderType | string | no | Stop-loss order type<br>LIMIT<br>MARKET<br>Default is market. |
| slOrderPrice | string | no | Stop-loss order price |
| tpQty | string | no | Take-profit order quantity(base coin)<br>At least one of tpQty or slQty is required. |
| slQty | string | no | Stop-loss order quantity(base coin)<br>At least one of tpQty or slQty is required. |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| orderId | string | - | TP/SL Order ID |

---
