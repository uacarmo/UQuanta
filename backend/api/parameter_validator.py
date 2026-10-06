from typing import Any


def validate_parameters(
    experiment: str,
    parameters: dict[str, Any],
) -> None:

    if experiment == "rabi":
        _require_positive_int(parameters, "num_points")

    elif experiment == "t1":
        _require_positive_int(parameters, "num_points")
        _require_positive_float(parameters, "true_t1")
        _require_nonnegative_float(parameters, "max_time")

    elif experiment == "t2":
        _require_positive_int(parameters, "num_points")
        _require_positive_float(parameters, "true_t2")
        _require_nonnegative_float(parameters, "max_time")
        _require_positive_int(parameters, "shots")

    elif experiment == "f01_spectroscopy":
        _require_positive_float(parameters, "f01")
        _require_positive_float(parameters, "drive_strength")
        _require_positive_float(parameters, "interaction_time")
        _require_positive_int(parameters, "num_points")

        frequency_start = parameters.get(
            "frequency_start",
            4.0,
        )

        frequency_stop = parameters.get(
            "frequency_stop",
            6.0,
        )

        if frequency_start >= frequency_stop:
            raise ValueError(
                "frequency_start must be less than frequency_stop"
            )


def _require_positive_int(
    parameters: dict[str, Any],
    name: str,
) -> None:

    if name not in parameters:
        return

    value = parameters[name]

    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(
            f"{name} must be an integer"
        )

    if value <= 0:
        raise ValueError(
            f"{name} must be positive"
        )


def _require_positive_float(
    parameters: dict[str, Any],
    name: str,
) -> None:

    if name not in parameters:
        return

    value = parameters[name]

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(
            f"{name} must be a number"
        )

    if value <= 0:
        raise ValueError(
            f"{name} must be positive"
        )


def _require_nonnegative_float(
    parameters: dict[str, Any],
    name: str,
) -> None:

    if name not in parameters:
        return

    value = parameters[name]

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(
            f"{name} must be a number"
        )

    if value < 0:
        raise ValueError(
            f"{name} must be non-negative"
        )