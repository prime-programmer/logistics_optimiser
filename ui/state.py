import streamlit as st
import config

def init_session_state():
    """Initialises non-widget state variables on first load."""
    defaults = {
        "warehouses": config.DEFAULT_WAREHOUSES.copy(),
        "stores": config.DEFAULT_STORES.copy(),
        "results": None,
        "map_last_click": None,
        
    }
    
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val