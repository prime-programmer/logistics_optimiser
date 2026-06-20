def fuel_cost_per_mile(fuel_type: str, petrol_price: float, diesel_price: float) -> float:
    """Return £/mile for van or lorry based on fuel type."""
    price = petrol_price if fuel_type == "Petrol" else diesel_price
    if fuel_type == "Petrol":
        mpg = MPG_VAN
    else:
        mpg = MPG_VAN  # vans can be either; lorries are diesel
    litres_per_mile = LITRES_PER_GALLON / mpg
    return price * litres_per_mile

