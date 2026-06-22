import streamlit as st
import config
from services.fuel_prices import fetch_fuel_prices

def render_sidebar():
    with st.sidebar:
        st.title("⚙️ Settings")

        # 1. Check if keys exist securely in the background
        has_ors_secret = "ORS_API_KEY" in st.secrets
        has_fuel_secret = "FUEL_CLIENT_ID" in st.secrets and "FUEL_CLIENT_SECRET" in st.secrets

        # 2. OpenRouteService Settings
        if not has_ors_secret:
            st.text_input(
                "OpenRouteService API Key", 
                type="password", 
                key="ors_key_input", 
                help="Free at openrouteservice.org"
            )
            st.session_state.ors_key = st.session_state.get("ors_key_input", "")
        else:
            # Load secretly and show a clean success badge instead of an input box
            st.session_state.ors_key = st.secrets["ORS_API_KEY"]
            st.success("✅ Map Routing Connected")

        # 3. Gov.UK Fuel Settings
        st.subheader("⛽ Fuel Finder API")
        if not has_fuel_secret:
            client_id = st.text_input("Client ID", type="password")
            client_secret = st.text_input("Client Secret", type="password")
        else:
            client_id = st.secrets["FUEL_CLIENT_ID"]
            client_secret = st.secrets["FUEL_CLIENT_SECRET"]
            st.success("✅ Gov.UK Live Prices Connected")

        st.subheader("🚗 Fuel Type")
        st.selectbox("Select fuel type", ["Diesel", "Petrol"], key="fuel_type")

        # Fetch live fuel prices using the securely loaded keys
        petrol_price, diesel_price, fuel_source = fetch_fuel_prices(
            client_id=client_id,
            client_secret=client_secret
        )
        
        st.info(f"UK avg prices ({fuel_source}):\n\n⛽ Petrol: £{petrol_price:.3f}/L\n🛢️ Diesel: £{diesel_price:.3f}/L")

        active_price = diesel_price if st.session_state.fuel_type == "Diesel" else petrol_price
        st.metric("Active fuel price", f"£{active_price:.3f}/L")
        
        # Save to state for the optimiser and cost engine to access
        st.session_state.active_price = active_price

        st.slider("Van MPG", 15, 60, int(config.MPG_VAN), step=1, key="van_mpg")
        st.slider("Lorry MPG", 10, 40, int(config.MPG_LORRY), step=1, key="lorry_mpg")

        # Calculate active cost per mile
        def active_cost_per_mile(mpg):
            litres_pm = config.LITRES_PER_GALLON / mpg
            return active_price * litres_pm

        st.session_state.van_rate_live = active_cost_per_mile(st.session_state.van_mpg)
        st.session_state.lorry_rate_live = active_cost_per_mile(st.session_state.lorry_mpg)

        st.markdown(f"**Van:** £{st.session_state.van_rate_live:.4f}/mile | **Lorry:** £{st.session_state.lorry_rate_live:.4f}/mile")

        st.subheader("🧬 Algorithm Iterations")
        st.slider("Random Search steps", 500, 10000, 2000, step=500, key="rs_steps")
        st.slider("Hill Climbing steps", 500, 10000, 3000, step=500, key="hc_steps")
        st.slider("GA generations", 50, 500, 150, step=25, key="ga_gens")
        st.slider("GA population", 20, 200, 80, step=10, key="ga_pop")

        st.subheader("🕐 Time Windows (optional)")
        use_tw = st.checkbox("Enable time windows", value=False, key="use_tw")
        if use_tw:
            st.info("Set per-store delivery windows below (or leave as 0–24 for unrestricted).")

        st.checkbox("Compare with OR-Tools benchmark", value=True, key="run_ortools")