"""
Assignment 1 Exercise: Lists & Basic Operations
Student: Markus
Goal: Understand Python lists as INPUT layer of Waterspider UDM

MISSION:
Learn how lists work in Python by building FX pair data structures
"""

# ============================================================================
# TEHTÄVÄ 1: Luoda ja käsitellä lista
# ============================================================================
print("\n" + "="*60)
print("TEHTÄVÄ 1: Listat ja perusoperaatiot")
print("="*60)

# Valmis - katso vain:
fx_pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"]
print(f"\nStarting pairs: {fx_pairs}")
print(f"Total pairs: {len(fx_pairs)}")

# TODO 1.1: Tulosta ensimmäinen pari (index 0)
print(f"First pair: {fx_pairs[0]}")



# TODO 1.2: Tulosta viimeinen pari (negative indexing)
print(f"Last pair: {fx_pairs[-1]}")



# TODO 1.3: Lisää 2 omaa valuuttaparia append() metodilla
fx_pairs.append("CHF/USD")
fx_pairs.append("SGD/USD")



# TODO 1.4: Tulosta päivitetty lista
print(f"Updated pairs: {fx_pairs}")
