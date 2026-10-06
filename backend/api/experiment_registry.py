EXPERIMENTS = {
    "rabi": {
        "name": "Rabi Oscillation",
        "category": "calibration",
        "status": "validated",
        "parameters": {
            "num_points": {
                "type": "integer",
                "default": 200,
                "unit": "points",
                 "minimum": 1,
            },
        },
    },

    "t1": {
        "name": "T1 Relaxation",
        "category": "calibration",
        "status": "validated",
        "parameters": {
            "num_points": {
                "type": "integer",
                "default": 31,
                "unit": "points",
                "minimum": 1,
            },
            "true_t1": {
                "type": "float",
                "default": 5.0,
                "unit": "simulator_units",
                "minimum": 0.0,
            },
            "max_time": {
                "type": "float",
                "default": 15.0,
                "unit": "simulator_units",
                "minimum": 0.0,
            },
        },
    },

    "t2": {
        "name": "T2 Coherence",
        "category": "calibration",
        "status": "validated",
        "parameters": {
            "num_points": {
                "type": "integer",
                "default": 25,
                "unit": "points",
                "minimum": 1,
            },
            "true_t2": {
                "type": "float",
                "default": 3.0,
                "unit": "simulator_units",
                "minimum": 0.0,
            },
            "max_time": {
                "type": "float",
                "default": 12.0,
                "unit": "simulator_units",
                "minimum": 0.0,
            },
            "shots": {
                "type": "integer",
                "default": 1000,
                "unit": "shots",
                "minimum": 1,
            },
            "seed": {
                "type": "integer",
                "default": 42,
                "unit": "seed",
            },
        },
    },

    "f01_spectroscopy": {
        "name": "F01 Spectroscopy",
        "category": "spectroscopy",
        "status": "validated",
        "parameters": {
            "f01": {
                "type": "float",
                "default": 5.0,
                "unit": "frequency_units",
                "minimum": 0.0,
            },
            "drive_strength": {
                "type": "float",
                "default": 3.141592653589793,
                "unit": "angular_frequency_units",
                "minimum": 0.0,
            },
            "interaction_time": {
                "type": "float",
                "default": 1.0,
                "unit": "simulator_units",
                "minimum": 0.0,
            },
            "frequency_start": {
                "type": "float",
                "default": 4.0,
                "unit": "frequency_units",
            },
            "frequency_stop": {
                "type": "float",
                "default": 6.0,
                "unit": "frequency_units",
            },
            "num_points": {
                "type": "integer",
                "default": 201,
                "unit": "points",
                "minimum": 1,
            },
        },
    },
}


def list_experiments():
    return [
        {
            "id": experiment_id,
            **metadata,
        }
        for experiment_id, metadata in EXPERIMENTS.items()
    ]


def is_known_experiment(experiment_id: str) -> bool:
    return experiment_id in EXPERIMENTS