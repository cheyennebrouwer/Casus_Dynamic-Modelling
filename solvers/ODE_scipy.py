import numpy as np
from scipy.integrate import solve_ivp


def solve_ode(model, t_values, V0, method="RK45"):
    """
    Solve a tumor growth differential equation using SciPy.

    Parameters
    ----------
    model : TumorGrowthModel
        The tumor growth model to solve.

    t_values : array-like
        Time points at which the solution is evaluated.

    V0 : float
        Initial tumor volume.

    method : str
        Numerical integration method used by SciPy.
        Default is RK45.

    Returns
    -------
    numpy.ndarray
        Calculated tumor volumes at the requested time points.
    """

    # Convert time values to a NumPy array
    t_values = np.asarray(t_values, dtype=float)

    # Check input
    if t_values.ndim != 1 or len(t_values) < 2:
        raise ValueError("At least two time points are required.")

    if not np.all(np.isfinite(t_values)):
        raise ValueError("Time values must be finite.")

    if np.any(np.diff(t_values) <= 0):
        raise ValueError("Time values must be strictly increasing.")

    if V0 < 0:
        raise ValueError("Initial tumor volume cannot be negative.")

    if not np.isfinite(V0):
        raise ValueError("Initial tumor volume must be finite.")

    # Solve the differential equation
    solution = solve_ivp(
        fun=lambda t, y: [model.derivative(t, y[0])],
        t_span=(t_values[0], t_values[-1]),
        y0=[V0],
        t_eval=t_values,
        method=method
    )

    # Temporary debugging
    print(type(solution))
    print(solution.success)
    print(solution.message)
    print(solution.y)

    # Check whether the solver was successful
    if not solution.success:
        raise RuntimeError(solution.message)

    # Return the calculated tumor volumes
    return solution.y[0]

