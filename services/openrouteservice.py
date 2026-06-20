#ORS Distance Matrix
@st.cache_data(ttl=86400, show_spinner=False)
def get_ors_distance_matrix(coords_tuple, api_key):
    """
    Call OpenRouteService Matrix API.
    coords_tuple: ((lat,lon), ...) – hashable for caching
    Returns numpy array of distances in MILES.
    """
    if not api_key:
        return None, "No ORS API key provided"

    coords_ors = [[lon, lat] for lat, lon in coords_tuple]
    payload = {
        "locations": coords_ors,
        "metrics": ["distance"],
        "units": "m",
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
