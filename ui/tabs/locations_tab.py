import streamlit as st
import random

def render_locations_tab():
    st.subheader("Warehouses")
    for wname in list(st.session_state.warehouses.keys()):
        lat, lon = st.session_state.warehouses[wname]
        c1, c2, c3, c4 = st.columns([1, 2, 2, 1])
        c1.markdown(f"**{wname}**")
        new_lat = c2.number_input(f"Lat {wname}", value=lat, format="%.5f", key=f"wlat_{wname}")
        new_lon = c3.number_input(f"Lon {wname}", value=lon, format="%.5f", key=f"wlon_{wname}")
        st.session_state.warehouses[wname] = (new_lat, new_lon)

    st.markdown("---")
    st.subheader("Stores")
    st.session_state.tw_windows = {}
    
    for sid in sorted(st.session_state.stores.keys()):
        lat, lon = st.session_state.stores[sid]
        cols = st.columns([1, 2, 2, 2, 2, 1])
        cols[0].markdown(f"**{sid}**")
        new_lat = cols[1].number_input(f"Lat {sid}", value=lat, format="%.5f", key=f"slat_{sid}")
        new_lon = cols[2].number_input(f"Lon {sid}", value=lon, format="%.5f", key=f"slon_{sid}")
        
        if st.session_state.use_tw:
            tw_start = cols[3].number_input(f"Open {sid}", 0, 23, 8, key=f"tw_s_{sid}")
            tw_end   = cols[4].number_input(f"Close {sid}", 0, 24, 18, key=f"tw_e_{sid}")
            st.session_state.tw_windows[sid] = (tw_start, tw_end)
            
        if cols[-1].button("❌", key=f"del_{sid}"):
            del st.session_state.stores[sid]
            st.rerun()
            
        st.session_state.stores[sid] = (new_lat, new_lon)

    if st.button("➕ Add store at default position"):
        new_id = max(st.session_state.stores.keys(), default=0) + 1
        st.session_state.stores[new_id] = (52.0 + random.uniform(-0.5, 0.5), 0.5 + random.uniform(-0.5, 0.5))
        st.rerun()