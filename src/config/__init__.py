class Config:
    
    # Simulation parameters
    travel_time_method = 'location'
    travel_time_std_dev = 0.2
    min_travel_time = 5 # (min)
    vehicle_speed = 1200 #(m/min)


    # For random map initiatization
    random_init_n_nodes = 500

    def __init__(self, **kwargs):
        pass