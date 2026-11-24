import numpy as np

def bic(mse, n, k):
    """
    Calculate the Bayesian Information Criterion (BIC) using the
    mean squared error and the number of model parameters.

    Parameters
    ----------
    mse : float, mean of squared error of the fitted model
    n : int, number of measured points
    k : int, number of estimated model parameters

    Returns
    -------
    float: calculated BIC value. Lower values indicate a better
           balance between model fit and complexity

    Raises
    ------
    ValueError: if the MSE or n is less than or equal to 0
    """
    if n <= 0:
        raise ValueError("n must be greater than 0")
    if mse <= 0:
        raise ValueError("mse must be greater than 0")

    return n * np.log(mse) + k * np.log(n)