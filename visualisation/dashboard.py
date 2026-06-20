import streamlit as st
import pandas as pd
import config
from services.emissions import calculate_emissions

def render_results_metrics(res, van_mpg, lorry_mpg):
    """Renders the top-line metrics and environmental impact."""
    st.subheader(f"🏆 Best solution: {res['best_name']} — £{res['best_cost']:.2f}")
    st.caption(f"Distance mode: **{res['dist_mode']}** | "
               f"Fuel: **{res['fuel_type']}** @ £{res['active_price']:.3f}/L | "
               f"Van: £{res['van_rate']:.4f}/mi | Lorry: £{res['lorry_rate']:.4f}/mi")

    c1, c2, c3 = st.columns(3)
    c1.metric("Random Search", f"£{res['rs_cost']:.2f}")
    c2.metric("Hill Climbing",  f"£{res['hc_cost']:.2f}")
    c3.metric("Genetic Algorithm", f"£{res['ga_cost']:.2f}")

    st.markdown("---")
    st.subheader("🌍 Environmental Impact")

    total_emissions = 0.0
    for chunk, vtype, miles, cost, widx in res["routes_w1"] + res["routes_w2"]:
        mpg = van_mpg if vtype == "Van" else lorry_mpg
        emissions = calculate_emissions(miles, mpg, res["fuel_type"])
        total_emissions += emissions

    e1, e2 = st.columns(2)
    e1.metric("Total CO₂e Emissions", f"{total_emissions:.1f} kg")
    trees_needed = total_emissions / (21.0 / 365)
    e2.metric("Equivalent Trees Needed (Daily)", f"{trees_needed:.1f} trees")

def render_route_breakdown(res, van_mpg, lorry_mpg):
    """Renders the dropdown expanders for each route."""
    st.markdown("### Route Breakdown")
    det = res["det"]
    for wlabel, routes, subtotal in [("W1", res["routes_w1"], det["c1"]),
                                      ("W2", res["routes_w2"], det["c2"])]:
        with st.expander(f"**{wlabel}** — {len(routes)} vehicle(s) — Subtotal: £{subtotal:.2f}"):
            for i, (chunk, vtype, miles, cost, _) in enumerate(routes, 1):
                rate = res["van_rate"] if vtype == "Van" else res["lorry_rate"]
                mpg = van_mpg if vtype == "Van" else lorry_mpg
                route_emissions = calculate_emissions(miles, mpg, res["fuel_type"])
                
                st.markdown(
                    f"**Vehicle {i}** ({vtype}, {len(chunk)} stores)  \n"
                    f"`{wlabel} → {' → '.join(str(s) for s in chunk)} → {wlabel}`  \n"
                    f"📏 {miles:.1f} miles | 💷 £{cost:.2f} | ☁️ **{route_emissions:.1f} kg CO₂e**"
                )
                if res["tw_windows"]:
                    for s in chunk:
                        if s in res["tw_windows"]:
                            tw = res["tw_windows"][s]
                            st.caption(f"  Store {s}: delivery window {tw[0]:02d}:00–{tw[1]:02d}:00")

def render_comparison_tables(res, van_mpg, lorry_mpg):
    """Renders the dataframes and charts for the Comparison tab."""
    st.subheader("Algorithm Comparison")
    rows = [
        {"Algorithm": "Random Search",     "Total Cost (£)": round(res["rs_cost"], 2), "Gap to best (%)": round((res["rs_cost"] - res["best_cost"])/res["best_cost"]*100, 2)},
        {"Algorithm": "Hill Climbing",     "Total Cost (£)": round(res["hc_cost"], 2), "Gap to best (%)": round((res["hc_cost"] - res["best_cost"])/res["best_cost"]*100, 2)},
        {"Algorithm": "Genetic Algorithm", "Total Cost (£)": round(res["ga_cost"], 2), "Gap to best (%)": round((res["ga_cost"] - res["best_cost"])/res["best_cost"]*100, 2)}
    ]

    if res.get("ort_cost"):
        rows.append({"Algorithm": "OR-Tools (benchmark)", "Total Cost (£)": round(res["ort_cost"], 2), "Gap to best (%)": round((res["ort_cost"] - res["best_cost"])/res["best_cost"]*100, 2)})

    st.dataframe(pd.DataFrame(rows).set_index("Algorithm"), use_container_width=True)

    st.markdown("---")
    st.subheader("Fuel Cost Sensitivity")
    price_range = [p/100 for p in range(100, 200, 5)]
    sens_rows = []
    for p in price_range:
        def cr(mpg): return (config.LITRES_PER_GALLON/mpg) * p
        row = {"Fuel price (£/L)": p}
        for name, cost in [("RS", res["rs_cost"]), ("HC", res["hc_cost"]), ("GA", res["ga_cost"])]:
            row[name] = round(cost * (cr(van_mpg)/res["van_rate"]), 2)
        sens_rows.append(row)
        
    st.line_chart(pd.DataFrame(sens_rows).set_index("Fuel price (£/L)"))