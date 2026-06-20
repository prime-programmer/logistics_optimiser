import streamlit as st
from visualisation.dashboard import render_comparison_tables

def render_compare_tab():
    res = st.session_state.results
    if res is None:
        st.info("Run the optimiser first.")
        return
        
    render_comparison_tables(res, st.session_state.van_mpg, st.session_state.lorry_mpg)