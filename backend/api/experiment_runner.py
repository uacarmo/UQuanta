from typing import Any
import importlib


class ExperimentRunner:

    def __init__(self):
        self._experiments = {
            "rabi": self._run_rabi,
            "t1": self._run_t1,
            "t2": self._run_t2,
            "f01_spectroscopy": self._run_f01_spectroscopy,
        }
    

    def run(
        self,
        experiment: str,
        parameters: dict[str, Any],
    ) -> dict[str, Any]:

        if experiment not in self._experiments:
            raise ValueError(
                f"Unknown experiment: {experiment}"
            )

        return self._experiments[experiment](parameters)

    def _run_rabi(
        self,
        parameters: dict[str, Any],
    ) -> dict[str, Any]:

        num_points = parameters.get("num_points", 200)

        module = importlib.import_module(
            "experiments.01_rabi_reference"
        )

        theta, probability = module.rabi_experiment(
            num_points=num_points
        )

        return {
            "experiment": "rabi",
            "result_type": "curve",
            "data": {
                "x": {
                    "name": "theta",
                    "unit": "rad",
                    "values": theta.tolist(),
                },
                "y": {
                    "name": "probability",
                    "unit": "dimensionless",
                    "values": probability.tolist(),
                },
            },
            "metadata": {
                "num_points": len(theta),
            },
        }
    
    def _run_t1(
        self,
        parameters: dict[str, Any],
        ) -> dict[str, Any]:

        num_points = parameters.get("num_points", 31)
        true_t1 = parameters.get("true_t1", 5.0)
        max_time = parameters.get("max_time", 15.0)

        module = importlib.import_module(
            "experiments.10_t1_measurement"
        )

        import numpy as np

        times = np.linspace(
            0.0,
            max_time,
            num_points,
        )

        probabilities = module.theoretical_t1_decay(
            times,
            true_t1,
        )

        estimated_t1, slope, intercept = (
            module.estimate_t1(
                times,
                probabilities,
            )
        )

        relative_error = (
            abs(estimated_t1 - true_t1)
            / true_t1
            * 100.0
        )

        return {
            "experiment": "t1",
            "result_type": "curve",
            "data": {
                "x": {
                    "name": "time",
                    "unit": "simulator_units",
                    "values": times.tolist(),
                },
                "y": {
                    "name": "excited_state_probability",
                    "unit": "dimensionless",
                    "values": probabilities.tolist(),
                },
            },
            "metadata": {
                "num_points": len(times),
                "true_t1": true_t1,
                "estimated_t1": estimated_t1,
                "slope": slope,
                "intercept": intercept,
                "relative_error_percent": relative_error,
                "max_time": max_time,
            },
        }
    
    def _run_t2(
        self,
        parameters: dict[str, Any],
        ) -> dict[str, Any]:

        num_points = parameters.get("num_points", 25)
        true_t2 = parameters.get("true_t2", 3.0)
        max_time = parameters.get("max_time", 12.0)
        shots = parameters.get("shots", 1000)
        seed = parameters.get("seed", 42)

        module = importlib.import_module(
            "quantum.t2_measurement"
        )

        import numpy as np

        times = np.linspace(
            0.0,
            max_time,
            num_points,
        )

        rng = np.random.default_rng(seed)

        measured_coherences = []

        for time in times:
            (
                theory,
                successes,
                failures,
                measured,
            ) = module.simulate_t2_measurement(
                time,
                true_t2,
                shots,
                rng,
            )

            measured_coherences.append(measured)

        measured_coherences = np.asarray(
            measured_coherences,
            dtype=float,
        )

        (
            estimated_t2,
            slope,
            intercept,
        ) = module.estimate_t2(
            times,
            measured_coherences,
        )

        relative_error = (
            abs(estimated_t2 - true_t2)
            / true_t2
            * 100.0
        )

        return {
            "experiment": "t2",
            "result_type": "curve",
            "data": {
                "x": {
                    "name": "time",
                    "unit": "simulator_units",
                    "values": times.tolist(),
                },
                "y": {
                    "name": "coherence",
                    "unit": "dimensionless",
                    "values": measured_coherences.tolist(),
                },
            },
            "metadata": {
                "num_points": len(times),
                "true_t2": true_t2,
                "estimated_t2": estimated_t2,
                "slope": slope,
                "intercept": intercept,
                "relative_error_percent": relative_error,
                "max_time": max_time,
                "shots": shots,
                "seed": seed,
            },
        }

    def _run_f01_spectroscopy(
        self,
        parameters: dict[str, Any],
        ) -> dict[str, Any]:

        import numpy as np

        from quantum.spectroscopy import Spectroscopy

        f01 = parameters.get("f01", 5.0)
        drive_strength = parameters.get(
            "drive_strength",
            2.0 * np.pi * 0.5,
        )
        interaction_time = parameters.get(
            "interaction_time",
            1.0,
        )

        frequency_start = parameters.get(
            "frequency_start",
            4.0,
        )

        frequency_stop = parameters.get(
            "frequency_stop",
            6.0,
        )

        num_points = parameters.get(
            "num_points",
            201,
        )

        omega_01 = 2.0 * np.pi * f01

        spectroscopy = Spectroscopy(
            omega_01=omega_01,
            drive_strength=drive_strength,
            interaction_time=interaction_time,
        )

        frequencies = np.linspace(
            frequency_start,
            frequency_stop,
            num_points,
        )

        drive_frequencies = (
            2.0 * np.pi * frequencies
        )

        probabilities = spectroscopy.sweep(
            drive_frequencies
        )

        (
            resonance_omega,
            maximum_probability,
        ) = spectroscopy.find_resonance(
            drive_frequencies,
            probabilities,
        )

        resonance_frequency = (
            resonance_omega / (2.0 * np.pi)
        )

        relative_error = (
            abs(resonance_frequency - f01)
            / f01
            * 100.0
        )

        return {
            "experiment": "f01_spectroscopy",
            "result_type": "curve",
            "data": {
                "x": {
                    "name": "drive_frequency",
                    "unit": "frequency_units",
                    "values": frequencies.tolist(),
                },
                "y": {
                    "name": "excited_state_probability",
                    "unit": "dimensionless",
                    "values": probabilities.tolist(),
                },
            },
            "metadata": {
                "f01": f01,
                "resonance_frequency": resonance_frequency,
                "maximum_probability": maximum_probability,
                "relative_error_percent": relative_error,
                "drive_strength": drive_strength,
                "interaction_time": interaction_time,
                "frequency_start": frequency_start,
                "frequency_stop": frequency_stop,
                "num_points": len(frequencies),
            },
        }