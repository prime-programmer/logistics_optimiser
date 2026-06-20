import streamlit as st
from streamlit_folium import st_folium
from visualisation.maps import build_map
from visualisation.dashboard import render_results_metrics, render_route_breakdown

def render_results_tab():
    res = st.session_state.results
    if res is None:
        st.info("Run the optimiser first.")
        return

    # Render metrics
    render_results_metrics(res, st.session_state.van_mpg, st.session_state.lorry_mpg)

    # Render interactive map
    m_result = build_map(
        locations=res["all_loc_map"], 
        warehouses=st.session_state.warehouses, 
        stores=st.session_state.stores, 
        routes_w1=res["routes_w1"], 
        routes_w2=res["routes_w2"]
    )
    st_folium(m_result, width=900, height=520, returned_objects=[])

    # Render Breakdown & Convergence
    render_route_breakdown(res, st.session_state.van_mpg, st.session_state.lorry_mpg)
    
    st.markdown("### Convergence")
    chart_data = {
        "RS": res["rs_hist"],
        "HC": res["hc_hist"],
        "GA": res["ga_hist"],
    }
    st.line_chart(chart_data)