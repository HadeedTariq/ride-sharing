def estimate_fare(distance_km, surge_multiplier=1.0):
    BASE_FARE = 50  # Fixed starting fare
    PER_KM_RATE = 20  # Rate per kilometer

    total_fare = BASE_FARE + (distance_km * PER_KM_RATE)
    total_fare *= surge_multiplier  # Apply surge pricing

    return round(total_fare, 2)
