import pytest
from services.cost_engine import cost_per_mile
from services.emissions import calculate_emissions
import config

def test_cost_per_mile_diesel():
    # 1.44 per litre, 38 MPG
    rate = cost_per_mile("Diesel", 1.42, 1.44, mpg=38)
    # 4.54609 litres per gallon / 38 = 0.1196 litres per mile
    # 0.1196 * 1.44 = £0.1722 per mile
    assert round(rate, 4) == 0.1722

def test_cost_per_mile_petrol():
    rate = cost_per_mile("Petrol", 1.42, 1.44, mpg=38)
    assert round(rate, 4) == 0.1698

def test_calculate_emissions():
    # 100 miles at 24 MPG (Lorry)
    emissions = calculate_emissions(distance_miles=100.0, mpg=24.0, fuel_type="Diesel")
    # 100 / 24 = 4.166 gallons * 4.54609 = 18.94 litres
    # 18.94 * 2.512 = 47.58 kg CO2
    assert 47.0 < emissions < 48.0

def test_zero_distance_emissions():
    assert calculate_emissions(0, 38.0, "Diesel") == 0.0