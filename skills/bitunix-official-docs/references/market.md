# Market Data Endpoints

Part of the Bitunix Futures API reference. Conventions, signing, the endpoint index and the WebSocket guide live in `SKILL.md`.

## Get Tickers

Interface is used to get future trading pair tickers.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbols | string | no | Trading pairs, based on the symbolName, i.e. BTCUSDT,ETHUSDT,XRPUSDT |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | - | Coin pair name i.e. BTCUSDT |
| markPrice | string | - | mark price |
| lastPrice | string | - | last price |
| open | string | - | Entry price of the last 24 hours |
| last | string | - | last price |
| quoteVol | string | - | Trading volume of the coin(last 24 hours) |
| baseVol | string | - | Trading volume of the last 24 hours |
| high | string | - | 24h high |
| low | string | - | 24h low |

---

## Get Depth

Interface is used to get future order book.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | Trading pair, based on the symbolName, i.e. BTCUSDT |
| limit | string | no | Fixed gear enumeration value: 1/5/15/50/max, passing max returns the maximum gear of the trading pairWhen the actual depth does not meet the limit, return according to the actual gear . If max is passed in, the maximum level of the trading pair will be returned. |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| asks.index[0] | string | - | ask price |
| asks.index[1] | string | - | ask amount |
| bids.index[0] | string | - | bid price |
| bids.index[1] | string | - | bid amount |

---

## Get Funding Rate Batch

Get the current funding rate of the contract

### Request Parameters

None — this endpoint takes no request parameters.

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | - | Coin pair |
| markPrice | decimal | - | mark price |
| lastPrice | decimal | - | last price |
| indexPrice | decimal | - | index price |
| fundingRate | decimal | - | Current funding rates |
| nextFundingTime | number | - | next Funding settlement time(ms) |
| fundingInterval | int32 | - | funding settlement interval(hour) |
| maxFundingRate | decimal | - | Max Current Funding Rate |
| minFundingRate | decimal | - | Min Current Funding Rate |

---

## Get Funding Rate History

Get the history funding rate of the contract

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | Trading pair, based on the symbolName, i.e. BTCUSDT |
| startTime | number | no | Start timestamp(Funding settle time)<br>Unix timestamp in milliseconds format, e.g. 1597026383085 |
| endTime | number | no | End timestamp(Funding settle time)<br>Unix timestamp in milliseconds format, e.g. 1597026383085 |
| limit | int32 | no | Default: 100,Maximum: 200 |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| markPrice | string | - | Mark price |
| fundingRate | string | - | Funding rate |
| fundingTime | number | - | Funding timestamp |

---

## Get Funding Rate

Get the current funding rate of the contract

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | Trading pair, based on the symbolName, i.e. BTCUSDT |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | - | Coin pair |
| markPrice | decimal | - | mark price |
| lastPrice | decimal | - | last price |
| indexPrice | decimal | - | index price |
| fundingRate | decimal | - | Current funding rates |
| nextFundingTime | number | - | next Funding settlement time(ms) |
| fundingInterval | int32 | - | funding settlement interval(hour) |
| maxFundingRate | decimal | - | Max Current Funding Rate |
| minFundingRate | decimal | - | Min Current Funding Rate |

---

## Get Kline

Interface is used to get future kline history.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | yes | Trading pair, based on the symbolName, i.e. BTCUSDT |
| endTime | number | no | Exclusive end bound. Query limit klines before this time. Unix timestamp in milliseconds, e.g. 1672410000000. Best practice: align to the interval open time. If omitted, the current forming candle open time is used |
| interval | string | yes | kline interval such as 1m 5m 15m 30m 1h 2h 4h 6h 8h 12h 1d 3d 1w 1M |
| limit | number | no | Number of klines to return, counting backward from endTime. Default: 100, maximum: 200 |
| type | string | no | Kline type, values: LAST_PRICE, MARK_PRICE; default: LAST_PRICE |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| open | string | - | open price |
| high | string | - | high price |
| low | string | - | low price |
| close | string | - | close price |
| quoteVol | string | - | Trading amount (quote currency turnover) for the kline period |
| baseVol | string | - | Trading volume (base coin) for the kline period |
| time | number | - | Candle open time, Unix timestamp in milliseconds. This is the open time, not the close time. Only closed candles are returned; the candle that is still forming is not included. |

---

## Get Trading Pairs

Interface is used to get future trading pair details.

### Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbols | string | no | Trading pairs, based on the symbolName, i.e. BTCUSDT,ETHUSDT,XRPUSDT |

### Response Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| symbol | string | - | Coin pair name i.e. BTCUSDT |
| base | string | - | Base currency Specifically refers to ETH as in ETHUSDT |
| quote | string | - | Base currency Specifically refers to USDT as in ETHUSDT |
| minTradeVolume | string | - | Minimum opening amount (base currency) |
| minBuyPriceOffset | string | - | Minimum price offset for buy orders |
| maxSellPriceOffset | string | - | Maximum price offset for sell orders |
| maxLimitOrderVolume | string | - | Maximum limit order base amount |
| maxMarketOrderVolume | string | - | Maximum market order base amount |
| basePrecision | number | - | Max precision of opening amount |
| quotePrecision | number | - | Max precision of order price |
| maxLeverage | number | - | Max leverage |
| minLeverage | number | - | Min leverage |
| defaultLeverage | number | - | Default Leverage |
| defaultMarginMode | string | - | Default margin mode Isolation Cross |
| priceProtectScope | string | - | Price protection scope.<br>For example: current mark price is:10000 priceProtectScope=0.02, the minimum sell order price = 10000*(1-0.02)=9800; the maximum buy order price = 10000*(1+0.02) = 10200 |
| symbolStatus | string | - | OPEN: trade normal CANCEL_ONLY: cancel only STOP: can't open/close position |
| isApiSupported | boolean | - | true: API Trading Enabled false: API Trading Disabled |
| maxFundingRate | decimal | - | Max Current Funding Rate |
| minFundingRate | decimal | - | Min Current Funding Rate |
| launchTime | long | - | Contract launch time. Unix timestamp in milliseconds (UTC). null: uptime not configured |
| delistTime | long | - | Scheduled contract delisting time. Unix timestamp in milliseconds (UTC). Omitted: delisting time not configured or cleared |

---
