import streamlit as st
import pandas as pd
import random

# -----------------------------------------------------------------------------
# 1. DATA ARCHITECTURE & INITIALIZATION
# -----------------------------------------------------------------------------
CONTEXTS = {
    "Work 💼": [2, 3],
    "Restaurant 🍽️": [2],
    "Family Dinner 🏠": [1, 2],
    "Casual Party 🎉": [1, 2],
    "Bar 🍻": [1, 2],
    "Beach 🏖️": [1],
    "Shopping 🛍️": [1, 2],
    "Stage/Formal 🎭": [3]
}

COLOR_CLASHES = {
    "Black": ["Navy", "Brown", "Earth"],
    "Navy": ["Black"],
    "Earth": ["Black", "Cool_Grey"]
}

TEXTURE_CLASHES = {
    "Technical": ["Corduroy", "Linen"],
    "Corduroy": ["Technical", "Linen", "Technical_Synthetic"],
    "Linen": ["Corduroy", "Heavy_Wool", "Technical"],
    "Heavy_Wool": ["Linen"]
}

FATIGUE_TEXTURES = ["Heavy_Wool", "Corduroy", "Denim"]

RAW_INVENTORY = [
    {"Category": "Bottom", "Item": "Chinos | Olive/Juniper Green | Gant", "Tier": "A", "Formality": 2, "Texture": "Cotton", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Bottom", "Item": "Jeans | Dark Indigo | OrSlow 105", "Tier": "A", "Formality": 1, "Texture": "Denim", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Bottom", "Item": "Chinos | Khaki | Lindbergh", "Tier": "B", "Formality": 2, "Texture": "Cotton", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Bottom", "Item": "Wool Pants | Grey Heavily brushed | Oscar Jacobsen", "Tier": "B", "Formality": 2, "Texture": "Heavy_Wool", "Color_Base": "Cool_Grey", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Cold"], "Weather": ["Dry", "Sun", "Wind"]},
    {"Category": "Bottom", "Item": "Technical Chinos | Charcoal Polyester | Lululemon ABC", "Tier": "B", "Formality": 1, "Texture": "Technical", "Color_Base": "Cool_Grey", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Warm", "Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Bottom", "Item": "Jeans | Stonewash | Levis 501", "Tier": "B", "Formality": 1, "Texture": "Denim", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Bottom", "Item": "Linen Shorts | Navy | These Glory Days", "Tier": "B", "Formality": 1, "Texture": "Linen", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Spring", "Summer"], "Temps": ["Warm"], "Weather": ["Dry", "Sun", "Wind"]},
    {"Category": "Bottom", "Item": "Chino Shorts | Khaki | J. Lindbergh", "Tier": "B", "Formality": 1, "Texture": "Cotton", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Summer"], "Temps": ["Warm", "Temperate"], "Weather": ["Dry", "Sun", "Wind"]},
    {"Category": "Bottom", "Item": "Corduroy Pants | Dark Green (Loose Fit) | Massimo Dutti", "Tier": "C", "Formality": 1, "Texture": "Corduroy", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind"]},
    {"Category": "Shirt", "Item": "Chambray Shirt | Light blue | Morris", "Tier": "A", "Formality": 2, "Texture": "Cotton", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Warm", "Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Shirt", "Item": "Cotton/Linen Seersucker Shirt | Off White | Grigio", "Tier": "A", "Formality": 2, "Texture": "Linen", "Color_Base": "Neutral", "Pattern": "Solid", "Seasons": ["Spring", "Summer"], "Temps": ["Warm", "Temperate"], "Weather": ["Dry", "Sun", "Wind"]},
    {"Category": "Shirt", "Item": "Poplin Shirt | Blue Stripe | Zegna", "Tier": "B", "Formality": 2, "Texture": "Cotton", "Color_Base": "Navy", "Pattern": "Stripe", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Warm", "Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Shirt", "Item": "Flannel Shirt | Red Checkered | Boss", "Tier": "B", "Formality": 1, "Texture": "Cotton", "Color_Base": "Earth", "Pattern": "Checkered", "Seasons": ["Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Shirt", "Item": "Linen Shirt | Green/olive | Åhlens", "Tier": "B", "Formality": 1, "Texture": "Linen", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Summer"], "Temps": ["Warm", "Temperate"], "Weather": ["Dry", "Sun", "Wind"]},
    {"Category": "Shirt", "Item": "Colorful 90s Vintage Shirt", "Tier": "B", "Formality": 1, "Texture": "Cotton", "Color_Base": "Earth", "Pattern": "Checkered", "Seasons": ["Spring", "Summer"], "Temps": ["Warm"], "Weather": ["Dry", "Sun", "Wind"]},
    {"Category": "Shirt", "Item": "Polo tee | Navy", "Tier": "B", "Formality": 1, "Texture": "Cotton", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Spring", "Summer"], "Temps": ["Warm", "Temperate"], "Weather": ["Dry", "Sun", "Wind"]},
    {"Category": "Shirt", "Item": "Poplin Shirt | White Tattersall | Laksen", "Tier": "C", "Formality": 2, "Texture": "Cotton", "Color_Base": "Neutral", "Pattern": "Checkered", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Warm", "Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Shirt", "Item": "OCBD | White | Morris", "Tier": "C", "Formality": 2, "Texture": "Cotton", "Color_Base": "Neutral", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Shirt", "Item": "OCBD | Light Grey | Taylor Store", "Tier": "C", "Formality": 2, "Texture": "Cotton", "Color_Base": "Cool_Grey", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Shirt", "Item": "OCBD | Light Blue | J. Lindeberg", "Tier": "C", "Formality": 2, "Texture": "Cotton", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Shirt", "Item": "Poplin Shirt | White | Dressmann", "Tier": "B", "Formality": 3, "Texture": "Cotton", "Color_Base": "Neutral", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Warm", "Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Layer", "Item": "Crew Neck Cashmere | Anthracite | Piecenza", "Tier": "A", "Formality": 2, "Texture": "Heavy_Wool", "Color_Base": "Cool_Grey", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Layer", "Item": "Cotton Sweatshirt | Light Grey | Arket", "Tier": "A", "Formality": 1, "Texture": "Cotton", "Color_Base": "Cool_Grey", "Pattern": "Solid", "Seasons": ["Spring", "Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Layer", "Item": "Corduroy Overshirt | Orange | Wrangler", "Tier": "A", "Formality": 1, "Texture": "Corduroy", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Layer", "Item": "Crew Neck Cashmere | Navy | Piecenza", "Tier": "B", "Formality": 2, "Texture": "Heavy_Wool", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Layer", "Item": "Quarter Zip Merino | Oatmeal | John Smedley", "Tier": "B", "Formality": 2, "Texture": "Heavy_Wool", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Layer", "Item": "Moleskin overshirt | Navy | Portugese Flanell", "Tier": "B", "Formality": 1, "Texture": "Cotton", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Layer", "Item": "Guernsey Sweater | Light Blue", "Tier": "C", "Formality": 1, "Texture": "Heavy_Wool", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Outer", "Item": "Car Coat | Insulated Waterproof Navy | UBR", "Tier": "A", "Formality": 2, "Texture": "Technical", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Outer", "Item": "Waxed Jacket | Brown/Green | Barbour Ashton", "Tier": "B", "Formality": 1, "Texture": "Cotton", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Autumn"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Outer", "Item": "Overcoat | Cashmere Camel | Boss", "Tier": "B", "Formality": 3, "Texture": "Heavy_Wool", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Cold"], "Weather": ["Dry", "Sun", "Wind"]}, 
    {"Category": "Outer", "Item": "Denim Jacket | Light Wash Denim | Levis", "Tier": "B", "Formality": 1, "Texture": "Denim", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Spring", "Summer"], "Temps": ["Warm", "Temperate"], "Weather": ["Dry", "Sun", "Wind"]},
    {"Category": "Outer", "Item": "Technical Harrington | Sand | Scandinavian Edition", "Tier": "B", "Formality": 1, "Texture": "Technical", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn"], "Temps": ["Warm", "Temperate"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Outer", "Item": "Wool Peacoat | Very Dark Navy | 40s Vintage", "Tier": "C", "Formality": 2, "Texture": "Heavy_Wool", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Footwear", "Item": "Lace up Boots | Brown Leather | Thursday Captain", "Tier": "A", "Formality": 2, "Texture": "Leather", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Footwear", "Item": "Suede Leather Sneakers | Clay | Adidas Samba", "Tier": "A", "Formality": 1, "Texture": "Suede", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn"], "Temps": ["Warm", "Temperate"], "Weather": ["Dry", "Sun", "Wind"]},
    {"Category": "Footwear", "Item": "Derby Shoes | Dark Brown | Loake 1880 Leyburn", "Tier": "B", "Formality": 2, "Texture": "Leather", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Warm", "Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind"]},
    {"Category": "Footwear", "Item": "Leather Sneakers | Off-white | Reebook Club C 85", "Tier": "B", "Formality": 1, "Texture": "Leather", "Color_Base": "Neutral", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn"], "Temps": ["Warm", "Temperate"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Footwear", "Item": "Chukka Boots | Brown Suede | Thursday Scout", "Tier": "C", "Formality": 2, "Texture": "Suede", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Autumn"], "Temps": ["Temperate"], "Weather": ["Dry", "Sun", "Wind"]},
    {"Category": "Footwear", "Item": "Chelsea Boots | Black Leather | Thursday Duke", "Tier": "C", "Formality": 2, "Texture": "Leather", "Color_Base": "Black", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Footwear", "Item": "Converse | Low Top White", "Tier": "C", "Formality": 1, "Texture": "Canvas", "Color_Base": "Neutral", "Pattern": "Solid", "Seasons": ["Spring", "Summer"], "Temps": ["Warm", "Temperate"], "Weather": ["Dry", "Sun", "Wind"]},
    {"Category": "Footwear", "Item": "Oxford Shoes | Dark Brown | Crockett & Jones", "Tier": "A", "Formality": 3, "Texture": "Leather", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Warm", "Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind"]},
    {"Category": "Accessory", "Item": "Seiko Alpinist", "Tier": "A", "Formality": 2, "Texture": "Metal", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Warm", "Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Accessory", "Item": "Dress belt | 35mm Dark Brown | Saddler", "Tier": "A", "Formality": 2, "Texture": "Leather", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Warm", "Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Accessory", "Item": "Persol PO3019S", "Tier": "A", "Formality": 2, "Texture": "Plastic", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Warm", "Temperate", "Cold"], "Weather": ["Sun"]},
    {"Category": "Accessory", "Item": "Deerskin Leather Gloves | Dark Brown", "Tier": "A", "Formality": 2, "Texture": "Leather", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Accessory", "Item": "Cashmere wool beanie | Dark grey", "Tier": "B", "Formality": 1, "Texture": "Heavy_Wool", "Color_Base": "Cool_Grey", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Accessory", "Item": "Wool scarf | Dary grey", "Tier": "B", "Formality": 2, "Texture": "Heavy_Wool", "Color_Base": "Cool_Grey", "Pattern": "Solid", "Seasons": ["Autumn", "Winter"], "Temps": ["Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Accessory", "Item": "Grenadine tie | Burgundy | Viola Milano", "Tier": "B", "Formality": 3, "Texture": "Silk", "Color_Base": "Earth", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Warm", "Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]},
    {"Category": "Suit", "Item": "Suit | Navy Sharkskin | Tailored by Skabo", "Tier": "A", "Formality": 3, "Texture": "Fine_Wool", "Color_Base": "Navy", "Pattern": "Solid", "Seasons": ["Spring", "Summer", "Autumn", "Winter"], "Temps": ["Temperate", "Cold"], "Weather": ["Dry", "Sun", "Wind", "Wet"]}
]

@st.cache_data
def load_data():
    df = pd.DataFrame(RAW_INVENTORY)
    tier_weights = {'A': 100, 'B': 40, 'C': 5}
    df['Tier_Weight'] = df['Tier'].map(tier_weights)
    return df

# -----------------------------------------------------------------------------
# 2. ALGORITHM LOGIC
# -----------------------------------------------------------------------------
def get_valid_inventory(df, season, temp, weather, allowed_formalities):
    mask = (
        df['Seasons'].apply(lambda x: season in x) &
        df['Temps'].apply(lambda x: temp in x) &
        df['Weather'].apply(lambda x: weather in x) &
        df['Formality'].isin(allowed_formalities)
    )
    return df[mask]

def get_best_item(valid_pool, category, target_formality, anchor_color, excluded_names, current_outfit_items):
    pool = valid_pool[valid_pool['Category'] == category].copy()
    pool = pool[~pool['Item'].isin(excluded_names)]
    if pool.empty: return None

    current_patterns = sum(1 for item in current_outfit_items if item.get('Pattern', 'Solid') != 'Solid')

    def calculate_final_weight(row):
        weight = row['Tier_Weight']
        formality_diff = abs(row['Formality'] - target_formality)
        item_texture = row.get('Texture', 'Cotton')
        
        if formality_diff == 1: weight *= 0.3 
        elif formality_diff >= 2: return 0
        if row.get('Color_Base') in COLOR_CLASHES.get(anchor_color, []): return 0 
        if row.get('Pattern') != 'Solid' and current_patterns >= 1: weight *= 0.1 
        
        for outfit_item in current_outfit_items:
            if item_texture in TEXTURE_CLASHES.get(outfit_item.get('Texture', 'Cotton'), []):
                return 0 
        return weight

    pool['Final_Weight'] = pool.apply(calculate_final_weight, axis=1)
    pool = pool[pool['Final_Weight'] > 0]
    return pool.sample(n=1, weights='Final_Weight').iloc[0] if not pool.empty else None

def validate_outfit_textures(outfit):
    core_categories = ['Bottom', 'Shirt', 'Layer']
    core_textures = [outfit[cat].get('Texture', 'Cotton') for cat in core_categories if cat in outfit]
    if not core_textures or 'Suit' in outfit: return True
    
    counts = pd.Series(core_textures).value_counts()
    for tex, count in counts.items():
        if tex in FATIGUE_TEXTURES and count > 1: return False
    if len(set(core_textures)) == 1 and core_textures[0] != 'Cotton' and len(core_textures) > 1: return False
    return True

def generate_full_outfit(valid_df, anchor_name, unavailable_items, max_retries=15):
    anchor = valid_df[valid_df['Item'] == anchor_name].iloc[0]
    base_slots = ['Bottom', 'Shirt', 'Layer', 'Outer', 'Footwear', 'Accessory']
    if anchor['Category'] == 'Suit': base_slots = ['Shirt', 'Outer', 'Footwear', 'Accessory']
    
    for _ in range(max_retries):
        outfit = {anchor['Category']: anchor}
        slots = [s for s in base_slots if s != anchor['Category']]
        if "Warm" in anchor['Temps'] and "Layer" in slots: slots.remove("Layer")
        
        random.shuffle(slots)
        for slot in slots:
            match = get_best_item(valid_df, slot, anchor['Formality'], anchor.get('Color_Base', 'Neutral'), [o['Item'] for o in outfit.values()] + unavailable_items, list(outfit.values()))
            if match is not None: outfit[slot] = match
        
        if validate_outfit_textures(outfit): return outfit
    return outfit

# -----------------------------------------------------------------------------
# 3. UI
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Algorithmic Wardrobe", layout="wide")
st.title("Daily Outfit Planner")
df_full = load_data()

with st.sidebar:
    season = st.selectbox("Season", ["Spring", "Summer", "Autumn", "Winter"])
    temp = st.selectbox("Temperature", ["Warm", "Temperate", "Cold"])
    weather = st.selectbox("Weather", ["Dry", "Sun", "Wind", "Wet"])
    context_ui = st.selectbox("Context", list(CONTEXTS.keys()))
    
    valid_inventory = get_valid_inventory(df_full, season, temp, weather, CONTEXTS[context_ui])
    anchor_name = st.selectbox("Pick Your Anchor", valid_inventory['Item'].tolist())
    
    if st.button("Generate Outfit 🎲"):
        st.session_state.outfit = generate_full_outfit(valid_inventory, anchor_name, [])

if 'outfit' in st.session_state and st.session_state.outfit:
    for cat, item in st.session_state.outfit.items():
        st.write(f"**{cat.upper()}**: {item['Item']}")