# visualisation/maps.py
import folium
import config

def build_map(locations, warehouses, stores, routes_w1, routes_w2):
    all_lats = [l[0] for l in locations.values()]
    all_lons = [l[1] for l in locations.values()]
    centre   = [sum(all_lats)/len(all_lats), sum(all_lons)/len(all_lons)]
    m = folium.Map(location=centre, zoom_start=8, tiles="CartoDB positron")

    # Warehouses
    for wname, (lat, lon) in warehouses.items():
        folium.Marker(
            [lat, lon],
            popup=f"<b>{wname}</b>",
            icon=folium.Icon(color="red", icon="home", prefix="fa"),
        ).add_to(m)

    # Stores
    for sname, (lat, lon) in stores.items():
        folium.CircleMarker(
            [lat, lon], radius=6, color=config.COLOURS["store"], fill=True, fill_opacity=0.9,
            popup=f"Store {sname}",
        ).add_to(m)

    # Routes (Handles both straight lines and real ORS roads)
    for routes in [routes_w1, routes_w2]:
        for i, (chunk, vtype, miles, cost, w_label, geometry) in enumerate(routes):
            color_key = "route_w1" if w_label == "W1" else "route_w2"
            col = config.COLOURS[color_key][i % len(config.COLOURS[color_key])]
            tooltip_txt = f"{w_label} V{i+1} ({vtype}) {miles:.1f}mi £{cost:.0f}"
            
            if geometry:
                # Draw real road curves
                folium.PolyLine(geometry, color=col, weight=4, opacity=0.85, tooltip=tooltip_txt).add_to(m)
            else:
                # Fallback to straight lines
                wloc = locations[w_label]
                pts  = [wloc] + [locations[s] for s in chunk] + [wloc]
                folium.PolyLine(pts, color=col, weight=3, opacity=0.85, tooltip=tooltip_txt).add_to(m)
                        
    return m