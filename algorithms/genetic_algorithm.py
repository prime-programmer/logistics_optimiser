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
            # Crossover
            cut = random.randrange(n_stores)
            ca  = pa[0][:cut] + pb[0][cut:]
            cp  = pa[1][:cut] + pb[1][cut:]
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