# Position Endpoints

Part of the Bitunix Futures API reference. Conventions, signing, the endpoint index and the WebSocket guide live in `SKILL.md`.

## Get History Positions

Get History Positions

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | no | Trading pair |
| positionId | string | no | position id |
| startTime | number | no | Start timestamp(position create time)<br>Unix timestamp in milliseconds format, e.g. 1597026383085 |
| endTime | number | no | Start timestamp(position create time)<br>Unix timestamp in milliseconds format, e.g. 1597026683085 |
| skip | number | no | skip order count default: 0 |
| limit | number | no | Number of queries: Maximum: 100, default: 10 |
| subAccountId | number | no | With subAccountUid: returns historical positions for that sub-account only.<br>Without subAccountUid: returns historical positions for the main account. |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| positionList | array | - | position list |
| positionId | string | - | position id |
| symbol | string | - | Trading pair |
| maxQty | string | - | max position amount |
| entryPrice | string | - | average entry price |
| closePrice | string | - | average close price |
| liqQty | string | - | liquidate quantity |
| side | string | - | LONG SHORT |
| marginMode | string | - | ISOLATION CROSS |
| positionMode | string | - | ONE_WAY HEDGE |
| leverage | int32 | - | leverage |
| fee | string | - | Deducted transaction fees: transaction fees deducted during the position |
| funding | string | - | total funding fee during the position |
| realizedPNL | string | - | Realized PnL(exclude funding fee and transaction fee) |
| liqPrice | string | - | Estimated liquidation price<br>If the value &lt;= 0, it means the position is at low risk and there is no liquidation price at this time |
| ctime | number | - | create timestamp |
| mtime | number | - | latest modify timestamp |
| subAccountId | number | - | position account id |
| total | number | - | total count |

---

## Get Pending Positions

Get Pending Positions

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | no | Trading pair |
| positionId | string | no | position id |
| subAccountId | number | no | With subAccountUid: returns positions for that sub-account only. Without subAccountUid:returns positions for the main account and all sub-accounts the current API Key can access. |
| includeSubAccounts | boolean | no | enable or disable sub-account query |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| positionId | string | - | position id |
| symbol | string | - | Trading pair |
| qty | string | - | position amount |
| entryValue | string | - | Available amount for positions |
| side | string | - | LONG SHORT |
| marginMode | string | - | ISOLATION CROSS |
| positionMode | string | - | ONE_WAY HEDGE |
| leverage | int32 | - | leverage |
| fee | string | - | Deducted transaction fees: transaction fees deducted during the position |
| funding | string | - | total funding fee during the position |
| realizedPNL | string | - | Realized PnL(exclude funding fee and transaction fee) |
| margin | string | - | locked asset of the position |
| unrealizedPNL | string | - | Unrealized PnL |
| liqPrice | string | - | Estimated liquidation price<br>If the value &lt;= 0, it means the position is at low risk and there is no liquidation price at this time |
| marginRate | string | - | Margin ratio |
| avgOpenPrice | string | - | Average open price |
| ctime | number | - | create timestamp |
| mtime | number | - | latest modify timestamp |
| subAccountId | number | - | position account id |

---

## Get Position Tiers

Get Position Tiers

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | Trading pair |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | - | Trading pair |
| level | int32 | - | level |
| startValue | string | - | Minimum value |
| endValue | string | - | Maximum value |
| leverage | int32 | - | leverage |
| maintenanceMarginRate | string | - | Maintenance margin rate: The margin amount corresponds to the position quantity tier. When the margin rate of a position is less than the maintenance margin rate, it will trigger a forced partial liquidation or full liquidation. |

---
