# importing librarys
import pandas as pd

# importing models
from models.base_model import TumorGrowthModel
from models.bertalanffy_model import bertalanffy_growth
from models.Exponential import exponential
from models.gompertz import gompertz
from models.logistic_model import logistic_growth

# importing solvers
from solvers.ODE_scipy import solve_ode
from solvers.euler import euler_solver

# importing optimization
from optimization.hooke_jeeves import hooke_jeeves

# importing model comparison criteria
from Comparison.AICc import aicc
from Comparison.BIC import bic

# Model1_101, Model1_109, Model2_254, Model4_353

# Read the data
data = pd.read_csv("data/synthetic_tumor_data.csv")

tumor_id = "Model1_101"
tumor_data = data[data["ID"] == tumor_id]
tumor_data = tumor_data.sort_values("Times")

times = tumor_data["Times"].to_numpy()
volumes = tumor_data["Volume"].to_numpy()

# Creating dictionary for the models
models = {
    "Logistic": TumorGrowthModel(
        "Logistic", logistic_growth, {"r": 0.2, "K": 1000}
    ),
    "Von Bertalanffy": TumorGrowthModel(
        "Von Bertalanffy", bertalanffy_growth, {"a": 0.5, "b": 0.1}
    ),
    "Exponential": TumorGrowthModel(
        "Exponential", exponential, {"c": 0.2}
    ),
    "Gompertz": TumorGrowthModel(
        "Gompertz", gompertz, {"c": 0.2, "V_max": 1000}
    )
}

# Creating dictionary for the solvers
solvers = {
    "Euler": euler_solver,
    "SciPy": solve_ode
}

results = {}

for model_name, model in models.items():
    results[model_name] = {}

    for solver_name, solver in solvers.items():
        best_parameters, best_mse = hooke_jeeves(
            model,
            solver,
            times,
            volumes
        )

        n = len(times)
        k = len(best_parameters)

        aicc_value = aicc(best_mse, n, k)
        bic_value = bic(best_mse, n, k)

        results[model_name][solver_name] = {
            "parameters": best_parameters,
            "mse": best_mse,
            "aicc": aicc_value,
            "bic": bic_value,
        }

for model_name, model_results in results.items():
    for solver_name, result in model_results.items():
        print("----------------------------------")
        print("Model:", model_name)
        print("Solver:", solver_name)
        print("Parameters:", result["parameters"])
        print("MSE:", round(result["mse"], 2))
        print("AICC:", round(result["aicc"], 2))
        print("BIC:", round(result["bic"], 2))
        print("----------------------------------")