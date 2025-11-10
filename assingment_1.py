"""
Assignment 1: Lists - FX Pair Data Structures

Learning Objective: Understand Python lists, indexing, and list methods
Real-world Application: Store and organize FX trading pairs

Author: Markus / ©Fox-In-The-Code
Date: Week 1, Monday
"""
# ============================================================================
# TEHTÄVÄ 1: Luoda ja muokata lista
# ============================================================================

# TODO 1.1: Luo lista nimeltä fx_pairs
# Sisältö: ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"]
# Kopioi vain - älä muuta!

fx_pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"]

# TODO 1.2: Tulosta lista
# Käytä: print(f"Our pairs: {fx_pairs}")

print(f"Our pairs: {fx_pairs}")

# TODO 1.3: Tulosta listan pituus
# Käytä: len()

print(f"Number of pairs: {len(fx_pairs)}")

# TODO 1.4: Lisää yksi pari append() -metodilla
# Lisää: "CHF/USD"
# Kopioi tämä rivi ja täytä:
# fx_pairs.append("???")

# SINÄ KIRJOITAT TÄMÄN!


# ============================================================================
# TEHTÄVÄ 2: Kirjoita funktio (KOODAAMINEN!)
# ============================================================================

# TODO 2.1: Kirjoita funktio parse_pair()
# Input: "EUR/USD"
# Output: {"base": "EUR", "quote": "USD"}
# 
# Vinkkejä:
# - Käytä split("/") jakamaan stringin
# - Palauta dictionary
#
# def parse_pair(pair):
#     # SINÄ KIRJOITAT LOGIIKAN!

# SINÄ KIRJOITAT TÄMÄN!


# ============================================================================
# TEHTÄVÄ 3: Käytä funktiota
# ============================================================================

# TODO 3.1: Iteroida listan läpi for-silmukalla
# Kutsu parse_pair() jokaiselle parille
# Tulosta tulos
#
# for pair in fx_pairs:
#     result = parse_pair(pair)
#     print(...)

# SINÄ KIRJOITAT TÄMÄN!
```

---

## 🎯 **NYKYTILANNE - SEURAAVA ASKEL:**
```
SINÄ (Driver):
1. Avaa VS Code
2. Luo tiedosto: assignment_1_exercise.py
3. Kopioi yllä oleva pohja (TODO-kommentit)
4. Tallenna: Ctrl+S

MINÄ (Navigator):
Odottelen kun sanot "Valmis, pohja luotu!"

Sitten:
INPUT → PROCESS → OUTPUT
```

---

## ✅ **VALMIUDEN MERKKI:**

Kun olet luonut tiedoston ja kopioinut pohjan, kirjoita:
```
"Valmis - assignment_1_exercise.py luotu pohjan kanssa!"