import numpy as np
from scipy.integrate import solve_ivp
from typing import Any


def solve_ode(model, t_values, V0: float, method="RK45"):
    """
    Solve an ODE using SciPy.

    Parameters:
        model: Growth model containing a derivative() method.
        t_values: Time points.
        V0: Initial tumor volume.
        method: Integration method (default RK45).

    Returns:
        Array containing calculated tumor volumes.
    """

    t_values = np.asarray(t_values, dtype=float)

    if t_values.ndim != 1:
        raise ValueError("Time points must be a one-dimensional array.")

    if t_values.shape[0] < 2:
        raise ValueError("At least two time points are required.")

    if np.any(np.diff(t_values) <= 0):
        raise ValueError("Time points must be increasing.")

    if not np.isfinite(V0) or V0 < 0:
        raise ValueError("V0 must be finite and non-negative.")

# solution: Any helpt pycharm met typeherkenning
    solution: Any = solve_ivp(
        fun=lambda t, y: [model.derivative(t, y[0])],
        t_span=(float(np.min(t_values)), float(np.max(t_values))),
        y0=[V0],
        t_eval=t_values,
        method=method
    )

    if not solution.success:
        raise RuntimeError(solution.message)

    return solution.y[0]
