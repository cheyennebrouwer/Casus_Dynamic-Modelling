import numpy as np

def aicc(mse, n, k):
    """
    Calculate the corrected Akaike information criterion (AICc)
    using the mean squared error and the number of model parameters

    Parameters
    ----------
    mse : float, mean squared error of the fitted model
    n: int, number of measured points
    k : int, number of estimated model parameters

    Returns
    -------
    float: calculated AICc value. Lower values indicate a better
           balance between model fit and complexity

    Raises
    ------
    ValueError: if there are too few measurement points or the MSE
                is less or equal to 0
    """
    if n <= k + 1:
        raise ValueError("Not enough data points to calculate AICc")

    if mse <= 0:
        raise ValueError("mse must be positive")

    return n * np.log(mse) + (2 * k * n) / (n - k - 1)

