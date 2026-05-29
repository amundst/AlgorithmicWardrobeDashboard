import streamlit as st
import pandas as pd
import random
from collections import Counter

# --- 1. CONFIGURATION & DATA ---
# Formality Matrix (1: Casual, 2: Smart Casual, 3: Formal)
FORMALITY_MATRIX = {
    (1, 1): 1.0, (1, 2): 0.3, (1, 3): 0.0,
    (2, 1): 0.3, (2, 2): 1.0, (2, 3): 0.3,
    (3, 1): 0.0, (3, 2): 0.3, (3, 3): 1.0
}
S_MAP = {"CORE": [1.0, 1.0, 1.0, 1.0], "AW": [0.2, 0.1, 1.0, 1.0], "SS": [1.0, 1.0, 0.2, 0.1]}

TEXTURE_CLASHES = {
    "Technical": ["Corduroy", "Linen"], "Corduroy": ["Technical", "Linen", "Technical_Synthetic"],
    "Linen": ["Corduroy", "Heavy_Wool", "Technical"], "Heavy_Wool": ["Linen"]
}
FATIGUE_TEXTURES = ["Heavy_Wool", "Corduroy", "Denim"]

RAW_INVENTORY = [
    # Bottoms
    {"Category": "Bottom", "Item": "Chinos | Gant", "Tier": "A", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Classic", "Texture": "Cotton"},
    {"Category": "Bottom", "Item": "Jeans | OrSlow 105", "Tier": "A", "Formality": 1, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Workwear", "Texture": "Denim"},
    {"Category": "Bottom", "Item": "Chinos | Lindbergh", "Tier": "B", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Classic", "Texture": "Cotton"},
    {"Category": "Bottom", "Item": "Wool Pants | Oscar Jacobsen", "Tier": "B", "Formality": 3, "CORE": False, "Seasons": S_MAP["AW"], "Style": "Classic", "Texture": "Heavy_Wool"},
    {"Category": "Bottom", "Item": "Tech Chinos | Lululemon", "Tier": "B", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Tech", "Texture": "Technical"},
    {"Category": "Bottom", "Item": "Jeans | Levis 501", "Tier": "B", "Formality": 1, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Workwear", "Texture": "Denim"},
    {"Category": "Bottom", "Item": "Linen Shorts | These Glory Days", "Tier": "B", "Formality": 1, "CORE": False, "Seasons": S_MAP["SS"], "Style": "Classic", "Texture": "Linen"},
    {"Category": "Bottom", "Item": "Chino Shorts | J. Lindbergh", "Tier": "B", "Formality": 1, "CORE": False, "Seasons": S_MAP["SS"], "Style": "Classic", "Texture": "Cotton"},
    {"Category": "Bottom", "Item": "Corduroy | Massimo Dutti", "Tier": "C", "Formality": 2, "CORE": False, "Seasons": S_MAP["AW"], "Style": "Workwear", "Texture": "Corduroy"},
    # Shirts
    {"Category": "Shirt", "Item": "Chambray | Morris", "Tier": "A", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Workwear", "Texture": "Cotton"},
    {"Category": "Shirt", "Item": "Seersucker | Grigio", "Tier": "A", "Formality": 2, "CORE": False, "Seasons": S_MAP["SS"], "Style": "Classic", "Texture": "Linen"},
    {"Category": "Shirt", "Item": "Poplin | Zegna", "Tier": "B", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Classic", "Texture": "Cotton"},
    {"Category": "Shirt", "Item": "Flannel | Boss", "Tier": "B", "Formality": 1, "CORE": False, "Seasons": S_MAP["AW"], "Style": "Workwear", "Texture": "Cotton"},
    {"Category": "Shirt", "Item": "Linen | Åhlens", "Tier": "B", "Formality": 1, "CORE": False, "Seasons": S_MAP["SS"], "Style": "Classic", "Texture": "Linen"},
    {"Category": "Shirt", "Item": "Vintage Shirt", "Tier": "B", "Formality": 1, "CORE": False, "Seasons": S_MAP["SS"], "Style": "Workwear", "Texture": "Cotton"},
    {"Category": "Shirt", "Item": "Polo | Navy", "Tier": "B", "Formality": 1, "CORE": False, "Seasons": S_MAP["SS"], "Style": "Classic", "Texture": "Cotton"},
    {"Category": "Shirt", "Item": "White Tattersall | Laksen", "Tier": "C", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Classic", "Texture": "Cotton"},
    {"Category": "Shirt", "Item": "OCBD | Morris", "Tier": "C", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Classic", "Texture": "Cotton"},
    {"Category": "Shirt", "Item": "OCBD | Taylor Store", "Tier": "C", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Classic", "Texture": "Cotton"},
    {"Category": "Shirt", "Item": "OCBD | J. Lindeberg", "Tier": "C", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Classic", "Texture": "Cotton"},
    # Layers
    {"Category": "Layer", "Item": "Cashmere | Piecenza", "Tier": "A", "Formality": 2, "CORE": False, "Seasons": S_MAP["AW"], "Style": "Hybrid", "Texture": "Heavy_Wool"},
    {"Category": "Layer", "Item": "Sweatshirt | Arket", "Tier": "A", "Formality": 1, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Workwear", "Texture": "Cotton"},
    {"Category": "Layer", "Item": "Corduroy Overshirt | Wrangler", "Tier": "A", "Formality": 1, "CORE": False, "Seasons": S_MAP["AW"], "Style": "Workwear", "Texture": "Corduroy"},
    {"Category": "Layer", "Item": "Merino Zip | John Smedley", "Tier": "B", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Classic", "Texture": "Heavy_Wool"},
    {"Category": "Layer", "Item": "Moleskin | Portuguese Flannel", "Tier": "B", "Formality": 1, "CORE": False, "Seasons": S_MAP["AW"], "Style": "Workwear", "Texture": "Cotton"},
    {"Category": "Layer", "Item": "Guernsey | Blue", "Tier": "C", "Formality": 1, "CORE": False, "Seasons": S_MAP["AW"], "Style": "Workwear", "Texture": "Heavy_Wool"},
    # Outerwear
    {"Category": "Outer", "Item": "Car Coat | UBR", "Tier": "A", "Formality": 2, "CORE": False, "Seasons": S_MAP["AW"], "Style": "Tech", "Texture": "Technical"},
    {"Category": "Outer", "Item": "Waxed Jacket | Barbour", "Tier": "B", "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Workwear", "Texture": "Cotton"},
    {"Category": "Outer", "Item": "Overcoat | Boss", "Tier": "B", "Formality": 3, "CORE": False, "Seasons": S_MAP["AW"], "Style": "Classic", "Texture": "Heavy_Wool"},
    {"Category": "Outer", "Item": "Denim Jacket | Levis", "Tier": "B", "Formality": 1, "CORE": False, "Seasons": S_MAP["SS"], "Style": "Workwear", "Texture": "Denim"},
    {"Category": "Outer", "Item": "Harrington | Scan. Ed.", "Tier": "B", "Formality": 1, "CORE": False, "Seasons": S_MAP["SS"], "Style": "Tech", "Texture": "Technical"},
    {"Category": "Outer", "Item": "Peacoat | Vintage", "Tier": "C", "Formality": 2, "CORE": False, "Seasons": S_MAP["AW"], "Style": "Workwear", "Texture": "Heavy_Wool"},
    # Footwear
    {"Category": "Footwear", "Item": "Boots | Thursday", "Tier": "A", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Workwear", "Texture": "Leather"},
    {"Category": "Footwear", "Item": "Sneakers | Samba", "Tier": "A", "Formality": 1, "CORE": False, "Seasons": S_MAP["SS"], "Style": "Workwear", "Texture": "Suede"},
    {"Category": "Footwear", "Item": "Derby | Loake", "Tier": "B", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Classic", "Texture": "Leather"},
    {"Category": "Footwear", "Item": "Sneakers | Reebok", "Tier": "B", "Formality": 1, "CORE": False, "Seasons": S_MAP["SS"], "Style": "Workwear", "Texture": "Leather"},
    {"Category": "Footwear", "Item": "Chukka | Thursday", "Tier": "C", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Workwear", "Texture": "Suede"},
    {"Category": "Footwear", "Item": "Chelsea | Thursday", "Tier": "C", "Formality": 2, "CORE": False, "Seasons": S_MAP["AW"], "Style": "Classic", "Texture": "Leather"},
    {"Category": "Footwear", "Item": "Converse", "Tier": "C", "Formality": 1, "CORE": False, "Seasons": S_MAP["SS"], "Style": "Workwear", "Texture": "Canvas"},
    # Accessories & Suiting
    {"Category": "Accessory", "Item": "Watch | Alpinist", "Tier": "A", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Hybrid", "Texture": "Metal"},
    {"Category": "Accessory", "Item": "Belt | Saddler", "Tier": "A", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Classic", "Texture": "Leather"},
    {"Category": "Accessory", "Item": "Glasses | Persol", "Tier": "A", "Formality": 1, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Classic", "Texture": "Plastic"},
    {"Category": "Accessory", "Item": "Gloves | Amanda C", "Tier": "A", "Formality": 2, "CORE": False, "Seasons": S_MAP["AW"], "Style": "Hybrid", "Texture": "Leather"},
    {"Category": "Suiting", "Item": "Suit | Navy | Skabo", "Tier": "A", "Formality": 3, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Classic", "Texture": "Fine_Wool"},
    {"Category": "Suiting", "Item": "Oxford | Crockett & Jones", "Tier": "A", "Formality": 3, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Classic", "Texture": "Leather"}
]

df = pd.DataFrame(RAW_INVENTORY)
df['Tier_Weight'] = df['Tier'].map({'A': 60, 'B': 30, 'C': 10})

# --- 2. LOGIC ---
def get_best_item(df, category, anchor, s_idx):
    pool = df[df['Category'] == category].copy()
    if random.random() < 0.2: return pool.sample(n=1).iloc[0]
    anchor_style = anchor['Style']
    def calculate_weight(row):
        core_boost = 1.1 if row['CORE'] else 1.0
        season_score = row['Seasons'][s_idx]
        f_score = FORMALITY_MATRIX.get((anchor['Formality'], row['Formality']), 0.0)
        style_score = 1.8 if row['Style'] == anchor_style else (0.6 if row['Style'] == "Hybrid" or anchor_style == "Hybrid" else 0.1)
        return row['Tier_Weight'] * season_score * f_score * core_boost * style_score
    pool['Final_Weight'] = pool.apply(calculate_weight, axis=1)
    pool = pool[pool['Final_Weight'] > 0]
    return pool.sample(n=1, weights='Final_Weight').iloc[0] if not pool.empty else None

def validate_outfit(outfit):
    if 'Bottom' not in outfit or 'Footwear' not in outfit: return False
    if 'Shirt' not in outfit and 'Layer' not in outfit: return False
    # Texture Fatigue
    textures = [outfit[c].get('Texture') for c in ['Bottom', 'Shirt', 'Layer'] if c in outfit]
    counts = pd.Series(textures).value_counts()
    for tex, count in counts.items():
        if tex in FATIGUE_TEXTURES and count > 1: return False
    return True

def generate_full_outfit(anchor_name, season):
    s_idx = ["Spring", "Summer", "Autumn", "Winter"].index(season)
    anchor = df[df['Item'] == anchor_name].iloc[0]
    for _ in range(100):
        outfit = {anchor['Category']: anchor}
        slots = ['Bottom', 'Shirt', 'Layer', 'Outer', 'Footwear', 'Accessory', 'Suiting']
        random.shuffle(slots)
        for slot in slots:
            if slot in outfit or (slot == 'Suiting' and outfit.get('Bottom', {}).get('Category') != 'Suiting'): continue
            match = get_best_item(df, slot, anchor, s_idx)
            if match is not None: outfit[slot] = match
        if validate_outfit(outfit): return outfit
    return None

# --- 3. UI ---
st.title("Algorithmic Wardrobe")
season = st.sidebar.selectbox("Season", ["Spring", "Summer", "Autumn", "Winter"])
anchor = st.sidebar.selectbox("Pick Anchor", df['Item'].tolist())

if st.sidebar.button("Generate Outfit"):
    st.session_state.outfit = generate_full_outfit(anchor, season)

if 'outfit' in st.session_state and st.session_state.outfit:
    for cat, item in st.session_state.outfit.items():
        st.write(f"**{cat}**: {item['Item']}")
    if st.button("Are these items clean? (Y)"): st.success("Enjoy your day!")
    if st.button("No (N)"): st.rerun()