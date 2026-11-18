def exponential(self, t, r, V):
    """Exponentieel model

    Parameters
    t : Time
    r : Tumor Growth
    V : Current Tumor Volume
    """
    return r ** V
