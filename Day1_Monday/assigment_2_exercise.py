"""
Assignment 2 Exercise: Functions & parse_pair()
Student: Markus
Goal: Write a function to parse FX pairs (INPUT-PROCESS-OUTPUT)

MISSION:
Learn how functions work by building parse_pair()
This function will split "EUR/USD" into {"base": "EUR", "quote": "USD"}
"""

# ============================================================================
# TEHTÄVÄ 2: Kirjoita funktio parse_pair() - KOODAAMINEN!
# ============================================================================
print("\n" + "="*60)
print("TEHTÄVÄ 2: Funktio parse_pair()")
print("="*60)

# TODO 2.1: Kirjoita funktio parse_pair()
# 
# Mitä se tekee:
# - Ottaa parametrin: pair (esim "EUR/USD")
# - Jakaa sen split("/") metodilla
# - Palauttaa dictionary: {"base": "EUR", "quote": "USD"}
#
# Esimerkki:
# parse_pair("EUR/USD") → {"base": "EUR", "quote": "USD"}

def parse_pair(pair):
    parts = pair.split("/")
    return {"base": parts[0], "quote": parts[1]}



# ============================================================================
# TEHTÄVÄ 3: Käytä funktiota (Iterointi)
# ============================================================================
print("\n" + "="*60)
print("TEHTÄVÄ 3: For-silmukka + Funktio")
print("="*60)

# Käytä listaasi assignment_1_exercise.py:stä:
# fx_pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "CHF/USD", "SGD/USD"]

# TODO 3.1: Kirjoita for-silmukka joka:
# - Iteroi listan läpi
# - Kutsu parse_pair() jokaiselle
# - Tulosta tulos
#
# for pair in fx_pairs:
#     result = parse_pair(pair)
#     print(f"{pair}: {result}")

# SINÄ KIRJOITAT TÄMÄN!


# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*60)
print("VALMIS!")
print("="*60)
```

---

## 🎯 **SEURAAVA ASKEL (nyt):**

**VS Code:ssa:**

1. **Liitä pohja** (Ctrl+V)
2. **Ctrl+S** → nimeä: `assignment_2_exercise.py`
3. **Tallenna Day1_Monday:iin**

---

## ✅ **VALMIUDEN MERKKI:**

Kun tiedosto luotu ja tallennettu, kerro:
```
"assignment_2_exercise.py luotu Day1_Monday:iin!"