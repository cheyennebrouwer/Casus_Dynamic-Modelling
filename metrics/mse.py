import numpy as np

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