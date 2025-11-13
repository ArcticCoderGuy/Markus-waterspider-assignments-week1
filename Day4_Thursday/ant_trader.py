# ant_trader.py - KORJATTU (vain ASCII)
from market_structure import detect_bos, detect_m1_break_retest, calculate_atr, Candle
from datetime import datetime

class AntTrader:
    """Stupid but consistent Ant-Trader"""
    
    def __init__(self, pair="EURUSD", risk_pct=0.005, account_balance=5000):
        self.pair = pair
        self.risk_pct = risk_pct
        self.account_balance = account_balance
        
        # Config
        self.stop_pips = 12
        self.tp_pips = 3
        self.atr_min = 0.0005
        self.atr_max = 0.005
        
        # State
        self.open_trade = None
        self.trades_log = []
    
    def run_cycle(self, m5_candles):
        """One cycle"""
        
        if len(m5_candles) < 3:
            return None
        
        atr = calculate_atr(m5_candles, period=14)
        if atr is None or atr < self.atr_min or atr > self.atr_max:
            return {"status": "SKIP", "reason": f"ATR {atr:.2f} out of range"}
        
        if self.open_trade:
            exit_result = self.check_exit(m5_candles[-1])
            if exit_result:
                return exit_result
            return {"status": "TRADE_OPEN", "entry": self.open_trade["entry"]}
        
        bos = detect_bos(m5_candles)
        if not bos:
            return {"status": "NO_BOS"}
        
        signal = detect_m1_break_retest(m5_candles, bos)
        if not signal:
            return {"status": "NO_SIGNAL"}
        
        entry_result = self.entry_trade(m5_candles[-1], bos)
        return entry_result
    
    def entry_trade(self, candle, direction):
        """Entry"""
        
        entry_price = candle.close
        
        if direction == "UP":
            sl = entry_price - (self.stop_pips * 0.0001)
            tp = entry_price + (self.tp_pips * 0.0001)
        else:
            sl = entry_price + (self.stop_pips * 0.0001)
            tp = entry_price - (self.tp_pips * 0.0001)
        
        risk_amount = self.account_balance * self.risk_pct
        stop_distance_pips = self.stop_pips
        pip_value = 10
        volume = risk_amount / (stop_distance_pips * pip_value)
        
        self.open_trade = {
            "direction": direction,
            "entry": entry_price,
            "sl": sl,
            "tp": tp,
            "volume": round(volume, 2),
            "entry_time": datetime.now(),
            "be_hit": False,
            "highest": entry_price if direction == "UP" else entry_price,
            "lowest": entry_price if direction == "DOWN" else entry_price
        }
        
        return {
            "status": "ENTRY",
            "direction": direction,
            "entry": entry_price,
            "sl": sl,
            "tp": tp,
            "volume": volume,
            "risk_eur": risk_amount
        }
    
    def check_exit(self, candle):
        """Check exit"""
        
        if not self.open_trade:
            return None
        
        current_price = candle.close
        trade = self.open_trade
        direction = trade["direction"]
        
        if direction == "UP":
            trade["highest"] = max(trade["highest"], current_price)
        else:
            trade["lowest"] = min(trade["lowest"], current_price)
        
        if direction == "UP" and current_price >= trade["tp"]:
            return self.close_trade("TP", current_price, candle)
        
        if direction == "DOWN" and current_price <= trade["tp"]:
            return self.close_trade("TP", current_price, candle)
        
        if direction == "UP" and current_price <= trade["sl"]:
            return self.close_trade("SL", current_price, candle)
        
        if direction == "DOWN" and current_price >= trade["sl"]:
            return self.close_trade("SL", current_price, candle)
        
        if not trade["be_hit"]:
            be_threshold = trade["entry"] + ((trade["tp"] - trade["entry"]) * 0.5)
            
            if direction == "UP" and current_price >= be_threshold:
                trade["be_hit"] = True
                trade["sl"] = trade["entry"] + 0.0001
                return {"status": "BE_HIT", "new_sl": trade["sl"]}
        
        return None
    
    def close_trade(self, reason, close_price, candle):
        """Close trade and log"""
        
        trade = self.open_trade
        pnl_pips = abs(close_price - trade["entry"]) / 0.0001
        pnl_eur = (close_price - trade["entry"]) * trade["volume"] * 10
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "pair": self.pair,
            "direction": trade["direction"],
            "entry": trade["entry"],
            "close": close_price,
            "sl": trade["sl"],
            "tp": trade["tp"],
            "volume": trade["volume"],
            "pnl_pips": pnl_pips,
            "pnl_eur": pnl_eur,
            "reason": reason,
            "be_hit": trade["be_hit"]
        }
        
        self.trades_log.append(log_entry)
        self.open_trade = None
        
        return {
            "status": "EXIT",
            "reason": reason,
            "close_price": close_price,
            "pnl_pips": pnl_pips,
            "pnl_eur": pnl_eur
        }
    
    def get_stats(self):
        """Stats"""
        if not self.trades_log:
            return None
        
        wins = sum(1 for t in self.trades_log if t["pnl_eur"] > 0)
        losses = sum(1 for t in self.trades_log if t["pnl_eur"] < 0)
        bes = len(self.trades_log) - wins - losses
        
        total_pnl = sum(t["pnl_eur"] for t in self.trades_log)
        
        return {
            "total_trades": len(self.trades_log),
            "wins": wins,
            "losses": losses,
            "bes": bes,
            "win_rate_pct": (wins / len(self.trades_log)) * 100 if self.trades_log else 0,
            "total_pnl_eur": total_pnl
        }