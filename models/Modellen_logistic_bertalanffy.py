

def logistic_growth(t, V, r, K):
    """
    Calculate the tumor growth rate using the logistic model.

    Parameters
    ----------
    t : float, Time
    V : float, Current tumor volume
    r : float, Growth rate
    K : float, Carrying capacity (maximum tumor volume)

    Returns : float, Rate of change of tumor volume
    """

    return r * V * (1 - V / K)


def bertalanffy_growth(t, V, a, b):
    """
    Calculate the tumor growth rate using the Von Bertalanffy model.

    Parameters
    ----------
    t : float, Time
    V : float, Current tumor volume
    a : float, Growth coefficient
    b : float, Loss coefficient

    Returns : float, Rate of change of tumor volume
    """

    return a * V ** (2/3) - b * V