class TumorGrowthModel:
    """
    General class for a tumor growth model.

    Stores the model name, growth function and model parameters.
    Allows different tumor growth models to be evaluated using the same interface.

    Parameters
    ----------
    name : str, Name of the tumor growth model.
    function : callable, Function that calculates the rate of change of tumor volume.
    parameters : dictionary, Model-specific parameters and their values.
    """
    def __init__(self, name, function, parameters):
        self.name = name
        self.function = function
        self.parameters = parameters.copy()

    def derivative(self, t, V):
        """
        Calculate the rate of change of tumor volume.

        Parameters
        ----------
        t : float, Current time.
        V : float, Current tumor volume.

        Returns float, rate of change of tumor volume.
        """
        return self.function(t, V, **self.parameters)

    def set_parameters(self, **parameters):
        """
        Update the parameters of the tumor growth model.

        Parameters
        ----------
        **parameters : Dictionary of model-specific parameter names and their new values.

        Raises
        ------
        ValueError: if an unknown parameter is provided.
        """
        unknown = set(parameters) - set(self.parameters)

        if unknown:
            raise ValueError(f"Unknown parameters: {unknown}")

        self.parameters.update(parameters)