import numpy as np
from models.base_model import TumorGrowthModel
from metrics.mse import mse

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