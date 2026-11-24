import numpy as np
from optimization.hooke_jeeves import calculate_error


def monte_carlo(model, solver, times, volumes, iterations=1000):

    best_parameters = model.parameters.copy()
    best_mse = calculate_error(
        model, solver, times, volumes, best_parameters
    )

    for _ in range(iterations):

        new_parameters = {
            key: np.random.uniform(0.01, 2.0)
            for key in best_parameters
        }

        new_mse = calculate_error(
            model, solver, times, volumes, new_parameters
        )

        if new_mse < best_mse:
            best_parameters = new_parameters
            best_mse = new_mse

    return best_parameters, best_mse
