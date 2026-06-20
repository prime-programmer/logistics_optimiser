import streamlit as st
import folium
from streamlit_folium import st_folium
import config

def render_map_tab():
    col_map, col_ctrl = st.columns([3, 1])
    
    with col_ctrl:
        st.subheader("Add locations")
        add_mode = st.radio("Next click adds:", ["Store", "Warehouse W1", "Warehouse W2"])
        st.caption("Click on the map to add a location.")
        
        if st.button("🗑️ Reset to defaults"):
            st.session_state.warehouses = config.DEFAULT_WAREHOUSES.copy()
            st.session_state.stores = config.DEFAULT_STORES.copy()
            st.session_state.results = None
            st.rerun()
            
        st.markdown("---")
        st.markdown(f"**Warehouses:** {len(st.session_state.warehouses)}")
        st.markdown(f"**Stores:** {len(st.session_state.stores)}")

    with col_map:
        all_locs = {**st.session_state.warehouses, **st.session_state.stores}
        if all_locs:
            all_lats = [v[0] for v in all_locs.values()]
            all_lons = [v[1] for v in all_locs.values()]
            centre = [sum(all_lats)/len(all_lats), sum(all_lons)/len(all_lons)]
        else:
            centre = [52.0, 0.5]

        m_preview = folium.Map(location=centre, zoom_start=7, tiles="CartoDB positron")
        
        for wname, (lat, lon) in st.session_state.warehouses.items():
            folium.Marker([lat, lon], popup=wname, 
                          icon=folium.Icon(color="red", icon="home", prefix="fa")).add_to(m_preview)
                          
        for sname, (lat, lon) in st.session_state.stores.items():
            folium.CircleMarker([lat, lon], radius=7, color=config.COLOURS["store"], 
                                fill=True, fill_opacity=0.9, popup=f"Store {sname}").add_to(m_preview)

        map_data = st_folium(m_preview, width=700, height=480, returned_objects=["last_clicked"])

        if map_data and map_data.get("last_clicked"):
            click = map_data["last_clicked"]
            lat, lon = click["lat"], click["lng"]
            key = (round(lat, 5), round(lon, 5))
            
            if key != st.session_state.map_last_click:
                st.session_state.map_last_click = key
                if add_mode == "Store":
                    new_id = max(st.session_state.stores.keys(), default=0) + 1
                    st.session_state.stores[new_id] = (lat, lon)
                elif add_mode == "Warehouse W1":
                    st.session_state.warehouses["W1"] = (lat, lon)
                else:
                    st.session_state.warehouses["W2"] = (lat, lon)
                st.rerun()