def euclidean_distance_matrix(locations):
    """Fallback Euclidean distances (treated as km, then converted to rough miles)."""
    n = len(locations)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            lat1, lon1 = locations[i]
            lat2, lon2 = locations[j]
            # approximate km
            dlat = (lat2 - lat1) * 111.0
            dlon = (lon2 - lon1) * 111.0 * math.cos(math.radians((lat1+lat2)/2))
            km   = math.sqrt(dlat**2 + dlon**2)
            D[i][j] = km * 0.621371
    return D


