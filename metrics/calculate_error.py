import numpy as np

from models.base_model import TumorGrowthModel

from metrics.mse import mse

from solvers.euler import euler_solver
from solvers.ODE_scipy import solve_ode

def calculate_error(model, solver, times, volumes, parameters):
    """
    Simulates tumor growth using the given model and solver, then calculates the MSE.

    Parameters
    ----------
    model : TumorGrowthModel, class used for the simulation
    solver : callable, ODE solver to simulate tumor growth
    times : numpy.ndarray, time points of the measurements
    volumes : numpy.ndarray, measured tumor volumes
    parameters : dict, model parameters used for the simulation

    Returns
    -------
    float, mean squared error between measured and predicted tumor volumes
           Returns infinity if the simulation produces invalid values or raises
           a numerical error.

    Raises
    ------
    ValueError: if an unsupported solver is passed to the function
    """
    model_copy = TumorGrowthModel(
        model.name,
        model.function,
        parameters
    )

    t_span = (times[0], times[-1])
    V0 = volumes[0]
    dt = 0.1

    if solver not in (euler_solver, solve_ode):
        raise ValueError("Unsupported solver")

    try:
        if solver == euler_solver:
            calculated_times, calculated_volumes = solver(
                model_copy, t_span, V0, dt
            )

            predicted = np.interp(
                times, calculated_times, calculated_volumes
            )

        elif solver == solve_ode:
            predicted = solver(
                model_copy, times, V0
            )

    except (ValueError, OverflowError, FloatingPointError):
        return float("inf")

    if not np.all(np.isfinite(predicted)):
        return float("inf")

    if np.any(predicted <0):
        return float("inf")

    error = mse(volumes, predicted)

    if not np.isfinite(error):
        return float("inf")

    return error
