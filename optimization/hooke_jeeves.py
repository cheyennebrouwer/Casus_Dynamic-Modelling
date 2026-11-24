import numpy as np
from models.base_model import TumorGrowthModel


def mse(measured, predicted):
    """
    Calculates the mean squared error (MSE) between measured and predicted values.

    Parameters
    ----------
    measured : numpy.ndarray, measured tumor volume
    predicted : numpy.ndarray, predicted tumor volume

    Returns
    -------
    float, mean squared error between measured and predicted volumes
    """
    differences = measured - predicted
    return np.square(differences).mean()


def calculate_error(model, solver, times, volumes, parameters):
    """
    Simulates tumor growth using the given model and solver, then calculates the MSE.

    parameters
    ----------
    model : TumorGrowthModel, class used for the simulation
    solver : callable, ODE solver to simulate tumor growth
    times : numpy.ndarray, time points of the measurements
    volumes : numpy.ndarray, measured tumor volumes
    parameters : dict, model parameters used for the simulation

    Returns
    -------
    float, mean squared error between measured and predicted tumor volumes
    """
    model_copy = TumorGrowthModel(
        model.name,
        model.function,
        parameters
    )

    t_span = (times[0], times[-1])
    V0 = volumes[0]
    dt = 0.1

    calculated_times, calculated_volumes = solver(
        model_copy, t_span, V0, dt
    )

    predicted = np.interp(
        times, calculated_times, calculated_volumes
    )

    return mse(volumes, predicted)


def hooke_jeeves(model, solver, times, volumes, step_size=0.1, tolerance=1e-6):
    """
    Optimizes the tumor growth model parameters using the Hooke-Jeeves method by minimizing the mean squared error.

    Parameters
    ----------
    model : TumorGrowthModel, the model to optimize
    solver : callable, ODE solver used to simulate tumor growth
    times : numpy.ndarray, time points of the measurements
    volumes : numpy.ndarray, measured tumor volumes
    step_size : float, optional, initial step size for adjusting model parameters (default: 0.1)
    tolerance : float, optional, minimum step size used as stopping criterion (default: 1e-6)

    Returns
    -------
    dict, optimized model parameters
    float, mean squared error obtained with the optimized parameters
    """
    parameters = model.parameters.copy()

    steps = {}
    for key in parameters:
        steps[key] = step_size

    current_mse = calculate_error(model, solver, times, volumes, parameters)

    while max(steps.values()) > tolerance:
        for key in parameters:

            # Skip parameters when their step is below the tolerance, to cut down on processing time
            if abs(steps[key]) <= tolerance:
                continue

            new_parameters = parameters.copy()
            new_parameters[key] += steps[key]

            new_mse = calculate_error(model, solver, times, volumes, new_parameters)

            if new_mse < current_mse:
                parameters = new_parameters
                current_mse = new_mse

            else:
                new_parameters = parameters.copy()
                new_parameters[key] -= steps[key]

                new_mse = calculate_error(model, solver, times, volumes, new_parameters)

                if new_mse < current_mse:
                    parameters = new_parameters
                    current_mse = new_mse

                else:
                    steps[key] *= 0.2

    return parameters, current_mse
