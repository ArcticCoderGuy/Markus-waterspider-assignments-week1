# Mikrobot Main Strategy - EURUSD Trend-Based Price Action (No MAs)

Author: Markus  
Date: Week 1  
Status: Draft v1 (for coding)

---

## 1. Goal & Scope
- Instrument: EURUSD
- Timeframes: H1 (bias), M5 (execution)
- Style: Market structure + price action (BOS  pullback  PA trigger)
- Objective: Production-ready rules for live trades by Friday

---

## 2. Assumptions & Constraints
- No moving averages. Pure structure and price action.
- Broker: IconFX/PUPrime via MT5 (market orders, SL/TP attached).
- Trading window: London + NY sessions (server time aligned, see Params).
- Max spread allowed: 1.2 pips (configurable).
- Risk per trade: 0.5% account balance.
- RR target: 2.0 (TP at 2R), optional partial at 1R.

---

## 3. UDM (Input  Process  Output)
- Input
  - Market data: EURUSD H1 & M5 OHLC, tick size/value, min lot/step, spread.
  - State: open positions, cooldown timestamps, intraday PnL.
  - Environment: session clock, optional news window (manual list for now).
- Process
  - Bias (H1): determine up/down/none via market structure (HH/HL vs LH/LL) and BOS.
  - Setup (M5): BOS in bias direction, then pullback to prior impulse zone or ~50% retrace.
  - Trigger (M5): engulfing or strong body close in zone, aligned with bias.
  - Risk: 0.5% risk sizing; SL beyond swing � ATR buffer; TP = 2R; optional partial at 1R and BE.
  - Filters: spread, session, one position per direction, cooldown after SL.
- Output
  - Order request: side (BUY/SELL), volume, price=market, SL, TP, tags (bias/setup/trigger IDs).
  - Logs and telemetry: decision path, parameters, results.

---

## 4. Definitions
- Swing High/Low (fractal=2):
  - Swing High: high[i] > high[i-1], high[i] > high[i-2], high[i] = high[i+1], high[i] = high[i+2].
  - Swing Low: inverse of above.
- BOS (Break of Structure): close beyond the most recent opposite swing (close > last swing high for bullish BOS; close < last swing low for bearish BOS).
- Impulse leg: the directional move that created the BOS.
- Zone (supply/demand): candle range prior to impulse that was violated by BOS; execution expects pullback to this zone or ~0.5 retracement of the impulse range.
- ATR buffer: buffer = 0.2 � ATR(14, M5) added beyond swing for SL.

---

## 5. Timeframe Logic
- Bias (H1):
  - Bullish if there is a clear bullish BOS and recent structure is HH/HL (last correction holds HL).
  - Bearish if there is a clear bearish BOS and recent structure is LH/LL (last correction holds LH).
  - If mixed/ranging (no clean BOS), bias = none  no trades.
- Execution (M5):
  - Trade only in bias direction.
  - Require M5 BOS in bias direction.
  - After BOS, wait for pullback into the identified zone or to ~50% of the impulse.

---

## 6. Entry Rules (M5)
- Long Entry:
  1) Bias = bullish (H1) and M5 shows bullish BOS.
  2) Price pulls back into demand zone (pre-impulse area) or to 50% of the impulse range.
  3) Trigger: bullish engulfing or strong bullish close (body = 60% of candle range) while inside zone.
  4) Spread = max_spread and session filter passes.
- Short Entry:
  1) Bias = bearish (H1) and M5 shows bearish BOS.
  2) Price pulls back into supply zone or to 50% of the impulse range.
  3) Trigger: bearish engulfing or strong bearish close (body = 60%).
  4) Spread = max_spread and session filter passes.

---

## 7. Stop, Target, and Management
- Stop Loss (SL):
  - Long: below last swing low of the pullback minus ATR buffer.
  - Short: above last swing high of the pullback plus ATR buffer.
- Take Profit (TP):
  - Initial TP at 2 � risk (2R) from entry.
- Management (optional, configurable):
  - At +1R: take 50% off and move SL to BE.
  - Trailing after +1R: trail behind new swings on M5.
- Early Exit:
  - If opposite-direction BOS occurs on M5 before reaching +1R, close at market.
  - Time-based: if trade sits > 90 minutes without reaching +0.5R, close at market.

---

## 8. Risk & Sizing
- Risk per trade: risk_pct = 0.005 (0.5%).
- Position size formula:
  - risk_amount = balance � risk_pct
  - stop_pips = abs(entry - SL) / pip_size
  - volume = risk_amount / (stop_pips � pip_value)
  - Normalize to broker min/max/step; reject if below min.
- Max concurrent positions per symbol per direction: 1.
- Cooldown after SL: 15 minutes for the symbol.

---

## 9. Filters & Safety
- Spread filter: current_spread = 1.2 pips.
- Session filter: trades only within allowed window (see Params).
- News filter: manual block list (30 min around high-impact events).
- Daily protection (optional): stop trading after daily loss = X%.
- Connectivity & symbol checks: ensure symbol selected, trading allowed, correct digits, stop levels respected.

---

## 10. State Machine
- IDLE  WAIT_BIAS (H1 ready)
- WAIT_BIAS  WAIT_SETUP (M5 BOS in bias direction)
- WAIT_SETUP  WAIT_TRIGGER (price pulls back into zone/50% area)
- WAIT_TRIGGER  PLACED (trigger candle meets rule, order sent)
- PLACED  MANAGED (SL/TP tracking, partials, trail)
- MANAGED  CLOSED (TP, SL, early exit, or time-based)
- After CLOSED: update cooldown if SL; go to WAIT_SETUP or WAIT_BIAS based on structure.

---

## 11. Parameters (Defaults)
- risk_pct: 0.005
- rr_target: 2.0
- partial_at_1R: true, partial_ratio: 0.5
- trail_after_1R: true
- atr_period: 14
- atr_buffer_mult: 0.2
- max_spread_pips: 1.2
- session_start: 08:00 (local/server-aligned)
- session_end: 20:00 (local/server-aligned)
- cooldown_minutes_after_SL: 15
- fractal_depth: 2
- time_close_minutes: 90

---

## 12. Pseudocode
H1 bias:
- compute swings (fractal_depth), determine last BOS and structure (HH/HL vs LH/LL)
- bias = up/down/none

M5 execution loop:
- if bias is none  continue
- detect BOS in bias direction
- define impulse leg and zone; calc 50% retrace
- wait for price to enter zone
- on candle close in zone, check trigger (engulfing or strong body in direction)
- compute SL beyond swing � ATR buffer
- compute risk_amount and volume; normalize; check spread/session/cooldown/open positions
- send market order with SL/TP (2R); log decision path and parameters
- manage trade: partial at 1R, move SL to BE, optional trail; early exit rules

---

## 13. Data & Logging
- Each decision logs: timestamp, bias state, BOS id, zone id, trigger candle id, spread, session, SL/TP, risk, volume, order result, errors.
- Trade metrics: win rate, avg R, profit factor, max drawdown, expectancy.

---

## 14. Testing & Validation Plan
- Unit tests: swing detection, BOS detection, zone mapping, trigger classification, sizing math (pip_value/tick_value).
- Dry-run test on historical M5 data: verify entries align with rules; no trades when bias=none.
- Live paper test: confirm spreads, sessions, stop-level constraints, and order placement.

---

## 15. Module Split (Implementation Plan)
- structure.py: swings, BOS, zone, trigger detection
- risk.py: risk sizing, broker normalization, SL/TP math
- broker_mt5.py: data fetch, symbol properties, order send, spread, sessions
- run_ea.py: orchestrator loop (H1 bias + M5 execution), logging

---

## 16. Future Enhancements
- News calendar integration (auto block windows)
- Multi-symbol expansion and portfolio risk cap
- Advanced zone scoring and confluence (e.g., higher TF zones)
- Robust persistence for state and telemetry

