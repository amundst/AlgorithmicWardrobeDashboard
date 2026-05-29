import streamlit as st
import pandas as pd
import sqlite3
import random

# --- 1. DATABASE & INIT ---
def init_db():
    conn = sqlite3.connect('wardrobe.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY, item TEXT, category TEXT, 
                    tier TEXT, formality INTEGER, texture TEXT, 
                    color_base TEXT, pattern TEXT, seasons TEXT, 
                    temps TEXT, weather TEXT)''')
    conn.commit()
    conn.close()

def load_data():
    conn = sqlite3.connect('wardrobe.db')
    df = pd.read_sql_query("SELECT * FROM inventory", conn)
    conn.close()
    tier_weights = {'A': 100, 'B': 40, 'C': 5}
    df['Tier_Weight'] = df['Tier'].map(tier_weights)
    return df

# --- 2. ALGORITHM LOGIC ---
def get_best_item(valid_pool, category, target_formality, anchor_color, current_outfit_items):
    pool = valid_pool[valid_pool['Category'] == category].copy()
    
    def calculate_weight(row):
        weight = row['Tier_Weight']
        diff = row['Formality'] - target_formality
        
        # Impossible transitions
        if row['Formality'] == 3 or abs(diff) > 1: return 0
        # directional probability: harder to dress up (diff > 0) than down (diff < 0)
        if diff > 0: weight *= 0.2 
        
        if row.get('Color_Base') in COLOR_CLASHES.get(anchor_color, []): return 0 
        return weight

    pool['Final_Weight'] = pool.apply(calculate_weight, axis=1)
    pool = pool[pool['Final_Weight'] > 0]
    return pool.sample(n=1, weights='Final_Weight').iloc[0] if not pool.empty else None

# --- 3. UI & APPROVAL FLOW ---
st.title("Daily Outfit Planner")
if 'outfit' not in st.session_state: st.session_state.outfit = None

if st.session_state.outfit:
    st.write("### Your Generated Outfit:")
    for cat, item in st.session_state.outfit.items():
        st.write(f"**{cat.upper()}**: {item['item']}")
    
    if st.button("Are all items clean and ready to use? (Y)"):
        st.success("Great! Have a good day.")
    if st.button("No, generate another (N)"):
        # Logic to re-trigger generation
        st.rerun()

# --- 4. DATA MIGRATION ---
# Call init_db() on first run to build the SQLite foundation.