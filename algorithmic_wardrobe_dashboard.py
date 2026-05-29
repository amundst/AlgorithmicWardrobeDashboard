import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# 1. DATA ARCHITECTURE & INITIALIZATION
# -----------------------------------------------------------------------------
# You didn't provide Pools or Formality in your markdown. I have engineered them 
# into the dataset based on logical assumptions of the items to make the algorithm work.
# Formality Scale: 1 (Casual), 2 (Smart Casual), 3 (Formal)

RAW_INVENTORY = [
    # Bottoms
    {"Category": "Bottom", "Item": "Chinos | Olive/Juniper Green | Gant", "Tier": "A", "Season": "CORE", "Formality": 2, "Pool": ["Main"]},
    {"Category": "Bottom", "Item": "Jeans | Dark Indigo | OrSlow 105", "Tier": "A", "Season": "CORE", "Formality": 1, "Pool": ["Main"]},
    {"Category": "Bottom", "Item": "Chinos | Khaki | Lindbergh", "Tier": "B", "Season": "CORE", "Formality": 2, "Pool": ["Main"]},
    {"Category": "Bottom", "Item": "Wool Pants | Grey Heavily brushed | Oscar Jacobsen", "Tier": "B", "Season": "AW", "Formality": 2, "Pool": ["Main", "Stage"]},
    {"Category": "Bottom", "Item": "Technical Chinos | Charcoal Polyester | Lululemon ABC", "Tier": "B", "Season": "CORE", "Formality": 1, "Pool": ["Main", "At-Home"]},
    {"Category": "Bottom", "Item": "Jeans | Stonewash | Levis 501", "Tier": "B", "Season": "CORE", "Formality": 1, "Pool": ["Main"]},
    {"Category": "Bottom", "Item": "Linen Shorts | Navy | These Glory Days", "Tier": "B", "Season": "SS", "Formality": 1, "Pool": ["Main", "At-Home"]},
    {"Category": "Bottom", "Item": "Chino Shorts | Khaki | J. Lindbergh", "Tier": "B", "Season": "SS", "Formality": 1, "Pool": ["Main", "At-Home"]},
    {"Category": "Bottom", "Item": "Corduroy Pants | Dark Green (Loose Fit) | Massimo Dutti", "Tier": "C", "Season": "AW", "Formality": 1, "Pool": ["Main"]},
    
    # Shirts
    {"Category": "Shirt", "Item": "Chambray Shirt | Light blue | Morris", "Tier": "A", "Season": "CORE", "Formality": 2, "Pool": ["Main"]},
    {"Category": "Shirt", "Item": "Cotton/Linen Seersucker Shirt | Off White | Grigio", "Tier": "A", "Season": "SS", "Formality": 2, "Pool": ["Main"]},
    {"Category": "Shirt", "Item": "Poplin Shirt | Blue Stripe | Zegna", "Tier": "B", "Season": "CORE", "Formality": 2, "Pool": ["Main", "Stage"]},
    {"Category": "Shirt", "Item": "Flannel Shirt | Red Checkered | Boss", "Tier": "B", "Season": "AW", "Formality": 1, "Pool": ["Main"]},
    {"Category": "Shirt", "Item": "Linen Shirt | Green/olive | Åhlens", "Tier": "B", "Season": "SS", "Formality": 1, "Pool": ["Main"]},
    {"Category": "Shirt", "Item": "Colorful 90s Vintage Shirt", "Tier": "B", "Season": "SS", "Formality": 1, "Pool": ["Main", "At-Home"]},
    {"Category": "Shirt", "Item": "Polo tee | Navy", "Tier": "B", "Season": "SS", "Formality": 1, "Pool": ["Main", "At-Home"]},
    {"Category": "Shirt", "Item": "Poplin Shirt | White Tattersall | Laksen", "Tier": "C", "Season": "CORE", "Formality": 2, "Pool": ["Main"]},
    {"Category": "Shirt", "Item": "OCBD | White | Morris", "Tier": "C", "Season": "CORE", "Formality": 2, "Pool": ["Main"]},
    {"Category": "Shirt", "Item": "OCBD | Light Grey | Taylor Store", "Tier": "C", "Season": "CORE", "Formality": 2, "Pool": ["Main"]},
    {"Category": "Shirt", "Item": "OCBD | Light Blue | J. Lindeberg", "Tier": "C", "Season": "CORE", "Formality": 2, "Pool": ["Main"]},
    {"Category": "Shirt", "Item": "Poplin Shirt | White | Dressmann", "Tier": "B", "Season": "CORE", "Formality": 3, "Pool": ["Stage"]}, # Moved from formal

    # Layers
    {"Category": "Layer", "Item": "Crew Neck Cashmere | Anthracite | Piecenza", "Tier": "A", "Season": "AW", "Formality": 2, "Pool": ["Main", "Stage"]},
    {"Category": "Layer", "Item": "Cotton Sweatshirt | Light Grey | Arket", "Tier": "A", "Season": "CORE", "Formality": 1, "Pool": ["Main", "At-Home"]},
    {"Category": "Layer", "Item": "Corduroy Overshirt | Orange | Wrangler", "Tier": "A", "Season": "AW", "Formality": 1, "Pool": ["Main"]},
    {"Category": "Layer", "Item": "Crew Neck Cashmere | Navy | Piecenza", "Tier": "B", "Season": "AW", "Formality": 2, "Pool": ["Main", "Stage"]},
    {"Category": "Layer", "Item": "Quarter Zip Merino | Oatmeal | John Smedley", "Tier": "B", "Season": "CORE", "Formality": 2, "Pool": ["Main"]},
    {"Category": "Layer", "Item": "Moleskin overshirt | Navy | Portugese Flanell", "Tier": "B", "Season": "AW", "Formality": 1, "Pool": ["Main"]},
    {"Category": "Layer", "Item": "Guernsey Sweater | Light Blue", "Tier": "C", "Season": "AW", "Formality": 1, "Pool": ["Main", "At-Home"]},

    # Outerwear
    {"Category": "Outer", "Item": "Car Coat | Insulated Waterproof Navy | UBR", "Tier": "A", "Season": "AW", "Formality": 2, "Pool": ["Main", "Stage"]},
    {"Category": "Outer", "Item": "Waxed Jacket | Brown/Green | Barbour Ashton", "Tier": "B", "Season": "CORE", "Formality": 1, "Pool": ["Main"]},
    {"Category": "Outer", "Item": "Overcoat | Cashmere Camel | Boss", "Tier": "B", "Season": "AW", "Formality": 3, "Pool": ["Main", "Stage"]},
    {"Category": "Outer", "Item": "Denim Jacket | Light Wash Denim | Levis", "Tier": "B", "Season": "SS", "Formality": 1, "Pool": ["Main"]},
    {"Category": "Outer", "Item": "Technical Harrington | Sand | Scandinavian Edition", "Tier": "B", "Season": "SS", "Formality": 1, "Pool": ["Main"]},
    {"Category": "Outer", "Item": "Wool Peacoat | Very Dark Navy | 40s Vintage", "Tier": "C", "Season": "AW", "Formality": 2, "Pool": ["Main"]},

    # Footwear
    {"Category": "Footwear", "Item": "Lace up Boots | Brown Leather | Thursday Captain", "Tier": "A", "Season": "CORE", "Formality": 2, "Pool": ["Main"]},
    {"Category": "Footwear", "Item": "Suede Leather Sneakers | Clay | Adidas Samba", "Tier": "A", "Season": "SS", "Formality": 1, "Pool": ["Main", "At-Home"]},
    {"Category": "Footwear", "Item": "Derby Shoes | Dark Brown | Loake 1880 Leyburn", "Tier": "B", "Season": "CORE", "Formality": 2, "Pool": ["Main", "Stage"]},
    {"Category": "Footwear", "Item": "Leather Sneakers | Off-white | Reebook Club C 85", "Tier": "B", "Season": "SS", "Formality": 1, "Pool": ["Main", "At-Home"]},
    {"Category": "Footwear", "Item": "Chukka Boots | Brown Suede | Thursday Scout", "Tier": "C", "Season": "CORE", "Formality": 2, "Pool": ["Main"]},
    {"Category": "Footwear", "Item": "Chelsea Boots | Black Leather | Thursday Duke", "Tier": "C", "Season": "AW", "Formality": 2, "Pool": ["Main"]},
    {"Category": "Footwear", "Item": "Converse | Low Top White", "Tier": "C", "Season": "SS", "Formality": 1, "Pool": ["Main"]},
    {"Category": "Footwear", "Item": "Oxford Shoes | Dark Brown | Crockett & Jones", "Tier": "A", "Season": "CORE", "Formality": 3, "Pool": ["Stage"]}, # Moved from formal

    # Accessories
    {"Category": "Accessory", "Item": "Seiko Alpinist", "Tier": "A", "Season": "CORE", "Formality": 2, "Pool": ["Main"]},
    {"Category": "Accessory", "Item": "Dress belt | 35mm Dark Brown | Saddler", "Tier": "A", "Season": "CORE", "Formality": 2, "Pool": ["Main", "Stage"]},
    {"Category": "Accessory", "Item": "Persol PO3019S", "Tier": "A", "Season": "CORE", "Formality": 2, "Pool": ["Main", "Stage"]},
    {"Category": "Accessory", "Item": "Deerskin Leather Gloves | Dark Brown", "Tier": "A", "Season": "AW", "Formality": 2, "Pool": ["Main"]},
    {"Category": "Accessory", "Item": "Leather Belt | Dark Brown 35mm | Zara", "Tier": "B", "Season": "CORE", "Formality": 1, "Pool": ["Main"]},
    {"Category": "Accessory", "Item": "Leather Belt | Black 50mm | Levis", "Tier": "B", "Season": "CORE", "Formality": 1, "Pool": ["Main"]},
    {"Category": "Accessory", "Item": "Dress belt | 30mm Black | Zara", "Tier": "B", "Season": "CORE", "Formality": 2, "Pool": ["Main", "Stage"]},
    {"Category": "Accessory", "Item": "Ray ban aviators", "Tier": "B", "Season": "CORE", "Formality": 1, "Pool": ["Main"]},
    {"Category": "Accessory", "Item": "Cashmere wool beanie | Dark grey", "Tier": "B", "Season": "AW", "Formality": 1, "Pool": ["Main"]},
    {"Category": "Accessory", "Item": "Wool scarf | Dary grey", "Tier": "B", "Season": "AW", "Formality": 2, "Pool": ["Main", "Stage"]},
    {"Category": "Accessory", "Item": "Braided Leather Belt | Light Brown 35mm", "Tier": "C", "Season": "SS", "Formality": 1, "Pool": ["Main"]},
    {"Category": "Accessory", "Item": "Grenadine tie | Burgundy | Viola Milano", "Tier": "B", "Season": "CORE", "Formality": 3, "Pool": ["Stage"]},
    {"Category": "Accessory", "Item": "Silk tie | Black", "Tier": "C", "Season": "CORE", "Formality": 3, "Pool": ["Stage"]},

    # Suiting 
    {"Category": "Suit", "Item": "Suit | Navy Sharkskin | Tailored by Skabo", "Tier": "A", "Season": "CORE", "Formality": 3, "Pool": ["Stage"]}
]

@st.cache_data
def load_data():
    df = pd.DataFrame(RAW_INVENTORY)
    # Tier mapping to numerical value for scoring
    tier_weights = {'A': 100, 'B': 50, 'C': 10}
    df['Tier_Score'] = df['Tier'].map(tier_weights)
    return df

# -----------------------------------------------------------------------------
# 2. ALGORITHM LOGIC
# -----------------------------------------------------------------------------
def get_best_item(df, category, anchor_item_series, excluded_names):
    """
    Finds the optimal item for a given category based on constraints and weighted scoring.
    """
    # 1. Hard Filter: Category and Availability
    pool = df[df['Category'] == category]
    pool = pool[~pool['Item'].isin(excluded_names)]
    
    if pool.empty:
        return None

    # 2. Soft Filter / Scoring logic based on Anchor Formality
    anchor_formality = anchor_item_series['Formality']
    
    def calculate_score(row):
        score = row['Tier_Score']
        formality_diff = abs(row['Formality'] - anchor_formality)
        
        # Penalties logic
        if formality_diff == 1:
            score -= 30  # Slight mismatch (e.g. Smart Casual with Casual) is okay, but discouraged
        elif formality_diff >= 2:
            score -= 200 # Severe mismatch (Suit + Converse). Active avoidance.
            
        return score

    pool['Match_Score'] = pool.apply(calculate_score, axis=1)
    
    # Sort by score descending
    pool = pool.sort_values(by='Match_Score', ascending=False)
    
    # Return the top item as a Series
    return pool.iloc[0]

def generate_full_outfit(df, anchor_name, season, pool_context, unavailable_items):
    """Generates a complete outfit around an anchor."""
    # Hard Environment Filtering
    valid_df = df[
        (df['Season'].isin([season, 'CORE'])) & 
        (df['Pool'].apply(lambda pools: pool_context in pools))
    ]
    
    # Extract Anchor
    anchor = valid_df[valid_df['Item'] == anchor_name].iloc[0]
    outfit = {anchor['Category']: anchor}
    
    # Determine which slots to fill
    slots_needed = ['Bottom', 'Shirt', 'Layer', 'Outer', 'Footwear', 'Accessory']
    if anchor['Category'] == 'Suit':
        # Suit overrides Bottom and usually Layer.
        slots_needed = ['Shirt', 'Outer', 'Footwear', 'Accessory']
    else:
        slots_needed.remove(anchor['Category'])

    # Fill slots
    for slot in slots_needed:
        # Exclude currently selected items + marked unavailable items
        current_selection_names = [item['Item'] for item in outfit.values()]
        exclusions = current_selection_names + unavailable_items
        
        best_match = get_best_item(valid_df, slot, anchor, exclusions)
        if best_match is not None:
            outfit[slot] = best_match

    return outfit

# -----------------------------------------------------------------------------
# 3. STATE MANAGEMENT
# -----------------------------------------------------------------------------
def reset_state():
    st.session_state.phase = 'input'
    st.session_state.outfit = {}
    st.session_state.unavailable = []

if 'phase' not in st.session_state:
    st.session_state.phase = 'input'
if 'outfit' not in st.session_state:
    st.session_state.outfit = {}
if 'unavailable' not in st.session_state:
    st.session_state.unavailable = []

# -----------------------------------------------------------------------------
# 4. UI ARCHITECTURE
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Algorithmic Wardrobe", layout="wide")
st.title("Daily Outfit Planner")

df_full = load_data()

# SIDEBAR (Constraints)
with st.sidebar:
    st.header("1. Environmental Constraints")
    # If environment changes, we must reset the outfit state
    season = st.selectbox("Season / Weather", ["SS", "AW"], on_change=reset_state)
    pool_context = st.selectbox("Context / Pool", ["Main", "At-Home", "Stage"], on_change=reset_state)
    
    st.header("2. Build Parameters")
    # Filter valid anchors based on constraints
    valid_anchors_df = df_full[
        (df_full['Season'].isin([season, 'CORE'])) & 
        (df_full['Pool'].apply(lambda x: pool_context in x))
    ]
    
    anchor_name = st.selectbox("Anchor Item", valid_anchors_df['Item'].tolist(), on_change=reset_state)
    
    if st.button("Generate Outfit", type="primary", use_container_width=True):
        st.session_state.unavailable = [] # Reset on fresh generation
        st.session_state.outfit = generate_full_outfit(df_full, anchor_name, season, pool_context, st.session_state.unavailable)
        st.session_state.phase = 'generated'

# MAIN DASHBOARD
if st.session_state.phase in ['generated', 'pivot']:
    
    st.subheader("Generated Configuration")
    
    # Display the outfit cleanly using columns
    categories = ['Suit', 'Outer', 'Layer', 'Shirt', 'Bottom', 'Footwear', 'Accessory']
    
    for cat in categories:
        if cat in st.session_state.outfit:
            item_data = st.session_state.outfit[cat]
            # Use styling to distinguish Tier levels
            tier = item_data['Tier']
            color = "green" if tier == "A" else "orange" if tier == "B" else "red"
            
            st.markdown(f"""
            <div style='padding: 10px; border-left: 4px solid {color}; background-color: #f9f9f9; margin-bottom: 10px; border-radius: 4px; color: black;'>
                <strong style='color: #333;'>{cat.upper()}</strong><br>
                {item_data['Item']} <i>(Tier: {tier})</i>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # PHASE: CHECK
    if st.session_state.phase == 'generated':
        st.subheader("Availability Check")
        st.write("Are all of these items clean, ironed, and currently available?")
        
        col1, col2 = st.columns(2)
        if col1.button("Yes - Lock it in", use_container_width=True):
            st.success("Outfit locked. End of sequence.")
            st.balloons()
            
        if col2.button("No - Pivot needed", use_container_width=True):
            st.session_state.phase = 'pivot'
            st.rerun()

    # PHASE: PIVOT
    elif st.session_state.phase == 'pivot':
        st.subheader("Recalibration Protocol")
        
        # Don't allow replacing the anchor
        current_items = [v['Item'] for k, v in st.session_state.outfit.items() if v['Item'] != anchor_name]
        
        if not current_items:
            st.warning("Only the anchor remains. Change constraints to generate a new outfit.")
        else:
            missing_item_name = st.selectbox("Which item is unavailable?", current_items)
            
            if st.button("Recalculate Slot", type="secondary"):
                # Mark as unavailable globally
                st.session_state.unavailable.append(missing_item_name)
                
                # Identify the category of the missing item
                missing_cat = df_full[df_full['Item'] == missing_item_name].iloc[0]['Category']
                
                # Remove from current outfit
                del st.session_state.outfit[missing_cat]
                
                # Fetch new item for that slot
                exclusions = [v['Item'] for v in st.session_state.outfit.values()] + st.session_state.unavailable
                anchor_data = st.session_state.outfit.get(
                    df_full[df_full['Item'] == anchor_name].iloc[0]['Category'], 
                    df_full[df_full['Item'] == anchor_name].iloc[0]
                )
                
                new_item = get_best_item(
                    df_full[
                        (df_full['Season'].isin([season, 'CORE'])) & 
                        (df_full['Pool'].apply(lambda x: pool_context in x))
                    ], 
                    missing_cat, 
                    anchor_data, 
                    exclusions
                )
                
                if new_item is not None:
                    st.session_state.outfit[missing_cat] = new_item
                    st.success(f"Slot recalculated. {missing_item_name} has been replaced.")
                else:
                    st.error(f"No suitable replacements found for {missing_cat} under current constraints.")
                
                # Return to generated phase
                st.session_state.phase = 'generated'
                st.rerun()

elif st.session_state.phase == 'input':
    st.info("Set your constraints in the sidebar and hit 'Generate Outfit' to begin the sequence.")