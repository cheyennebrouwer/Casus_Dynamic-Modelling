# Solver	Moet ieder model kunnen gebruiken zonder modelspecifieke aanpassingen.
# Optimalisatie	Moet de parameters van ieder model kunnen aanpassen.

# Modellen Cheyenne: Exponentieel en Gompertz
# Doen: Class aanmaken, per model een functie die zo min mogelijk hardcoded is
# Parameters/argumenten: Modelnaam, string; Tijd (t), float; Meerdere tijdstippen -> list/numpy.ndarray?;
# Tumorvolume (V), float; Groeiparameter (c), float; Maximale tumorgrootte (Vmax), float; ....
# Invoer: Tijd, volume, modelparameters
# Uitvoer: Verandering van tumorvolume per tijdseenheid

# Argumenten kunnen per model verschillen, gezien niet alle modellen hetzelfde berekenen!!

import math


class TumorGrowthModels:
    def __init__(self):
        pass

    def exponential(self, t, c, V):
        """Exponentieel model

        Parameters
        t : Time
        c : Tumor Growth
        V : Current Tumor Volume
        """
        return c ** V

    def gompertz(self, t, c, V, V_max):
        """Gompertz model

        Parameters
        t: Time
        c : Tumor Growth
        V : Current Tumor Volume
        V_max : Maximum Tumor Growth
        """
        return c * V * math.log(V_max / V)
