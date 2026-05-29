import streamlit as st
import pandas as pd
import random

# --- 1. CONFIGURATION & DATA ---
FORMALITY_MATRIX = {
    (1, 1): 1.0, (1, 2): 0.3, (1, 3): 0.0,
    (2, 1): 0.3, (2, 2): 1.0, (2, 3): 0.3,
    (3, 1): 0.0, (3, 2): 0.3, (3, 3): 1.0
}
S_MAP = {"CORE": [1.0, 1.0, 1.0, 1.0], "AW": [0.2, 0.1, 1.0, 1.0], "SS": [1.0, 1.0, 0.2, 0.1]}
TEXTURE_CLASHES = {"Technical": ["Corduroy", "Linen"], "Corduroy": ["Technical", "Linen"], "Linen": ["Corduroy", "Heavy_Wool", "Technical"], "Heavy_Wool": ["Linen"]}
FATIGUE_TEXTURES = ["Heavy_Wool", "Corduroy", "Denim"]

# [Inventory remains same as provided]
RAW_INVENTORY = [
    {"Category": "Bottom", "Item": "Chinos | Gant", "Tier": "A", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Classic", "Texture": "Cotton"},
    {"Category": "Bottom", "Item": "Jeans | OrSlow 105", "Tier": "A", "Formality": 1, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Workwear", "Texture": "Denim"},
    {"Category": "Shirt", "Item": "Chambray | Morris", "Tier": "A", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Workwear", "Texture": "Cotton"},
    {"Category": "Layer", "Item": "Cashmere | Piecenza", "Tier": "A", "Formality": 2, "CORE": False, "Seasons": S_MAP["AW"], "Style": "Hybrid", "Texture": "Heavy_Wool"},
    {"Category": "Outer", "Item": "Car Coat | UBR", "Tier": "A", "Formality": 2, "CORE": False, "Seasons": S_MAP["AW"], "Style": "Tech", "Texture": "Technical"},
    {"Category": "Footwear", "Item": "Boots | Thursday", "Tier": "A", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Workwear", "Texture": "Leather"},
    {"Category": "Accessory", "Item": "Watch | Alpinist", "Tier": "A", "Formality": 2, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Hybrid", "Texture": "Metal"},
    {"Category": "Suiting", "Item": "Suit | Navy | Skabo", "Tier": "A", "Formality": 3, "CORE": True, "Seasons": S_MAP["CORE"], "Style": "Classic", "Texture": "Fine_Wool"}
]
# ... [Assuming full list from your snippet is loaded here in the real file]

df = pd.DataFrame(RAW_INVENTORY)
df['Tier_Weight'] = df['Tier'].map({'A': 60, 'B': 30, 'C': 10})

# --- 2. LOGIC ---
def generate_full_outfit(anchor_name, season, activity_level):
    s_idx = ["Spring", "Summer", "Autumn", "Winter"].index(season)
    anchor = df[df['Item'] == anchor_name].iloc[0]
    # Adjust target formality based on activity (1=Casual, 3=Formal)
    target_f = 3 if activity_level == "Formal" else (2 if activity_level == "Smart Casual" else 1)
    
    for _ in range(100):
        outfit = {anchor['Category']: anchor}
        slots = ['Bottom', 'Shirt', 'Layer', 'Outer', 'Footwear', 'Accessory']
        for slot in slots:
            if slot in outfit: continue
            # Weighting items that match the target activity formality
            pool = df[df['Category'] == slot].copy()
            def calculate_weight(row):
                f_match = 1.0 if row['Formality'] == target_f else 0.5
                return row['Tier_Weight'] * row['Seasons'][s_idx] * f_match
            pool['W'] = pool.apply(calculate_weight, axis=1)
            outfit[slot] = pool.sample(n=1, weights='W').iloc[0]
        return outfit

# --- 3. UI ---
st.title("Algorithmic Wardrobe")
season = st.sidebar.selectbox("Season", ["Spring", "Summer", "Autumn", "Winter"])
activity = st.sidebar.selectbox("Activity", ["Casual", "Smart Casual", "Formal"])
temp = st.sidebar.slider("Temperature (°C)", -10, 30, 15)
anchor = st.sidebar.selectbox("Pick Anchor", df['Item'].tolist())

if st.sidebar.button("Generate Outfit"):
    st.session_state.outfit = generate_full_outfit(anchor, season, activity)

if 'outfit' in st.session_state and st.session_state.outfit:
    for cat, item in st.session_state.outfit.items():
        st.write(f"**{cat}**: {item['Item']}")
    
    col1, col2 = st.columns(2)
    if col1.button("These items are clean"):
        st.success("Enjoy your day!")
    if col2.button("No, regenerate"):
        st.session_state.outfit = generate_full_outfit(anchor, season, activity)
        st.rerun()