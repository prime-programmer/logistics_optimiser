import pytest
import numpy as np
from algorithms.base_optimizer import route_dist, rand_sol, two_opt

@pytest.fixture
def dummy_distance_matrix():
    # 3x3 simple matrix
    return np.array([
        [0.0, 10.0, 20.0],
        [10.0, 0.0, 5.0],
        [20.0, 5.0, 0.0]
    ])

def test_route_dist(dummy_distance_matrix):
    # Route: Warehouse (0) -> Store (1) -> Store (2) -> Warehouse (0)
    # Distances: D[0,1] + D[1,2] + D[2,0] = 10 + 5 + 20 = 35
    chunk = [1, 2]
    warehouse_idx = 0
    distance = route_dist(chunk, warehouse_idx, dummy_distance_matrix)
    assert distance == 35.0

def test_rand_sol():
    n_stores = 5
    a, p = rand_sol(n_stores)
    assert len(a) == n_stores
    assert len(p) == n_stores
    # Ensure assignments are binary
    assert all(x in [0, 1] for x in a)
    # Ensure all stores are represented in the permutation
    assert set(p) == set(range(n_stores))

def test_two_opt(dummy_distance_matrix):
    # A deliberately bad route: W(0) -> S(2) -> S(1) -> W(0) = 20 + 5 + 10 = 35
    # Optimized should be W(0) -> S(1) -> S(2) -> W(0) = 10 + 5 + 20 = 35 (Same in this triangle, but tests execution)
    route = [2, 1]
    optimized = two_opt(route, warehouse_idx=0, D=dummy_distance_matrix)
    assert len(optimized) == len(route)
    assert set(optimized) == set(route)