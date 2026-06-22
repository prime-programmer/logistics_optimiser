import config
from algorithms.base_optimizer import route_dist

def ortools_solve(D, w1_idx, w2_idx, van_rate, lorry_rate, n_stores, time_limit=10):
    """Use OR-Tools VRP for benchmark comparison."""
    try:
        from ortools.constraint_solver import pywrapcp, routing_enums_pb2
    except ImportError:
        return None, None, "OR-Tools not available"

    all_nodes = list(range(n_stores)) + [w1_idx, w2_idx]
    n_nodes   = len(all_nodes)
    idx_map   = {v:i for i, v in enumerate(all_nodes)}

    def dist_cb(i, j):
        a, b = all_nodes[i], all_nodes[j]
        return int(D[a, b] * 1000)

  
    # Build manager: 4 vehicles total (assign 2 to W1, and 2 to W2)
    depot_indices = [
        idx_map[w1_idx], idx_map[w1_idx], 
        idx_map[w2_idx], idx_map[w2_idx]
    ]
    manager = pywrapcp.RoutingIndexManager(n_nodes, 4, depot_indices, depot_indices)
    routing = pywrapcp.RoutingModel(manager)

    cb_idx = routing.RegisterTransitCallback(
        lambda i, j: dist_cb(manager.IndexToNode(i), manager.IndexToNode(j))
    )
    routing.SetArcCostEvaluatorOfAllVehicles(cb_idx)

    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    params.time_limit.seconds = time_limit

    solution = routing.SolveWithParameters(params)
    if not solution:
        return None, None, "OR-Tools found no solution"

    total_cost = 0.0
    routes = []
    
    for v in range(4):
        idx   = routing.Start(v)
        route = []
        while not routing.IsEnd(idx):
            node = manager.IndexToNode(idx)
            if node not in depot_indices:
                route.append(all_nodes[node])
            idx = solution.Value(routing.NextVar(idx))
            
        if route:
            depot = w1_idx if v < 2 else w2_idx
            rate  = van_rate if len(route) <= config.VAN_MAX else lorry_rate
            miles = route_dist(route, depot, D)
            cost  = miles * rate
            total_cost += cost
            routes.append((route, 'Van' if len(route) <= config.VAN_MAX else 'Lorry', miles, cost, depot))

    return total_cost, routes, None