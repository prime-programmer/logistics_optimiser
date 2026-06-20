# Route Helpers 
def route_dist(chunk, warehouse_idx, D):
    if not chunk:
        return 0.0
    idxs = [warehouse_idx] + list(chunk) + [warehouse_idx]
    total = sum(D[idxs[k], idxs[k+1]] for k in range(len(idxs)-1))
    return float(total)


def two_opt(route, warehouse_idx, D):
    if len(route) < 2:
        return route
    best = route[:]
    improved = True
    while improved:
        improved = False
        for i in range(len(best)-1):
            for j in range(i+2, len(best)):
                new = best[:i] + best[i:j+1][::-1] + best[j+1:]
                if route_dist(new, warehouse_idx, D) < route_dist(best, warehouse_idx, D):
                    best = new
                    improved = True
    return best


def best_vehicle_split(stores, warehouse_idx, D, van_rate, lorry_rate):
    n = len(stores)
    if n == 0:
        return 0.0, []
    INF = float('inf')
    dp_cost   = [INF] * (n+1)
    dp_routes = [None] * (n+1)
    dp_cost[0]   = 0.0
    dp_routes[0] = []
    for i in range(1, n+1):
        for j in range(max(0, i-LORRY_MAX), i):
            chunk = stores[j:i]
            miles = route_dist(chunk, warehouse_idx, D)
            rate, vtype = (van_rate, 'Van') if len(chunk) <= VAN_MAX else (lorry_rate, 'Lorry')
            total = dp_cost[j] + miles * rate
            if total < dp_cost[i]:
                opt_chunk = two_opt(list(chunk), warehouse_idx, D)
                opt_miles = route_dist(opt_chunk, warehouse_idx, D)
                opt_cost  = opt_miles * rate
                dp_cost[i]   = dp_cost[j] + opt_cost
                dp_routes[i] = dp_routes[j] + [(opt_chunk, vtype, opt_miles, opt_cost)]
    return dp_cost[n], dp_routes[n]


def evaluate(assignment, perm, D, w1_idx, w2_idx, van_rate, lorry_rate):
    w1 = [perm[i] for i in range(len(perm)) if assignment[i] == 0]
    w2 = [perm[i] for i in range(len(perm)) if assignment[i] == 1]
    c1, _ = best_vehicle_split(w1, w1_idx, D, van_rate, lorry_rate)
    c2, _ = best_vehicle_split(w2, w2_idx, D, van_rate, lorry_rate)
    return c1 + c2


def solution_details(assignment, perm, D, w1_idx, w2_idx, van_rate, lorry_rate):
    w1 = [perm[i] for i in range(len(perm)) if assignment[i] == 0]
    w2 = [perm[i] for i in range(len(perm)) if assignment[i] == 1]
    c1, r1 = best_vehicle_split(w1, w1_idx, D, van_rate, lorry_rate)
    c2, r2 = best_vehicle_split(w2, w2_idx, D, van_rate, lorry_rate)
    return {"total": c1+c2, "w1": w1, "w2": w2, "r1": r1, "r2": r2, "c1": c1, "c2": c2}


# Algorithms 
def rand_sol(n_stores):
    a = [random.randint(0,1) for _ in range(n_stores)]
    p = list(range(n_stores))
    random.shuffle(p)
    return a, p


def neighbour(a, p):
    na, np_ = a[:], p[:]
    move = random.choice(['flip','swap_perm','swap_assign'])
    n = len(a)
    if move == 'flip':
        i = random.randrange(n); na[i] ^= 1
    elif move == 'swap_perm':
        i,j = random.sample(range(n),2); np_[i],np_[j]=np_[j],np_[i]
    else:
        w1s=[i for i in range(n) if na[i]==0]
        w2s=[i for i in range(n) if na[i]==1]
        if w1s and w2s:
            i=random.choice(w1s); j=random.choice(w2s)
            na[i],na[j]=1,0
    return na, np_
