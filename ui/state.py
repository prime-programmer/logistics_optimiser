import streamlit as st
import config

def init_session_state():
    """Initialises all required state variables on first load."""
    defaults = {
        "warehouses": config.DEFAULT_WAREHOUSES.copy(),
        "stores": config.DEFAULT_STORES.copy(),
        "results": None,
        "map_last_click": None,
        "fuel_type": "Diesel",
        "ors_key": "",
        "van_mpg": int(config.MPG_VAN),
        "lorry_mpg": int(config.MPG_LORRY),
        "rs_steps": 2000,
        "hc_steps": 3000,
        "ga_gens": 150,
        "ga_pop": 80,
        "use_tw": False,
        "run_ortools": True
    }
    
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val