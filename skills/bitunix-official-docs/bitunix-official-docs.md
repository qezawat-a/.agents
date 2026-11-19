---
name: bitunix-official-docs
description: verify any Bitunix API call's parameters against the official docs
provider: Bitunix
---

# Bitunix API Endpoint Parameter Reference

Generated from official documentation on 2026-11-18T00:07:08Z. Base URL: `https://fapi.bitunix.com`. Source pages: 50.

Every section below lists an endpoint's HTTP method, path, rate limit, description, and every request / response / push parameter exactly as the official documentation defines it. Use it to verify any agent-generated code before you call the API: if a parameter name, type, or required-flag differs from this file, fix the code.

> Source: official docs. Parameter names, types, enum values, and required flags are taken verbatim; do not invent alternatives.

## Endpoint Index

| # | Endpoint | Type | Method | Path | Doc |
|---|---|---|---|---|---|
| 1 | Get Tickers | rest | GET | /api/v1/futures/market/tickers | [doc](https://www.bitunix.com/api-docs/futures/market/get_tickers.html) |
| 2 | Change Log | rest | GET | /api/v1/futures/market/kline | [doc](https://www.bitunix.com/api-docs/futures/log/change_log.html) |
| 3 | Adjust Position Margin | rest | POST | /api/v1/futures/account/adjust_position_margin | [doc](https://www.bitunix.com/api-docs/futures/account/adjust_position_margin.html) |
| 4 | Change Leverage | rest | POST | /api/v1/futures/account/change_leverage | [doc](https://www.bitunix.com/api-docs/futures/account/change_leverage.html) |
| 5 | Change Margin Mode | rest | POST | /api/v1/futures/account/change_margin_mode | [doc](https://www.bitunix.com/api-docs/futures/account/change_margin_mode.html) |
| 6 | Change Position Mode | rest | POST | /api/v1/futures/account/change_position_mode | [doc](https://www.bitunix.com/api-docs/futures/account/change_position_mode.html) |
| 7 | Get Leverage and Margin Mode | rest | GET | /api/v1/futures/account/get_leverage_margin_mode | [doc](https://www.bitunix.com/api-docs/futures/account/get_leverage_and_margin_mode.html) |
| 8 | Get Single Account | rest | GET | /api/v1/futures/account | [doc](https://www.bitunix.com/api-docs/futures/account/get_single_account.html) |
| 9 | Asset Query | rest | GET | /api/v1/cp/asset/query | [doc](https://www.bitunix.com/api-docs/futures/copyTrading/asset/asset_query.html) |
| 10 | Error Code | error_code | - | - | [doc](https://www.bitunix.com/api-docs/futures/ErrorCode/error_code.html) |
| 11 | Get Depth | rest | GET | /api/v1/futures/market/depth | [doc](https://www.bitunix.com/api-docs/futures/market/get_depth.html) |
| 12 | Get Funding Rate | rest | GET | /api/v1/futures/market/funding_rate/batch | [doc](https://www.bitunix.com/api-docs/futures/market/get_funding_rate_batch.html) |
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
| 38 | Websocket | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/prepare/WebSocket.html) |
| 39 | Balance Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/private/Balance%20Channel.html) |
| 40 | Order Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/private/Order%20Channel.html) |
| 41 | Position Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/private/Position%20Channel.html) |
| 42 | Tp Sl Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/private/Tp%20Sl%20Channel.html) |
| 43 | Depth Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/public/depth%20channel.html) |
| 44 | Kline Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/public/kline%20channel.html) |
| 45 | Marketprice Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/public/MarketPrice%20Channel.html) |
| 46 | Ticker Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/public/Ticker%20Channel.html) |
| 47 | Tickers Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/public/Tickers%20Channel.html) |
| 48 | Trade Channel | ws | - | - | [doc](https://www.bitunix.com/api-docs/futures/websocket/public/Trade%20Channel.html) |
| 49 | Explanation of the Order Units in Futures Trading | article | - | - | [doc](https://www.bitunix.com/hub/helpcenter/article/explanation-of-the-order-units-in-futures-trading?id=170) |
| 50 | Bitunix Futures｜4 TP &amp; SL Execution Methods | article | - | - | [doc](https://www.bitunix.com/hub/academy/essential-beginners-guide/futures-trading-guide/bitunix-futures-positions-guide-to-four-tp-sl-methods) |

## Endpoint Details

## Get Tickers

**Type:** rest &nbsp;·&nbsp; **Method:** `GET` &nbsp;·&nbsp; **Path:** `/api/v1/futures/market/tickers` | Rate limit: `10 req/sec/ip`

Interface is used to get future trading pair tickers.

Official doc: [https://www.bitunix.com/api-docs/futures/market/get_tickers.html](https://www.bitunix.com/api-docs/futures/market/get_tickers.html)


### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbols | string | no | Trading pairs, based on the symbolName, i.e. BTCUSDT,ETHUSDT,XRPUSDT |


### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | ? | Coin pair name i.e. BTCUSDT |
| markPrice | string | ? | mark price |
| lastPrice | string | ? | last price |
| open | string | ? | Entry price of the last 24 hours |
| last | string | ? | last price |
| quoteVol | string | ? | Trading volume of the coin(last 24 hours) |
| baseVol | string | ? | Trading volume of the last 24 hours |
| high | string | ? | 24h high |
| low | string | ? | 24h low |


### Push Parameters

_No parameters documented._


### Error Codes

_No parameters documented._


---

## Change Log

**Type:** rest &nbsp;·&nbsp; **Method:** `GET` &nbsp;·&nbsp; **Path:** `/api/v1/futures/market/kline` | Rate limit: `documentation under WebSocket Preparing for Access.`

This page records updates to the OpenAPI documentation.

Official doc: [https://www.bitunix.com/api-docs/futures/log/change_log.html](https://www.bitunix.com/api-docs/futures/log/change_log.html)


### Request Parameters

_No parameters documented._


### Response Parameters

_No parameters documented._


### Push Parameters

_No parameters documented._


### Error Codes

_No parameters documented._


---

## Adjust Position Margin

**Type:** rest &nbsp;·&nbsp; **Method:** `POST` &nbsp;·&nbsp; **Path:** `/api/v1/futures/account/adjust_position_margin` | Rate limit: `5 req/sec/uid`

Add or reduce the margin（only for isolated margin mode）

Official doc: [https://www.bitunix.com/api-docs/futures/account/adjust_position_margin.html](https://www.bitunix.com/api-docs/futures/account/adjust_position_margin.html)


### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | Trading pair |
| marginCoin | string | yes | Margin coin |
| amount | string | yes | Margin amount, positive means increase, and negative means decrease |
| side | string | no | Position side
LONG
SHORT
Either side or positionId required |
| positionId | string | no | Position id
Either side or positionId required |


### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| N/A | - | ? |  |


### Push Parameters

_No parameters documented._


### Error Codes

_No parameters documented._


---

## Change Leverage

**Type:** rest &nbsp;·&nbsp; **Method:** `POST` &nbsp;·&nbsp; **Path:** `/api/v1/futures/account/change_leverage` | Rate limit: `10 req/sec/uid`

Adjust the leverage on the given symbol

Official doc: [https://www.bitunix.com/api-docs/futures/account/change_leverage.html](https://www.bitunix.com/api-docs/futures/account/change_leverage.html)


### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| marginCoin | string | yes | Margin coin |
| symbol | string | yes | Trading pair |
| leverage | number | yes | Leverage |


### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| marginCoin | string | ? | Margin coin |
| symbol | string | ? | Trading pair |
| leverage | number | ? | Leverage |


### Push Parameters

_No parameters documented._


### Error Codes

_No parameters documented._


---

## Change Margin Mode

**Type:** rest &nbsp;·&nbsp; **Method:** `POST` &nbsp;·&nbsp; **Path:** `/api/v1/futures/account/change_margin_mode` | Rate limit: `10 req/sec/uid`

This interface cannot be used when the users have an open position or an order

Official doc: [https://www.bitunix.com/api-docs/futures/account/change_margin_mode.html](https://www.bitunix.com/api-docs/futures/account/change_margin_mode.html)


### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| marginMode | string | yes | Margin Mode
ISOLATION
CROSS |
| symbol | string | yes | Trading pair |
| marginCoin | string | yes | Margin coin |


### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| marginMode | string | ? | Margin Mode
ISOLATION
CROSS |
| symbol | string | ? | Trading pair |
| marginCoin | string | ? | Margin coin |


### Push Parameters

_No parameters documented._


### Error Codes

_No parameters documented._


---

## Change Position Mode

**Type:** rest &nbsp;·&nbsp; **Method:** `POST` &nbsp;·&nbsp; **Path:** `/api/v1/futures/account/change_position_mode` | Rate limit: `10 req/sec/uid`

Adjust the position mode between 'one way mode' and 'hedge mode'<br><br>If you want to change the user's position mode on all symbol contracts, you need to specify hedge mode positions or one-way positions. Note: The position mode can't be adjusted when there is an open position order under the product type. Changes the user's position mode for all symbol futures: hedging mode or one-way mode.When users hold positions or orders on any side of any trading pair in the specific product type, the request may fail.

Official doc: [https://www.bitunix.com/api-docs/futures/account/change_position_mode.html](https://www.bitunix.com/api-docs/futures/account/change_position_mode.html)


### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| positionMode | string | yes | Position Mode
ONE_WAY
HEDGE |


### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| positionMode | string | ? | Position Mode
ONE_WAY
HEDGE |


### Push Parameters

_No parameters documented._


### Error Codes

_No parameters documented._


---

## Get Leverage and Margin Mode

**Type:** rest &nbsp;·&nbsp; **Method:** `GET` &nbsp;·&nbsp; **Path:** `/api/v1/futures/account/get_leverage_margin_mode` | Rate limit: `10 req/sec/uid`

get Leverage and Margin Mode

Official doc: [https://www.bitunix.com/api-docs/futures/account/get_leverage_and_margin_mode.html](https://www.bitunix.com/api-docs/futures/account/get_leverage_and_margin_mode.html)


### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | Trading pair |
| marginCoin | string | yes | Margin coin |


### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | ? | Trading pair |
| marginCoin | string | ? | Margin coin |
| leverage | number | ? | leverage |
| marginMode | string | ? | ISOLATION or CROSS |


### Push Parameters

_No parameters documented._


### Error Codes

_No parameters documented._


---

## Get Single Account

**Type:** rest &nbsp;·&nbsp; **Method:** `GET` &nbsp;·&nbsp; **Path:** `/api/v1/futures/account` | Rate limit: `10 req/sec/uid`

Get account details with the given 'marginCoin'

Official doc: [https://www.bitunix.com/api-docs/futures/account/get_single_account.html](https://www.bitunix.com/api-docs/futures/account/get_single_account.html)


### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| marginCoin | string | yes | Margin coin |


### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| marginCoin | string | ? | Margin Coin |
| available | string | ? | Available quantity in the account.
This field + crossUnrealizedPNL = Actual maximum open amount |
| frozen | string | ? | locked quantity of orders |
| margin | string | ? | locked quantity of positions |
| transfer | string | ? | Maximum transferable amount |
| positionMode | string | ? | Position mode
ONE_WAY
HEDGE |
| crossUnrealizedPNL | string | ? | unrealizedPNL for cross positions |
| isolationUnrealizedPNL | string | ? | unrealizedPNL for isolation positions |
| bonus | string | ? | Futures Bonus |


### Push Parameters

_No parameters documented._


### Error Codes

_No parameters documented._


---

## Asset Query

**Type:** rest &nbsp;·&nbsp; **Method:** `GET` &nbsp;·&nbsp; **Path:** `/api/v1/cp/asset/query` | Rate limit: `10 req/sec/uid`

Interface is used to asset query.

Official doc: [https://www.bitunix.com/api-docs/futures/copyTrading/asset/asset_query.html](https://www.bitunix.com/api-docs/futures/copyTrading/asset/asset_query.html)


### Request Parameters

_No parameters documented._


### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| available | string | ? | Futures available |
| maxTransfer | string | ? | Maximum transfer amount |


### Push Parameters

_No parameters documented._


### Error Codes

_No parameters documented._


---

## Error Code

**Type:** error_code &nbsp;·&nbsp; **Method:** `-` &nbsp;·&nbsp; **Path:** `-`
Official doc: [https://www.bitunix.com/api-docs/futures/ErrorCode/error_code.html](https://www.bitunix.com/api-docs/futures/ErrorCode/error_code.html)


### Request Parameters

_No parameters documented._


### Response Parameters

_No parameters documented._


### Push Parameters

_No parameters documented._


### Error Codes

| Parameter | Type | Required | Description |
|---|---|---|---|
| 0 | - | ? | Success |
| 403 | - | ? | This API key does not support this operation |
| 10001 | - | ? | Network Error |
| 10002 | - | ? | Parameter Error |
| 10003 | - | ? | api-key can't be empty |
| 10004 | - | ? | The current ip is not in the apikey ip whitelist |
| 10005 | - | ? | Too many requests, please try again later |
| 10006 | - | ? | Request too frequently |
| 10007 | - | ? | Sign signature error |
| 10008 | - | ? | {value} does not comply with the rule, optional [correctValue] |
| 10009 | - | ? | Another order operation is in progress, please try again shortly |
| 10010 | - | ? | Nonce's length must be less than 64 |
| 10011 | - | ? | The request timestamp must be within 60,000 ms of the server time. |
| 20001 | - | ? | Market not exists |
| 20002 | - | ? | The current positions amount has exceeded the maximum open limit, please adjust the risk limit |
| 20003 | - | ? | Insufficient balance |
| 20004 | - | ? | Insufficient Trader |
| 20005 | - | ? | Invalid leverage |
| 20006 | - | ? | You can't change leverage or margin mode as there are open orders |
| 20007 | - | ? | Order not found, please try it later |
| 20008 | - | ? | Insufficient amount |
| 20009 | - | ? | Position exists, so positions mode cannot be updated |
| 20010 | - | ? | Activation failed, the available balance in the futures account does not meet the conditions for activation of the coupon |
| 20011 | - | ? | Account not allowed to trade |
| 20012 | - | ? | This futures does not allow trading |
| 20013 | - | ? | Function disabled due tp pending account deletion request |
| 20014 | - | ? | Account deleted |
| 20015 | - | ? | This futures is not supported |
| 20016 | - | ? | Batch order exceeded the max size |
| 30001 | - | ? | Failed to order. Please adjust the order price or the leverage as the order price dealt may immediately liquidate. |
| 30002 | - | ? | Price below liquidated price |
| 30003 | - | ? | Price above liquidated price |
| 30004 | - | ? | Position not exist |
| 30005 | - | ? | The trigger price i
