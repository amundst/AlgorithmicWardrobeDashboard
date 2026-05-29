import streamlit as st
import pandas as pd
import random

# --- 1. CONFIGURATION ---
CONTEXTS = {
    "Work 💼": 2, "Restaurant 🍽️": 2, "Family Dinner 🏠": 2,
    "Casual Party 🎉": 1, "Bar 🍻": 1, "Beach 🏖️": 1,
    "Shopping 🛍️": 1, "Stage/Formal 🎭": 3
}

TEXTURE_CLASHES = {"Technical": ["Corduroy", "Linen"], "Corduroy": ["Technical", "Linen"], "Linen": ["Corduroy", "Heavy_Wool"], "Heavy_Wool": ["Linen"]}
FATIGUE_TEXTURES = ["Heavy_Wool", "Corduroy", "Denim"]

# Formality suitability: (Anchor, Item)
FORMALITY_MATRIX = {
    (1, 1): 1.0, (1, 2): 0.3, (1, 3): 0.0,
    (2, 1): 0.3, (2, 2): 1.0, (2, 3): 0.3,
    (3, 1): 0.0, (3, 2): 0.3, (3, 3): 1.0
}

# --- 2. FULL INVENTORY ---
RAW_INVENTORY = [
    # Bottoms
    {"Category": "Bottom", "Item": "Chinos | Olive Green", "Tier": "A", "Formality": 2, "Texture": "Cotton", "Style": "Classic", "CORE": True},
    {"Category": "Bottom", "Item": "Jeans | Indigo", "Tier": "A", "Formality": 1, "Texture": "Denim", "Style": "Workwear", "CORE": True},
    {"Category": "Bottom", "Item": "Chinos | Khaki", "Tier": "B", "Formality": 2, "Texture": "Cotton", "Style": "Classic", "CORE": True},
    {"Category": "Bottom", "Item": "Wool Pants | Grey", "Tier": "B", "Formality": 3, "Texture": "Heavy_Wool", "Style": "Classic", "CORE": False},
    {"Category": "Bottom", "Item": "Technical Chinos | Charcoal", "Tier": "B", "Formality": 2, "Texture": "Technical", "Style": "Tech", "CORE": True},
    {"Category": "Bottom", "Item": "Jeans | Stonewash", "Tier": "B", "Formality": 1, "Texture": "Denim", "Style": "Workwear", "CORE": True},
    {"Category": "Bottom", "Item": "Linen Shorts | Navy", "Tier": "B", "Formality": 1, "Texture": "Linen", "Style": "Classic", "CORE": False},
    {"Category": "Bottom", "Item": "Chino Shorts | Khaki", "Tier": "B", "Formality": 1, "Texture": "Cotton", "Style": "Classic", "CORE": False},
    {"Category": "Bottom", "Item": "Corduroy | Dark Green", "Tier": "C", "Formality": 2, "Texture": "Corduroy", "Style": "Workwear", "CORE": False},
    # Shirts
    {"Category": "Shirt", "Item": "Chambray | Morris", "Tier": "A", "Formality": 2, "Texture": "Cotton", "Style": "Workwear", "CORE": True},
    {"Category": "Shirt", "Item": "Seersucker | Grigio", "Tier": "A", "Formality": 2, "Texture": "Linen", "Style": "Classic", "CORE": False},
    {"Category": "Shirt", "Item": "Poplin | Blue Stripe", "Tier": "B", "Formality": 2, "Texture": "Cotton", "Style": "Classic", "CORE": True},
    {"Category": "Shirt", "Item": "Flannel | Boss", "Tier": "B", "Formality": 1, "Texture": "Cotton", "Style": "Workwear", "CORE": False},
    {"Category": "Shirt", "Item": "Linen | Åhlens", "Tier": "B", "Formality": 1, "Texture": "Linen", "Style": "Classic", "CORE": False},
    {"Category": "Shirt", "Item": "Vintage Shirt", "Tier": "B", "Formality": 1, "Texture": "Cotton", "Style": "Workwear", "CORE": False},
    {"Category": "Shirt", "Item": "Polo | Navy", "Tier": "B", "Formality": 1, "Texture": "Cotton", "Style": "Classic", "CORE": False},
    {"Category": "Shirt", "Item": "Poplin | Tattersall", "Tier": "C", "Formality": 2, "Texture": "Cotton", "Style": "Classic", "CORE": True},
    {"Category": "Shirt", "Item": "OCBD | White", "Tier": "C", "Formality": 2, "Texture": "Cotton", "Style": "Classic", "CORE": True},
    {"Category": "Shirt", "Item": "OCBD | Light Grey", "Tier": "C", "Formality": 2, "Texture": "Cotton", "Style": "Classic", "CORE": True},
    {"Category": "Shirt", "Item": "OCBD | Blue", "Tier": "C", "Formality": 2, "Texture": "Cotton", "Style": "Classic", "CORE": True},
    # Layers
    {"Category": "Layer", "Item": "Cashmere | Anthracite", "Tier": "A", "Formality": 2, "Texture": "Heavy_Wool", "Style": "Classic", "CORE": False},
    {"Category": "Layer", "Item": "Sweatshirt | Arket", "Tier": "A", "Formality": 1, "Texture": "Cotton", "Style": "Workwear", "CORE": True},
    {"Category": "Layer", "Item": "Corduroy Overshirt", "Tier": "A", "Formality": 1, "Texture": "Corduroy", "Style": "Workwear", "CORE": False},
    {"Category": "Layer", "Item": "Merino Zip", "Tier": "B", "Formality": 2, "Texture": "Heavy_Wool", "Style": "Classic", "CORE": True},
    {"Category": "Layer", "Item": "Moleskin Overshirt", "Tier": "B", "Formality": 1, "Texture": "Cotton", "Style": "Workwear", "CORE": False},
    {"Category": "Layer", "Item": "Guernsey | Blue", "Tier": "C", "Formality": 1, "Texture": "Heavy_Wool", "Style": "Workwear", "CORE": False},
    # Outer
    {"Category": "Outer", "Item": "Car Coat | UBR", "Tier": "A", "Formality": 2, "Texture": "Technical", "Style": "Tech", "CORE": False},
    {"Category": "Outer", "Item": "Waxed Jacket | Barbour", "Tier": "B", "Formality": 1, "Texture": "Cotton", "Style": "Workwear", "CORE": True},
    {"Category": "Outer", "Item": "Overcoat | Camel", "Tier": "B", "Formality": 3, "Texture": "Heavy_Wool", "Style": "Classic", "CORE": False},
    {"Category": "Outer", "Item": "Denim Jacket", "Tier": "B", "Formality": 1, "Texture": "Denim", "Style": "Workwear", "CORE": False},
    {"Category": "Outer", "Item": "Harrington", "Tier": "B", "Formality": 1, "Texture": "Technical", "Style": "Tech", "CORE": False},
    {"Category": "Outer", "Item": "Peacoat", "Tier": "C", "Formality": 2, "Texture": "Heavy_Wool", "Style": "Workwear", "CORE": False},
    # Footwear
    {"Category": "Footwear", "Item": "Boots | Thursday", "Tier": "A", "Formality": 2, "Texture": "Leather", "Style": "Workwear", "CORE": True},
    {"Category": "Footwear", "Item": "Sneakers | Samba", "Tier": "A", "Formality": 1, "Texture": "Leather", "Style": "Workwear", "CORE": False},
    {"Category": "Footwear", "Item": "Derby | Loake", "Tier": "B", "Formality": 2, "Texture": "Leather", "Style": "Classic", "CORE": True},
    {"Category": "Footwear", "Item": "Sneakers | Reebok", "Tier": "B", "Formality": 1, "Texture": "Leather", "Style": "Workwear", "CORE": False},
    {"Category": "Footwear", "Item": "Chukka | Thursday", "Tier": "C", "Formality": 2, "Texture": "Suede", "Style": "Workwear", "CORE": True},
    {"Category": "Footwear", "Item": "Chelsea | Duke", "Tier": "C", "Formality": 2, "Texture": "Leather", "Style": "Classic", "CORE": False},
    {"Category": "Footwear", "Item": "Converse", "Tier": "C", "Formality": 1, "Texture": "Canvas", "Style": "Workwear", "CORE": False},
    # Accessories
    {"Category": "Accessory", "Item": "Watch | Alpinist", "Tier": "A", "Formality": 2, "Texture": "Metal", "Style": "Classic", "CORE": True},
    {"Category": "Accessory", "Item": "Belt | Saddler", "Tier": "A", "Formality": 2, "Texture": "Leather", "Style": "Classic", "CORE": True},
    {"Category": "Accessory", "Item": "Glasses | Persol", "Tier": "A", "Formality": 1, "Texture": "Plastic", "Style": "Classic", "CORE": True},
    {"Category": "Accessory", "Item": "Gloves | Amanda C", "Tier": "A", "Formality": 2, "Texture": "Leather", "Style": "Classic", "CORE": False},
    {"Category": "Accessory", "Item": "Beanie", "Tier": "B", "Formality": 1, "Texture": "Heavy_Wool", "Style": "Classic", "CORE": False},
    {"Category": "Accessory", "Item": "Scarf", "Tier": "B", "Formality": 2, "Texture": "Heavy_Wool", "Style": "Classic", "CORE": False},
    # Suiting
    {"Category": "Suiting", "Item": "Suit | Skabo", "Tier": "A", "Formality": 3, "Texture": "Fine_Wool", "Style": "Classic", "CORE": True},
    {"Category": "Suiting", "Item": "Oxford Shoes", "Tier": "A", "Formality": 3, "Texture": "Leather", "Style": "Classic", "CORE": True}
]

df = pd.DataFrame(RAW_INVENTORY)
df['Tier_Weight'] = df['Tier'].map({'A': 60, 'B': 30, 'C': 10})

# --- 3. LOGIC ---
def get_best_item(category, anchor, target_temp, target_weather, excluded):
    pool = df[(df['Category'] == category) & (~df['Item'].isin(excluded))].copy()
    if pool.empty: return None
    
    def calculate_weight(row):
        # Environmental logic
        w_score = 1.0 if (target_weather == "Wet" and row['Texture'] in ["Technical", "Leather"]) else 0.5
        t_score = 1.0 if (target_temp < 10 and row['Texture'] in ["Heavy_Wool"]) or (target_temp > 20 and row['Texture'] in ["Linen", "Cotton"]) else 0.5
        
        f_score = FORMALITY_MATRIX.get((anchor['Formality'], row['Formality']), 0.0)
        s_score = 1.8 if row['Style'] == anchor['Style'] else 0.1
        
        return row['Tier_Weight'] * w_score * t_score * f_score * s_score
    
    pool['W'] = pool.apply(calculate_weight, axis=1)
    return pool.sample(n=1, weights='W').iloc[0] if pool['W'].sum() > 0 else None

def generate_full_outfit(anchor_name, temp, weather):
    anchor = df[df['Item'] == anchor_name].iloc[0]
    for _ in range(50):
        outfit = {anchor['Category']: anchor}
        for slot in ['Bottom', 'Shirt', 'Layer', 'Outer', 'Footwear', 'Accessory']:
            if slot in outfit: continue
            match = get_best_item(slot, anchor, temp, weather, [o['Item'] for o in outfit.values()])
            if match is not None: outfit[slot] = match
        # Validation
        texs = [o['Texture'] for o in outfit.values() if o['Category'] in ['Bottom', 'Shirt', 'Layer']]
        if len(set(texs)) == len(texs) or 'Cotton' in texs: return outfit
    return None

# --- 4. UI ---
st.title("Algorithmic Wardrobe")
temp = st.sidebar.slider("Temperature (°C)", -20, 30, 15)
weather = st.sidebar.selectbox("Weather", ["Dry", "Wet"])
activity = st.sidebar.selectbox("Context", list(CONTEXTS.keys()))
anchor = st.sidebar.selectbox("Pick Anchor", df['Item'].tolist())

if st.sidebar.button("Generate"):
    st.session_state.outfit = generate_full_outfit(anchor, temp, weather)

if 'outfit' in st.session_state and st.session_state.outfit:
    for cat, item in st.session_state.outfit.items(): st.write(f"**{cat}**: {item['Item']}")
    if st.button("Are these items clean? (Y)"): st.success("Enjoy.")
    if st.button("No (N)"): 
        st.session_state.outfit = generate_full_outfit(anchor, temp, weather)
        st.rerun()