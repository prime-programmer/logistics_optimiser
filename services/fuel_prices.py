import requests 
import streamlit as st

# ─── Fuel Price Fetcher ───────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_fuel_prices():
    """Fetch live UK average fuel prices from the RAC / GovUK open data."""
    try:
        # UK Gov BEIS fuel price data (weekly averages)
        url = "https://www.racfoundation.org/wp-content/uploads/fuel_watch.json"
        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            data = r.json()
            petrol = float(data.get("unleaded", UK_PETROL_FALLBACK * 100)) / 100
            diesel = float(data.get("diesel",   UK_DIESEL_FALLBACK * 100)) / 100
            return petrol, diesel, "RAC Foundation"
    except Exception:
        pass

    # Fallback: UK Gov DESNZ open data
    try:
        url2 = "https://www.gov.uk/government/statistics/weekly-road-fuel-prices"
        # Can't scrape HTML reliably, use hardcoded UK average
        pass
    except Exception:
        pass

    return UK_PETROL_FALLBACK, UK_DIESEL_FALLBACK, "estimated (live fetch failed)"
