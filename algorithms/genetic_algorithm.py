import random
from algorithms.base_optimizer import evaluate, rand_sol, neighbour

def ga_algo(D, w1_idx, w2_idx, van_rate, lorry_rate, n_stores, pop=80, gens=150, mr=0.35):
    def score(sol): 
        return evaluate(sol[0], sol[1], D, w1_idx, w2_idx, van_rate, lorry_rate)
        
    population = [rand_sol(n_stores) for _ in range(pop)]
    best_sol   = min(population, key=score)
    best_cost  = score(best_sol)
    history    = [best_cost]
    
    for _ in range(gens):
        scored = sorted(population, key=score)
        elite  = scored[:pop//2]
        children = []
        
        while len(children) < pop - len(elite):
            pa, pb = random.sample(elite, 2)
            
            # 1. Crossover for assignments (Binary array - standard slice is fine)
            cut = random.randrange(n_stores)
            ca  = pa[0][:cut] + pb[0][cut:]
            
            # 2. Crossover for permutations (Order Crossover to prevent missing stores)
            start, end = sorted(random.sample(range(n_stores), 2))
            cp = [-1] * n_stores
            cp[start:end] = pa[1][start:end]
            
            pb_filtered = [x for x in pb[1] if x not in cp]
            idx = 0
            for i in range(n_stores):
                if cp[i] == -1:
                    cp[i] = pb_filtered[idx]
                    idx += 1
            
            # Mutation
            if random.random() < mr:
                ca, cp = neighbour(ca, cp)
            children.append((ca, cp))
            
        population = elite + children
        gen_best = min(population, key=score)
        
        if score(gen_best) < best_cost:
            best_cost = score(gen_best)
            best_sol  = gen_best
            
        history.append(best_cost)
        
    return best_cost, best_sol, history