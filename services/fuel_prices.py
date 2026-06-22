import streamlit as st
import requests
import config

@st.cache_data(ttl=3600)
def fetch_fuel_prices(client_id=None, client_secret=None):
    """Fetch live UK fuel prices from the official Gov.UK Fuel Finder API."""
    
    if not client_id or not client_secret:
        return config.UK_PETROL_FALLBACK, config.UK_DIESEL_FALLBACK, "estimated (Missing Gov.UK API keys)"
        
    try:
        # Step 1: Request an OAuth 2.0 Access Token
        token_url = "https://www.fuel-finder.service.gov.uk/api/v1/oauth/generate_access_token"
        auth_payload = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
        
        # Force standard Form-Encoded payload for OAuth2
        token_req = requests.post(token_url, data=auth_payload, headers={"Accept": "application/json"}, timeout=5)
        
        if token_req.status_code != 200:
            print(f"\n--- FUEL API AUTH HARD ERROR: {token_req.status_code} ---")
            return config.UK_PETROL_FALLBACK, config.UK_DIESEL_FALLBACK, "estimated (Gov.UK Auth Failed)"
            
        response_json = token_req.json()
        
        # Tell Python to look inside the nested 'data' dictionary
        access_token = response_json.get("data", {}).get("access_token")
        
        if not access_token:
            print(f"\n--- FUEL API EMPTY TOKEN WARNING ---")
            print(f"Server Response: {token_req.text}\n------------------------------------\n")
            return config.UK_PETROL_FALLBACK, config.UK_DIESEL_FALLBACK, "estimated (No Token Returned)"
        
        # Step 2: Fetch the live prices using the Bearer Token
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        prices_url = "https://www.fuel-finder.service.gov.uk/api/v1/pfs/fuel-prices" 
        
        # request batch 1 to satisfy the Gov.UK API constraints
        prices_url = "https://www.fuel-finder.service.gov.uk/api/v1/pfs/fuel-prices" 
        r = requests.get(prices_url, headers=headers, params={"batch-number": 1}, timeout=10)
        
        if r.status_code != 200:
            print(f"\n--- FUEL DATA HTTP ERROR: {r.status_code} ---")
            print(f"Response: {r.text}\n---------------------------------\n")
            return config.UK_PETROL_FALLBACK, config.UK_DIESEL_FALLBACK, f"estimated (Data Fetch Failed: {r.status_code})"
            
        data = r.json()
        
        petrol_prices = []
        diesel_prices = []
            
        def normalize_price(p):
            """Cleans retailer pricing inconsistencies (Pounds vs Pence vs Tenths of a penny)."""
            try:
                val = float(p)
                if val == 0: return None
                if val < 5.0: return val               # Pounds (e.g., 1.45)
                if val > 1000.0: return val / 1000.0   # Tenths of pence (e.g., 1450)
                return val / 100.0                     # Pence (e.g., 145.0)
            except (ValueError, TypeError):
                return None
        
        # Navigate the JSON structure securely
        # Navigate the JSON structure securely
        stations = data.get("stations", data) if isinstance(data, dict) else data
        if isinstance(stations, dict) and "data" in stations:
            stations = stations["data"]
            
        if not isinstance(stations, list):
            stations = []

        for station in stations:
            # Gov.UK strictly uses the 'fuel_prices' list
            fuel_prices = station.get("fuel_prices", [])
            
            for fuel in fuel_prices:
                fuel_type = fuel.get("fuel_type", "").upper()
                price = fuel.get("price")
                
                if price is not None:
                    val = normalize_price(price)
                    if val:
                        # Catch E10, E5, and B7 variations
                        if fuel_type in ["E10", "E5", "UNLEADED"]:
                            petrol_prices.append(val)
                        elif "B7" in fuel_type or "DIESEL" in fuel_type:
                            diesel_prices.append(val)
        
        # Calculate final national averages
        if petrol_prices and diesel_prices:
            avg_petrol = sum(petrol_prices) / len(petrol_prices)
            avg_diesel = sum(diesel_prices) / len(diesel_prices)
            return avg_petrol, avg_diesel, "Gov.UK Live (API)"
            
    except Exception as e:
        print(f"Fuel Finder Error: {e}") 
        pass

    return config.UK_PETROL_FALLBACK, config.UK_DIESEL_FALLBACK, "estimated (live fetch failed)"