import streamlit as st
from services.openrouteservice import get_ors_distance_matrix
from services.distance_matrix import euclidean_distance_matrix
from algorithms.base_optimizer import solution_details
from algorithms.random_search import random_search_algo
from algorithms.hill_climbing import hill_climbing_algo
from algorithms.genetic_algorithm import ga_algo
from algorithms.ortools_solver import ortools_solve
from services.openrouteservice import get_ors_route_geometry

def render_optimise_section():
    st.markdown("---")
    if st.button("🚀 **OPTIMISE ROUTES**", type="primary", use_container_width=True):
        if len(st.session_state.stores) < 2:
            st.error("Please add at least 2 stores.")
            return
        if len(st.session_state.warehouses) < 2:
            st.error("Two warehouses (W1, W2) are required.")
            return

        warehouses = st.session_state.warehouses
        stores = st.session_state.stores
        store_ids = sorted(stores.keys())
        n_stores = len(store_ids)
        w1_idx, w2_idx = n_stores, n_stores + 1

        all_locs = [stores[sid] for sid in store_ids] + [warehouses["W1"], warehouses["W2"]]

        with st.spinner("Fetching road distances…"):
            if st.session_state.ors_key:
                D, err = get_ors_distance_matrix(tuple(all_locs), st.session_state.ors_key)
                if err:
                    st.warning(f"ORS: {err} — using straight-line fallback.")
                    D = euclidean_distance_matrix(all_locs)
                    dist_mode = "straight-line (fallback)"
                else:
                    dist_mode = "real road (ORS)"
            else:
                D = euclidean_distance_matrix(all_locs)
                dist_mode = "straight-line (no API key)"

        kwargs = dict(
            D=D, w1_idx=w1_idx, w2_idx=w2_idx,
            van_rate=st.session_state.van_rate_live, 
            lorry_rate=st.session_state.lorry_rate_live,
            n_stores=n_stores,
        )

        progress = st.progress(0, text="Running Random Search…")
        rs_cost, rs_sol, rs_hist = random_search_algo(**kwargs, steps=st.session_state.rs_steps)
        
        progress.progress(33, text="Running Hill Climbing…")
        hc_cost, hc_sol, hc_hist = hill_climbing_algo(**kwargs, steps=st.session_state.hc_steps)
        
        progress.progress(66, text="Running Genetic Algorithm…")
        ga_cost, ga_sol, ga_hist = ga_algo(**kwargs, pop=st.session_state.ga_pop, gens=st.session_state.ga_gens)
        progress.progress(90, text="Done ✓")

        ort_cost, ort_routes, ort_err = None, None, None
        if st.session_state.run_ortools:
            progress.progress(92, text="Running OR-Tools benchmark…")
            ort_cost, ort_routes, ort_err = ortools_solve(**kwargs)

        progress.progress(100, text="Complete!")

        # Pick best
        bests = [(rs_cost, "Random Search", rs_sol, rs_hist),
                 (hc_cost, "Hill Climbing",  hc_sol, hc_hist),
                 (ga_cost, "Genetic Algorithm", ga_sol, ga_hist)]
        best_cost, best_name, best_sol, _ = min(bests, key=lambda x: x[0])

        det = solution_details(best_sol[0], best_sol[1], D, w1_idx, w2_idx,
                               st.session_state.van_rate_live, st.session_state.lorry_rate_live)

     

        def remap_routes(routes, w_label):
            out = []
            for (chunk, vtype, miles, cost) in routes:
                real_chunk = [store_ids[c] for c in chunk]
                # Build coordinate list: Warehouse -> Stores -> Warehouse
                route_coords = [warehouses[w_label]] + [stores[s] for s in real_chunk] + [warehouses[w_label]]
                
                geometry = None
                if st.session_state.ors_key:
                    # Fetch the curvy road data
                    geometry = get_ors_route_geometry(tuple(route_coords), st.session_state.ors_key)
                    
                # We now return 6 variables instead of 5
                out.append((real_chunk, vtype, miles, cost, w_label, geometry))
            return out

        routes_w1 = remap_routes(det["r1"], "W1")
        routes_w2 = remap_routes(det["r2"], "W2")

        # Fixed: Use explicit strings "W1" and "W2" to avoid overwriting Store ID 10
        loc_by_widx = {"W1": warehouses["W1"], "W2": warehouses["W2"]}
        loc_by_sid  = {store_ids[i]: all_locs[i] for i in range(n_stores)}

        st.session_state.results = {
            "dist_mode": dist_mode,
            "fuel_type": st.session_state.fuel_type,
            "active_price": st.session_state.active_price,
            "van_rate": st.session_state.van_rate_live,
            "lorry_rate": st.session_state.lorry_rate_live,
            "rs_cost": rs_cost, "rs_hist": rs_hist,
            "hc_cost": hc_cost, "hc_hist": hc_hist,
            "ga_cost": ga_cost, "ga_hist": ga_hist,
            "best_cost": best_cost, "best_name": best_name,
            "routes_w1": routes_w1, "routes_w2": routes_w2,
            "det": det, "store_ids": store_ids,
            "all_loc_map": {**loc_by_sid, **loc_by_widx},
            "ort_cost": ort_cost, "ort_routes": ort_routes, "ort_err": ort_err,
            "tw_windows": st.session_state.get("tw_windows", {})
        }
        st.success("Optimisation complete! See **Results** tab.")

       