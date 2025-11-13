# mock_test.py
# Test Ant-Trader with mock data

from ant_trader import AntTrader, Candle
import random

def generate_mock_candles(count=100, start_price=1.1050):
    """Generate mock candles - BIGGER movements"""
    candles = []
    current = start_price
    
    for i in range(count):
        # BIGGER random movement (10x)
        move = random.uniform(-0.015, 0.015)  # Was -0.0015, +0.0015
        open_price = current
        close = current + move
        high = max(open_price, close) + abs(random.uniform(0, 0.005))  # Was 0.0005
        low = min(open_price, close) - abs(random.uniform(0, 0.005))   # Was 0.0005
        
        candles.append(Candle(open_price, high, low, close))
        current = close
    
    return candles

def simulate_scenario(scenario_name, candles_modifier):
    """Run simulation"""
    print(f"\n{'='*60}")
    print(f"SCENARIO: {scenario_name}")
    print(f"{'='*60}\n")
    
    bot = AntTrader(pair="EURUSD", risk_pct=0.005, account_balance=5000)
    candles = generate_mock_candles(100)
    
    candles = candles_modifier(candles)
    
    trade_count = 0
    
    for i in range(5, len(candles)):
        current_window = candles[max(0, i-20):i+1]
        result = bot.run_cycle(current_window)
        
        # DEBUG: Print every 10 cycles
        if i % 10 == 0:
            print(f"Candle {i}: {result}")
        
        if result and result["status"] in ["ENTRY", "EXIT", "BE_HIT"]:
            print(f"*** Candle {i}: {result}")
            trade_count += 1
    
    print(f"\nTotal trades detected: {trade_count}")
    
    stats = bot.get_stats()
    if stats:
        print(f"\n{'-'*60}")
        print(f"STATS:")
        print(f"  Total trades: {stats['total_trades']}")
        print(f"  Wins: {stats['wins']}, Losses: {stats['losses']}, BEs: {stats['bes']}")
        print(f"  Win rate: {stats['win_rate_pct']:.1f}%")
        print(f"  Total P&L: EUR {stats['total_pnl_eur']:.2f}")
        print(f"{'-'*60}\n")
    else:
        print("NO TRADES")
    
    return bot

# Scenario 1: Uptrend (BOS should work)
def uptrend_modifier(candles):
    for i, candle in enumerate(candles):
        shift = i * 0.00005  # Gradual uptrend
        candle.open += shift
        candle.high += shift
        candle.low += shift
        candle.close += shift
    return candles

# Scenario 2: Downtrend
def downtrend_modifier(candles):
    for i, candle in enumerate(candles):
        shift = -i * 0.00005  # Gradual downtrend
        candle.open += shift
        candle.high += shift
        candle.low += shift
        candle.close += shift
    return candles

# Scenario 3: Choppy (no trend)
def choppy_modifier(candles):
    return candles  # No modification, random

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "ANT-TRADER MOCK TEST" + " "*23 + "║")
    print("╚" + "="*58 + "╝")
    
    # Run scenarios
    bot1 = simulate_scenario("UPTREND (BOS should work)", uptrend_modifier)
    bot2 = simulate_scenario("DOWNTREND (BOS should work)", downtrend_modifier)
    bot3 = simulate_scenario("CHOPPY (no setup)", choppy_modifier)
    
    print("\n" + "="*60)
    print("ALL SCENARIOS COMPLETE")
    print("="*60 + "\n")