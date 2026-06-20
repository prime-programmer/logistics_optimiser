# app.py
import streamlit as st

from ui.state import init_session_state
from ui.sidebar import render_sidebar
from ui.optimise import render_optimise_section
from ui.tabs.map_tab import render_map_tab
from ui.tabs.locations_tab import render_locations_tab
from ui.tabs.results_tab import render_results_tab
from ui.tabs.compare_tab import render_compare_tab

# Page Config & Initial State
st.set_page_config(page_title="Delivery Route Optimiser", page_icon="🚚", layout="wide")
init_session_state()

# Render Sidebar
render_sidebar()

# Main Application Body
st.title("🚚 Delivery Route Optimiser")
st.caption("Place warehouses & stores on the map, then click **Optimise** to find the best routes.")

# The Execution Engine Trigger
render_optimise_section()

# The View Tabs
tab_map, tab_loc, tab_res, tab_comp = st.tabs([
    "🗺️ Map", "📍 Locations", "📊 Results", "🔬 Comparison"
])

with tab_map:
    render_map_tab()
with tab_loc:
    render_locations_tab()
with tab_res:
    render_results_tab()
with tab_comp:
    render_compare_tab()