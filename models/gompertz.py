def gompertz(self, t, c, V, V_max):
    """Gompertz model

    Parameters
    t: Time
    c : Tumor Growth
    V : Current Tumor Volume
    V_max : Maximum Tumor Growth
    """
    return c * V * math.log(V_max / V)
