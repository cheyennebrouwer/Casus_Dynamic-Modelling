import math


def gompertz(self, t, r, V, V_max):
    """Gompertz model

    Parameters
    t: Time
    r : Tumor Growth
    V : Current Tumor Volume
    V_max : Maximum Tumor Growth
    """
    return r * V * math.log(V_max / V)
