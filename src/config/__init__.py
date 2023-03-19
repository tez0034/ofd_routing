class Config:

    # Graph parameters
    customer_valid_attribute_names = ['location', 'delivery']
    store_valid_attribute_names = ['location', 'wait_time']
    
    # Simulation parameters
    travel_time_method = 'location'
    travel_time_std_dev = 0.2
    min_travel_time = 5 # (min)
    vehicle_speed = 400 #(m/min) - cyclist
    store_wait_time = 5 # (min)


    # For random map initiatization
    store_to_customer_ratio = 0.1
    random_init_n_nodes = 500
    map_size = [10000, 10000] # (m)
    max_edge_travel_time = 10 #(min)

    # Cost function parameters
    late_penalty_constant = 1e3
    late_penalty_weight = 5

    def __init__(self, **kwargs):
        pass