# config.py

VAN_MAX = 5
LORRY_MAX = 18

COLOURS = {
    "warehouse": "#FF0000",
    "store":     "#3388FF",
    "route_w1":  ["#E74C3C","#C0392B","#E67E22","#D35400","#F39C12"],
    "route_w2":  ["#2ECC71","#27AE60","#1ABC9C","#16A085","#8E44AD"],
}

UK_PETROL_FALLBACK = 1.42
UK_DIESEL_FALLBACK = 1.44
MPG_VAN = 38.0
MPG_LORRY = 24.0
LITRES_PER_GALLON = 4.54609

DEFAULT_WAREHOUSES = {
    "W1": (51.50, -0.12),
    "W2": (52.48,  1.75),
}

DEFAULT_STORES = {
    1:  (52.63,  1.30),
    2:  (51.75,  0.47),
    3:  (53.00, -0.12),
    4:  (52.20,  0.12),
    5:  (51.55,  0.70),
    6:  (52.40,  1.60),
    7:  (51.90,  1.00),
    8:  (52.90,  1.50),
    9:  (53.10,  0.90),
    10: (51.80, -0.40),
}