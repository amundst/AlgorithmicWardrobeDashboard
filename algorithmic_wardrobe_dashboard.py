import streamlit as st
import pandas as pd
import random

# --- 1. DATA & CONSTRAINTS ---
CONTEXTS = {
    "Work 💼": [2, 3], "Restaurant 🍽️": [2], "Family Dinner 🏠": [1, 2],
    "Casual Party 🎉": [1, 2], "Bar 🍻": [1, 2], "Beach 🏖️": [1],
    "Shopping 🛍️": [1, 2], "Stage/Formal 🎭": [3]
}

TEXTURE_CLASHES = {
    "Technical": ["Corduroy", "Linen"], "Corduroy": ["Technical", "Linen", "Technical_Synthetic"],
    "Linen": ["Corduroy", "Heavy_Wool", "Technical"], "Heavy_Wool": ["Linen"]
}
FATIGUE_TEXTURES = ["Heavy_Wool", "Corduroy", "Denim"]
COLOR_CLASHES = {"Black": ["Navy", "Brown", "Earth"], "Navy": ["Black"], "Earth": ["Black", "Cool_Grey"]}

RAW_INVENTORY = [
    {"Category": "Bottom", "Item": "Chinos | Olive Green", "Tier": "A", "Formality": 2, "Texture": "Cotton", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Autumn"], "Temps": ["Temperate"], "Weather": ["Dry"], "CORE": False},
    {"Category": "Bottom", "Item": "Jeans | Dark Indigo", "Tier": "A", "Formality": 1, "Texture": "Denim", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Autumn", "Winter", "Spring", "Summer"], "Temps": ["Cold", "Temperate", "Warm"], "Weather": ["Dry", "Wet"], "CORE": True},
    {"Category": "Shirt", "Item": "OCBD | Light Blue", "Tier": "C", "Formality": 2, "Texture": "Cotton", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Autumn", "Winter", "Spring", "Summer"], "Temps": ["Cold", "Temperate", "Warm"], "Weather": ["Dry", "Wet"], "CORE": True},
    {"Category": "Shirt", "Item": "T-Shirt | White", "Tier": "C", "Formality": 1, "Texture": "Cotton", "Color_Base": "Neutral", "Pattern": "Solid", "Seasons": ["Autumn", "Winter", "Spring", "Summer"], "Temps": ["Cold", "Temperate", "Warm"], "Weather": ["Dry", "Wet"], "CORE": True},
    {"Category": "Shirt", "Item": "T-Shirt | Navy", "Tier": "C", "Formality": 1, "Texture": "Cotton", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Autumn", "Winter", "Spring", "Summer"], "Temps": ["Cold", "Temperate", "Warm"], "Weather": ["Dry", "Wet"], "CORE": True},
    {"Category": "Shirt", "Item": "Flannel | Red Check", "Tier": "B", "Formality": 1, "Texture": "Cotton", "Color_Base": "Earth", "Pattern": "Checkered", "Seasons": ["Autumn", "Winter"], "Temps": ["Cold", "Temperate"], "Weather": ["Dry", "Wet"], "CORE": False},
    {"Category": "Layer", "Item": "Cashmere Crew | Anthracite", "Tier": "A", "Formality": 2, "Texture": "Heavy_Wool", "Color_Base": "Cool_Grey", "Pattern": "Solid", "Seasons": ["Autumn", "Winter", "Spring"], "Temps": ["Cold", "Temperate"], "Weather": ["Dry", "Wet"], "CORE": False},
    {"Category": "Outer", "Item": "Car Coat | Navy Waterproof", "Tier": "A", "Formality": 2, "Texture": "Technical", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Autumn", "Winter", "Spring"], "Temps": ["Cold", "Temperate"], "Weather": ["Dry", "Wet"], "CORE": False},
    {"Category": "Footwear", "Item": "Lace up Boots | Brown Leather", "Tier": "A", "Formality": 2, "Texture": "Leather", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Autumn", "Winter", "Spring"], "Temps": ["Cold", "Temperate"], "Weather": ["Dry", "Wet"], "CORE": False}
]

def load_data():
    df = pd.DataFrame(RAW_INVENTORY)
    df['Tier_Weight'] = df['Tier'].map({'A': 100, 'B': 40, 'C': 5})
    return df

def get_best_item(df, category, anchor, target_season, target_temp, target_weather):
    pool = df[df['Category'] == category].copy()
    
    def calculate_weight(row):
        # 1. CORE logic
        if row['CORE']: return row['Tier_Weight'] * 2.0
        
        # 2. Environmental Weighting (Soft Constraints)
        env_score = 1.0
        if target_season not in row['Seasons']: env_score *= 0.3
        if target_temp not in row['Temps']: env_score *= 0.3
        if target_weather not in row['Weather']: env_score *= 0.3
        
        # 3. Formality Weighting
        diff = row['Formality'] - anchor['Formality']
        if row['Formality'] == 3 or abs(diff) > 1: return 0
        formality_score = 0.2 if diff > 0 else 1.0
        
        # 4. Color Clash
        color_score = 0 if row['Color_Base'] in COLOR_CLASHES.get(anchor['Color_Base'], []) else 1.0
        
        return row['Tier_Weight'] * env_score * formality_score * color_score
    
    pool['Final_Weight'] = pool.apply(calculate_weight, axis=1)
    pool = pool[pool['Final_Weight'] > 0]
    return pool.sample(n=1, weights='Final_Weight').iloc[0] if not pool.empty else None

def validate_outfit(outfit):
    if 'Bottom' not in outfit or 'Footwear' not in outfit: return False
    if 'Shirt' not in outfit and 'Layer' not in outfit: return False
    textures = [outfit[c]['Texture'] for c in ['Bottom', 'Shirt', 'Layer'] if c in outfit]
    counts = pd.Series(textures).value_counts()
    for tex, count in counts.items():
        if tex in FATIGUE_TEXTURES and count > 1: return False
    return True

def generate_full_outfit(df, anchor_name, season, temp, weather):
    anchor = df[df['Item'] == anchor_name].iloc[0]
    for _ in range(50):
        outfit = {anchor['Category']: anchor}
        slots = ['Bottom', 'Shirt', 'Layer', 'Outer', 'Footwear', 'Accessory']
        random.shuffle(slots)
        for slot in slots:
            if slot in outfit: continue
            match = get_best_item(df, slot, anchor, season, temp, weather)
            if match is not None: outfit[slot] = match
        if validate_outfit(outfit): return outfit
    return None

st.title("Daily Outfit Planner")
df = load_data()
with st.sidebar:
    season, temp, weather = st.selectbox("Season", ["Autumn", "Winter", "Spring", "Summer"]), st.selectbox("Temp", ["Cold", "Temperate", "Warm"]), st.selectbox("Weather", ["Dry", "Wet"])
    context = st.selectbox("Context", list(CONTEXTS.keys()))
    anchor = st.selectbox("Pick Anchor", df['Item'].tolist())
    if st.button("Generate"): st.session_state.outfit = generate_full_outfit(df, anchor, season, temp, weather)

if 'outfit' in st.session_state and st.session_state.outfit:
    for cat, item in st.session_state.outfit.items(): st.write(f"**{cat}**: {item['Item']}")
    if st.button("Are these items clean? (Y)"): st.success("Enjoy.")
    if st.button("No (N)"): st.rerun()