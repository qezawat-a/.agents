# Bitunix Liquidation Mechanism

## Maintenance Margin Rate (MMR) Tiers

Position maintenance margin rates vary by notional value. Symbols have tier brackets where higher notional positions have lower MMR (leverage scaling).

### Getting Tiers
`GET /api/v1/futures/position/get_position_tiers?symbol=BTCUSDT`

Response:
```json
[
  {
    "level": 1,
    "startValue": "0",
    "endValue": "100000",
    "leverage": 50,
    "maintenanceMarginRate": "0.005"
  },
  ...
]
```

---

## Liquidation Price Formula

### Isolated Margin Mode

**Long Position:**
```
Liquidation Price = Entry × (1 - 1/Leverage + MMR)
```

**Short Position:**
```
Liquidation Price = Entry × (1 + 1/Leverage - MMR)
```

Where:
- `Entry` = position entry price
- `Leverage` = position leverage (clamped to tier ceiling)
- `MMR` = maintenance margin rate for position size tier

---

### Cross Margin Mode

Cross margin has additional risk as losses can exceed isolated margin. The liquidation mechanics are more complex and typically involve:

1. Position-level liquidation first
2. Cross-margin deficit liquidation if needed

---

## Position Tier Clamping

### Leverate Limits by Position Size

Each symbol has leverage limits based on position notional (size × price):

| Notional Range | Max Leverage |
|----------------|--------------|
| $0 - $10K | 50x-125x (symbol dependent) |
| $10K - $50K | 40x-100x |
| $50K - $100K | 20x-50x |
| $100K+ | 10x-25x |

**Implementation:** Check `tierFor()` before placing orders. The exchange will auto-clamp, but we should pre-validate.

---

## Stop Loss Safety Margin

### Fee-Band Floor

Each order incurs taker fees. Before placing a stop, verify:

```
Stop Distance >= 2 × Fee Band
```

Where Fee Band = `price × fee_rate`

Typically: 0.025% taker fee → Fee Band at $50,000 BTC ≈ $12.50

### ATR Stop Within Liquidation

For a long position:
```
Stop Must Be > Entry - (Entry × (1/Leverage + MMR))
```

Or equivalently:
```
Stop Must Be < LiqPrice + (Stop Distance for slippage)
```

### Safe Leverage Ceiling

Given Entry, Stop, and MMR:
```
Safe Leverage = 1 / (1 - Stop/Entry + MMR)
```

If configured leverage > safe ceiling → REFUSE trade (don't auto de-lever)

---

## Partial Fills & Liquidation Tracking

### Order Status: PART_FILLED_CANCELED

This IS a liquidation event:
- Order was partially filled
- Remainder was canceled due to margin/risk
- The filled portion may have been liquidated

### Position liqPrice Updates

- `liqPrice` in position data is an estimate
- Real-time updates via WebSocket position channel
- After partial fills, liqPrice may shift due to new MMR tier

---

## Liquidation Prevention Rules

1. **Stop distance check**: Stop must be inside liquidation distance
2. **Fee band floor**: Stop must be at least 2× fee away from entry
3. **Leverage consistency**: Can't exceed tier ceiling
4. **Position mode**: HEDGE mode requires tracking long/short separately

---

## Debug Checklist for Liquidation Issues

- [ ] Verify MMR from tier data, not static value
- [ ] Check position notional for tier clamping
- [ ] Confirm leverage is held, not changed mid-trade
- [ ] Validate stop is inside liq distance at configured leverage
- [ ] Account for fee-band in stop sizing
- [ ] PART_FILLED_CANCELED = real fill, not error

---

## Example Calculation

**Symbol:** BTCUSDT
**Entry:** $50,000
**Position Size:** 0.5 BTC (Notional: $25,000)
**Leverage:** 20x
**MMR:** 0.25% (0.0025)

```
Liquidation Price = 50000 × (1 - 1/20 + 0.0025)
                  = 50000 × (1 - 0.05 + 0.0025)
                  = 50000 × 0.9525
                  = $47,625

Stop at $49,000 would be liquidated (stop > liq)
Stop at $47,000 is safe
```

Safe leverage for stop at $47,000:
```
Safe Lev = 1 / (1 - 47000/50000 + 0.0025)
         = 1 / (1 - 0.06 + 0.0025)
         = 1 / 0.9425
         = 10.6x
```

So at 20x leverage with this stop, liquidation would occur first.