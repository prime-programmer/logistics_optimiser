from algorithms.base_optimizer import evaluate, rand_sol

def random_search_algo(D, w1_idx, w2_idx, van_rate, lorry_rate, n_stores, steps=2000):
    a,p = rand_sol(n_stores)
    best_cost = evaluate(a,p,D,w1_idx,w2_idx,van_rate,lorry_rate)
    best_sol  = (a,p)
    history   = [best_cost]
    for _ in range(steps):
        na,np_= rand_sol(n_stores)
        c = evaluate(na,np_,D,w1_idx,w2_idx,van_rate,lorry_rate)
        if c < best_cost:
            best_cost,best_sol = c,(na,np_)
        history.append(best_cost)
    return best_cost, best_sol, history

