def init():
    global state
    state = {}

    import threading
    global state_lock
    state_lock = threading.Lock()

    global reset_state
    def reset_state():
        state = {
            "busy": False,
            "current_round": 0,
            "num_nodes_averaged": 0,
            "num_nodes_chosen": 0,
            "current_weights" : None,
            "sigma_omega": None,
            "logging_credentials": {
                "host": "",
                "port": "",
                "username": "",
                "password": "",
            },
            "initial_message": {},
        }

    reset_state()
