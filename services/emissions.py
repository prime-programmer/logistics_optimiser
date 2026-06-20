# services/emissions.py

# Approximate UK Gov GHG Conversion Factors (kg CO2e per litre of fuel)
CO2E_PER_LITRE_DIESEL = 2.512
CO2E_PER_LITRE_PETROL = 2.193
LITRES_PER_GALLON = 4.54609

def calculate_emissions(distance_miles: float, mpg: float, fuel_type: str) -> float:
    """
    Calculate total CO2e emissions in kilograms for a given trip.
    """
    if distance_miles <= 0:
        return 0.0
        
    gallons_used = distance_miles / mpg
    litres_used = gallons_used * LITRES_PER_GALLON
    
    factor = CO2E_PER_LITRE_DIESEL if fuel_type == "Diesel" else CO2E_PER_LITRE_PETROL
    
    return litres_used * factor