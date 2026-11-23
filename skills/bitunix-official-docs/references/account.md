# Account Endpoints

Part of the Bitunix Futures API reference. Conventions, signing, the endpoint index and the WebSocket guide live in `SKILL.md`.

## Adjust Position Margin

Add or reduce the margin（only for isolated margin mode）

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | Trading pair |
| marginCoin | string | yes | Margin coin |
| amount | string | yes | Margin amount, positive means increase, and negative means decrease |
| side | string | no | Position side<br>LONG<br>SHORT<br>Either side or positionId required |
| positionId | string | no | Position id<br>Either side or positionId required |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| N/A | - | - |  |

---

## Change Leverage

Adjust the leverage on the given symbol

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| marginCoin | string | yes | Margin coin |
| symbol | string | yes | Trading pair |
| leverage | number | yes | Leverage |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| marginCoin | string | - | Margin coin |
| symbol | string | - | Trading pair |
| leverage | number | - | Leverage |

---

## Change Margin Mode

This interface cannot be used when the users have an open position or an order

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| marginMode | string | yes | Margin Mode<br>ISOLATION<br>CROSS |
| symbol | string | yes | Trading pair |
| marginCoin | string | yes | Margin coin |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| marginMode | string | - | Margin Mode<br>ISOLATION<br>CROSS |
| symbol | string | - | Trading pair |
| marginCoin | string | - | Margin coin |

---

## Change Position Mode

Adjust the position mode between 'one way mode' and 'hedge mode'<br><br>If you want to change the user's position mode on all symbol contracts, you need to specify hedge mode positions or one-way positions. Note: The position mode can't be adjusted when there is an open position order under the product type. Changes the user's position mode for all symbol futures: hedging mode or one-way mode.When users hold positions or orders on any side of any trading pair in the specific product type, the request may fail.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| positionMode | string | yes | Position Mode<br>ONE_WAY<br>HEDGE |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| positionMode | string | - | Position Mode<br>ONE_WAY<br>HEDGE |

---

## Get Leverage and Margin Mode

get Leverage and Margin Mode

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | Trading pair |
| marginCoin | string | yes | Margin coin |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | - | Trading pair |
| marginCoin | string | - | Margin coin |
| leverage | number | - | leverage |
| marginMode | string | - | ISOLATION or CROSS |

---

## Get Single Account

Get account details with the given 'marginCoin'

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| marginCoin | string | yes | Margin coin |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| marginCoin | string | - | Margin Coin |
| available | string | - | Available quantity in the account.<br>This field + crossUnrealizedPNL = Actual maximum open amount |
| frozen | string | - | locked quantity of orders |
| margin | string | - | locked quantity of positions |
| transfer | string | - | Maximum transferable amount |
| positionMode | string | - | Position mode<br>ONE_WAY<br>HEDGE |
| crossUnrealizedPNL | string | - | unrealizedPNL for cross positions |
| isolationUnrealizedPNL | string | - | unrealizedPNL for isolation positions |
| bonus | string | - | Futures Bonus |

---

## Asset Query

Interface is used to asset query.

### Request Parameters

None — this endpoint takes no request parameters.

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| available | string | - | Futures available |
| maxTransfer | string | - | Maximum transfer amount |

---
