import numpy as np
from metrics.calculate_error import calculate_error

# Dictionary for parameter limits
parameter_bounds = {
    "r": (0.001, 1.0),
    "K": (500, 3000),
    "a": (0.001, 2.0),
    "b": (0.001, 1.0),
    "c": (0.001, 1.0),
    "V_max": (500, 3000),
}

def monte_carlo(model, solver, times, volumes, iterations=1000):

    best_parameters = model.parameters.copy()
    best_mse = calculate_error(
        model, solver, times, volumes, best_parameters
    )

    for _ in range(iterations):

        new_parameters = {}

        for key in best_parameters:
            lower, upper = parameter_bounds[key]
            new_parameters[key] = np.random.uniform(lower, upper)

        new_mse = calculate_error(
            model, solver, times, volumes, new_parameters
        )

        if new_mse < best_mse:
            best_parameters = new_parameters
            best_mse = new_mse

    return best_parameters, best_mse
