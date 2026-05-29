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
    {"Category": "Bottom", "Item": "Chinos | Olive Green", "Tier": "A", "Formality": 2, "Texture": "Cotton", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Autumn"], "Temps": ["Temperate"], "Weather": ["Dry"]},
    {"Category": "Bottom", "Item": "Jeans | Dark Indigo", "Tier": "A", "Formality": 1, "Texture": "Denim", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Cold"], "Weather": ["Dry"]},
    {"Category": "Shirt", "Item": "OCBD | Light Blue", "Tier": "C", "Formality": 2, "Texture": "Cotton", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Cold"], "Weather": ["Dry"]},
    {"Category": "Shirt", "Item": "Flannel | Red Check", "Tier": "B", "Formality": 1, "Texture": "Cotton", "Color_Base": "Earth", "Pattern": "Checkered", "Seasons": ["Autumn", "Winter"], "Temps": ["Cold"], "Weather": ["Dry"]},
    {"Category": "Layer", "Item": "Cashmere Crew | Anthracite", "Tier": "A", "Formality": 2, "Texture": "Heavy_Wool", "Color_Base": "Cool_Grey", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Cold"], "Weather": ["Dry"]},
    {"Category": "Outer", "Item": "Car Coat | Navy Waterproof", "Tier": "A", "Formality": 2, "Texture": "Technical", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Cold"], "Weather": ["Wet"]},
    {"Category": "Footwear", "Item": "Lace up Boots | Brown Leather", "Tier": "A", "Formality": 2, "Texture": "Leather", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Cold"], "Weather": ["Dry"]}
]

def load_data():
    df = pd.DataFrame(RAW_INVENTORY)
    df['Tier_Weight'] = df['Tier'].map({'A': 100, 'B': 40, 'C': 5})
    return df

def get_valid_inventory(df, season, temp, weather, allowed_formalities):
    return df[
        df['Seasons'].apply(lambda x: season in x) &
        df['Temps'].apply(lambda x: temp in x) &
        df['Weather'].apply(lambda x: weather in x) &
        df['Formality'].isin(allowed_formalities)
    ]

# --- 2. LOGIC ---
def get_best_item(valid_pool, category, target_formality, anchor_color, current_outfit_items):
    pool = valid_pool[valid_pool['Category'] == category].copy()
    def calculate_weight(row):
        weight = row['Tier_Weight']
        diff = row['Formality'] - target_formality
        if row['Formality'] == 3 or abs(diff) > 1: return 0
        if diff > 0: weight *= 0.2  
        if row.get('Color_Base') in COLOR_CLASHES.get(anchor_color, []): return 0 
        return weight
    pool['Final_Weight'] = pool.apply(calculate_weight, axis=1)
    pool = pool[pool['Final_Weight'] > 0]
    return pool.sample(n=1, weights='Final_Weight').iloc[0] if not pool.empty else None

def validate_outfit(outfit):
    textures = [outfit[c]['Texture'] for c in ['Bottom', 'Shirt', 'Layer'] if c in outfit]
    counts = pd.Series(textures).value_counts()
    for tex, count in counts.items():
        if tex in FATIGUE_TEXTURES and count > 1: return False
    return True

def generate_full_outfit(df, anchor_name):
    anchor = df[df['Item'] == anchor_name].iloc[0]
    for _ in range(20):
        outfit = {anchor['Category']: anchor}
        slots = [s for s in ['Bottom', 'Shirt', 'Layer', 'Outer', 'Footwear', 'Accessory'] if s != anchor['Category']]
        random.shuffle(slots)
        for slot in slots:
            match = get_best_item(df, slot, anchor['Formality'], anchor.get('Color_Base'), list(outfit.values()))
            if match is not None: outfit[slot] = match
        if validate_outfit(outfit): return outfit
    return None

# --- 3. UI ---
st.title("Daily Outfit Planner")
df = load_data()

with st.sidebar:
    st.header("Conditions")
    season = st.selectbox("Season", ["Autumn", "Winter", "Spring", "Summer"])
    temp = st.selectbox("Temperature", ["Cold", "Temperate", "Warm"])
    weather = st.selectbox("Weather", ["Dry", "Wet"])
    context = st.selectbox("Context", list(CONTEXTS.keys()))
    
    valid_df = get_valid_inventory(df, season, temp, weather, CONTEXTS[context])
    
    if not valid_df.empty:
        anchor = st.selectbox("Pick Anchor", valid_df['Item'].tolist())
        if st.button("Generate Outfit"):
            st.session_state.outfit = generate_full_outfit(valid_df, anchor)
    else:
        st.warning("No items match these conditions.")

if 'outfit' in st.session_state and st.session_state.outfit:
    for cat, item in st.session_state.outfit.items():
        st.write(f"**{cat}**: {item['Item']}")
    if st.button("Are these items clean? (Y)"): st.success("Enjoy.")
    if st.button("No (N)"): st.rerun()