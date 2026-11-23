import numpy as np

def euler_solver(model, t_span, V0, dt):
    """
    Solve a tumor growth ODE using the Euler method.

    Calculates tumor volume over time using the growth rate provided by a tumor growth model.

    Parameters
    ----------
    model: TumorGrowthModel, tumor growth model containing the derivative function and model-specific parameters.
    t_span: tuple, start and end times of the simulation
    V0: float, initial tumor volume
    dt: float, time step

    Returns
    -------
    times: numpy.ndarray, array containing the calculated time points.
    volumes: numpy.ndarray, array containing the calculated tumor volumes.
    """
    t_start, t_end = t_span

    times = [t_start]
    volumes = [V0]

    t = t_start
    V = V0

    while t < t_end:
        step = min(dt, t_end - t)

        # Stop the loop if the time step is negligibly small
        if step < 1e-12:
            break

        dv = model.derivative(t, V) * step

        V += dv
        t += step

        times.append(t)
        volumes.append(V)

    return np.array(times), np.array(volumes)