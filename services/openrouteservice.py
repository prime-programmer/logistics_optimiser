import streamlit as st
import requests
import numpy as np

@st.cache_data(ttl=86400, show_spinner=False)
def get_ors_distance_matrix(coords_tuple, api_key):
    """
    Call OpenRouteService Matrix API.
    Returns numpy array of distances in MILES.
    """
    if not api_key:
        return None, "No ORS API key provided"

    coords_ors = [[lon, lat] for lat, lon in coords_tuple]
    
    payload = {
        "locations": coords_ors,
        "metrics": ["distance"],
        "units": "m",
        "radiuses": [-1] * len(coords_ors)  # Tells ORS to find the nearest road no matter how far
    }
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }
    try:
        r = requests.post(
            "https://api.openrouteservice.org/v2/matrix/driving-car",
            json=payload,
            headers=headers,
            timeout=30,
        )
        if r.status_code != 200:
            return None, f"ORS API error {r.status_code}: {r.text[:200]}"
        data = r.json()
        metres = np.array(data["distances"], dtype=float)
        miles  = metres / 1609.344
        return miles, None
    except Exception as e:
        return None, str(e)


@st.cache_data(ttl=86400, show_spinner=False)
def get_ors_route_geometry(coords_tuple, api_key):
    """Fetches the actual turn-by-turn road geometry for drawing lines."""
    if not api_key:
        return None
        
    coords_ors = [[lon, lat] for lat, lon in coords_tuple]
    
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }
    # Directions API accepts radiuses in the payload
    payload = {
        "coordinates": coords_ors,
        "radiuses": [-1] * len(coords_ors)  # Remove the 350-meter restriction
    }
    
    try:
        r = requests.post(
            "https://api.openrouteservice.org/v2/directions/driving-car/geojson",
            json=payload,
            headers=headers,
            timeout=10,
        )
        if r.status_code == 200:
            data = r.json()
            geometry = data["features"][0]["geometry"]["coordinates"]
            return [[lat, lon] for lon, lat in geometry]
        return None
    except Exception:
        return None