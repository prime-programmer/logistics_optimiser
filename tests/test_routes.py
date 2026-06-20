import pytest
import numpy as np
from services.distance_matrix import euclidean_distance_matrix

def test_euclidean_distance_matrix():
    # Two points, roughly 1 degree of latitude apart (approx 69 miles)
    locations = [
        (51.0, 0.0),
        (52.0, 0.0)
    ]
    D = euclidean_distance_matrix(locations)
    
    assert D.shape == (2, 2)
    assert D[0][0] == 0.0
    assert D[1][1] == 0.0
    
    # Distance should be symmetric
    assert D[0][1] == D[1][0]
    
    # 1 degree lat is ~111km -> ~69 miles
    assert 68.0 < D[0][1] < 70.0