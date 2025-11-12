# Mikrobot Main Strategy — EURUSD Scalping (BE Target Strategy)

Author: Markus  
Date: Week 47, 2025  
Status: Production v1 (Ready for Coding)

---

## 1. Goal & Scope
- **Instrument:** EURUSD only (Week 47 pilot)
- **Timeframes:** H1 (bias) + M5 (execution)
- **Style:** Scalping with Break Even (BE) focus
- **Target:** 2-4 pips profit per trade
- **Objective:** High win rate data for MPTO loop optimization
- **Future:** Scale to 7 forex pairs + NAS100 + BTC/ETH (post-optimization)

---

## 2. Strategy Philosophy

**Goal:** Achieve rapid break-even exits + tight 2-4 pip profits
- High win rate feeds MPTO confidence
- Quick capital turnover
- Data-rich for Waterspider ML optimization
- Low drawdown (tight SL = small losses)

**Success Metric:** Win rate > 60% + profit factor > 1.5
**Risk Model:** 0.5% per trade (scalping = smaller SL, more frequent)
**Optimization Loop:** MPTO (Measure→Plan→Take Action→Observe) via Waterspider

---

## 3. Assumptions & Constraints
- **Broker:** MT5 terminal (IconFX/PUPrime)
- **Execution:** Market orders with attached SL/TP
- **Spread:** EURUSD typical 0.2-0.4 pips (max 1.2 allowed)
- **Risk per trade:** 0.5% account balance
- **TP target:** 2-4 pips (tight, achievable)
- **SL:** 10-15 pips (tight, scalping-appropriate)
- **Session:** London + New York sessions (best volume/liquidity)
- **Position limit:** 1 BUY + 1 SELL maximum concurrent
- **Cooldown:** 15 minutes after SL hit (reset signal)

---

## 4. Definitions

### Market Structure & Setups

**Impulse Leg:**
- Directional price move 3+ consecutive M5 candles in same direction
- Minimum 15+ pips for clear identification
- Defines "where are we going?"

**Consolidation:**
- 2-3 M5 candles trading sideways (range < 8 pips)
- Follows impulse leg
- Defines "where are we waiting?"

**Pullback Zone:**
- Price retraces into impulse zone after consolidation
- Typical: 50% retrace or consolidation low/high
- Acts as entry trigger area
- Range: 5-10 pips (tight zone)

**Break of Structure (BOS):**
- Market breaks previous impulse high/low
- Indicates continuation or reversal
- H1 BOS = strong directional bias
- M5 BOS in bias direction = setup confirmation

### Entry Concepts

**Entry Setup (M5):**
1. Impulse leg visible (15+ pips)
2. Consolidation forms (2-3 candles sideways)
3. Pullback into zone (50% retrace area)
4. Price at zone boundary

**Entry Trigger (M5 Close):**
- **Engulfing Candle:** M5 close engulfs prior candle in impulse direction
- **Strong Body:** M5 candle body > 70% of range, closes at extreme
- Either = entry signal at market

**Entry Execution:**
- Market order on M5 candle close
- Price = current market (scalp entry ASAP)
- SL = 10-15 pips beyond pullback zone
- TP = +2 to +4 pips from entry

### Risk & Sizing

**Risk Amount:**
- risk_pct = 0.005 (0.5%)
- risk_amount = balance × 0.005
- Example: 5000€ × 0.005 = 25€ per trade

**Position Size (Lots):**
- Formula: volume = risk_amount / (stop_pips × pip_value)
- Example: 25€ / (12 pips × 10€/pip) = 0.208 lots → normalize to 0.2
- Broker min/max respected; reject if below minimum

**Stop Loss (Pips):**
- Always beyond pullback zone + buffer
- Typical: 10-15 pips
- Calculated per trade based on zone location

**Take Profit (Pips):**
- Fixed: 2-4 pips (tight scalp target)
- Goal: High probability hit = higher win rate

---

## 5. Timeframe Logic

### H1 Bias Determination (Filter Layer)
**Run:** Once per 4-hour cycle or at session start

**Logic:**
1. Identify last 3-5 H1 candle swings (highs/lows)
2. Determine structure: Higher High/Higher Low (uptrend) vs Lower High/Lower Low (downtrend)
3. Latest H1 BOS direction = current bias
4. Output: **bias = UP / DOWN / NONE**

**No Trades When:** bias = NONE (choppy, no direction)

### M5 Execution Loop (Action Layer)
**Run:** Every M5 candle close

**Logic:**
1. **Check bias:** If NONE, skip to next candle
2. **Scan for setup:** Impulse 15+ pips → Consolidation → Pullback zone forming?
3. **At pullback zone:** Wait for trigger (engulfing or strong body)
4. **On trigger:** Calculate SL/TP, size, risk; check filters (spread/session/cooldown)
5. **Place order:** Market order with attached SL/TP
6. **Monitor:** Trade closes at SL or TP; log result

**Interaction Rule:**
- H1 bias filters which direction to trade
- M5 finds exact entry in filtered direction
- No counter-bias trades (disciplined)

---

## 6. Entry Rules (M5)

### Pullback Zone Definition
- **Price location:** Consolidation low (short) or high (long)
- **50% retrace area:** From impulse extreme to consolidation open
- **Zone width:** Typically 5-10 pips

### Entry Trigger (Candle Close Required)
**BUY Setup (Uptrend Bias):**
1. Pullback to zone (price touches or enters)
2. M5 candle close above zone boundary
3. Candle is engulfing OR strong body (close near high, > 70% range)
4. Volume/momentum check (optional: larger close = stronger signal)

**SELL Setup (Downtrend Bias):**
1. Pullback to zone (price touches or enters)
2. M5 candle close below zone boundary
3. Candle is engulfing OR strong body (close near low, > 70% range)
4. Volume/momentum check (optional: larger close = stronger signal)

### Entry Execution
- **Order Type:** Market (enter immediately on close)
- **Price:** Current market bid/ask
- **SL Attachment:** Set at order placement
- **TP Attachment:** Set at order placement
- **Position:** 1 BUY + 1 SELL max (no pyramiding)

### Rejection Rules
- **Spread > 1.2 pips:** SKIP trade
- **Outside session window:** SKIP trade
- **Cooldown active:** SKIP trade (15min after SL)
- **Position already open in direction:** SKIP trade
- **Risk < broker minimum:** SKIP trade (undersized)

---

## 7. Stop, Target, and Management

### Stop Loss Placement
- **Logic:** Beyond pullback zone + ATR buffer (optional)
- **Typical distance:** 10-15 pips from entry
- **Formula:** SL = entry ± (zone_depth + 2 pips buffer)
- **Validation:** Broker must allow; adjust if too close

### Take Profit Levels
- **Primary TP (2-4 pips):** Main exit
  - Target: 2 pips (safe, higher probability)
  - Target: 3-4 pips (aggressive, fewer hits)
  - Set based on spread + volume (use 3 pips default)

- **No Partial Targets:** Close entire position at TP (scalping style)

### Trade Management

**During Trade:**
- Monitor fill and SL/TP levels (verify broker set correctly)
- No manual adjustments (automated via attached orders)
- No trailing stops (tight SL = quick resolution)

**Exit Conditions:**
- TP hit: Trade closes, profit recorded
- SL hit: Trade closes, loss recorded, cooldown triggered (15min)
- Time-based (optional): Close if open > 60 minutes (EOD management)

**Cooldown After SL:**
- Duration: 15 minutes (reset signal, avoid revenge trading)
- Applies per symbol
- Resume scanning after 15min

### Daily Management
- **Track win rate & PnL intraday**
- **Daily loss limit (optional):** Stop if daily loss > -1% account (safety)
- **End of session:** Close all open trades at session end (no overnight risk)

---

## 8. Risk & Sizing (Detailed)

### Position Size Calculation