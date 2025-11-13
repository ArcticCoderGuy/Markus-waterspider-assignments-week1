# market_structure.py
# Simple market structure detection - DUMB but works

class Candle:
    def __init__(self, open_price, high, low, close):
        self.open = open_price
        self.high = high
        self.low = low
        self.close = close
        self.range = high - low
        self.body = abs(close - open_price)

def detect_bos(candles):
    """Detect M5 Break of Structure - simple version"""
    if len(candles) < 3:
        return None
    
    # Last 3 candles
    c1, c2, c3 = candles[-3], candles[-2], candles[-1]
    
    # Uptrend: HH and HL
    if c3.high > c2.high > c1.high and c3.low > c2.low > c1.low:
        return "UP"
    
    # Downtrend: LH and LL
    if c3.high < c2.high < c1.high and c3.low < c2.low < c1.low:
        return "DOWN"
    
    return None

def detect_m1_break_retest(m5_candles, bos_direction):
    """After M5 BOS, detect M1 Break & Retest concept"""
    if not m5_candles:
        return None
    
    latest = m5_candles[-1]
    
    # Simple: is price moving in BOS direction?
    if bos_direction == "UP" and latest.close > latest.open:
        return "ENTRY_SIGNAL_UP"
    
    if bos_direction == "DOWN" and latest.close < latest.open:
        return "ENTRY_SIGNAL_DOWN"
    
    return None

def calculate_atr(candles, period=14):
    """Simple ATR calculation"""
    if len(candles) < period + 1:
        return 0.0005  # Return default if not enough data
    
    trs = []
    for i in range(1, len(candles)):
        prev_close = candles[i-1].close
        high = candles[i].high
        low = candles[i].low
        
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        trs.append(tr)
    
    if not trs:
        return 0.0005
    
    atr = sum(trs[-period:]) / period
    return atr if atr > 0 else 0.0005