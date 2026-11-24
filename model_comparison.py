# importing librarys
import pandas as pd
import argparse

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
from optimization.monte_carlo import monte_carlo

# importing model comparison criteria
from Comparison.AICc import aicc
from Comparison.BIC import bic

# Model1_101, Model1_109, Model2_254, Model4_353

# Read the data
def load_data(file_path):
    """
    Loads a CSV file into a Pandas DataFrame

    :param file_path: Path to the CSV file

    :return: Pandas DataFrame
    """
    data = pd.read_csv(file_path)

    return data


def select_tumor_data(data, id_column, time_column, volume_column, tumor_id):
    """
    Selects and sorts the measurements of a specific tumor and collects columns from the dataframe

    :param data: Pandas DataFrame
    :param id_column: Column containing the tumor IDs
    :param time_column: Column containing the time points
    :param volume_column: Column containing the tumor volumes
    :param tumor_id: Optional entry to analyze a specified tumor ID

    :return: Pandas DataFrame with sorted measurement times and tumor volumes
    """
    tumor_data = data[data[id_column] == tumor_id]
    tumor_data = tumor_data.sort_values(time_column)

    times = tumor_data[time_column].to_numpy()
    volumes = tumor_data[volume_column].to_numpy()

    return times, volumes


def parse_arguments():
    """
    Parses command line arguments for the model comparison

    :return: Dictionary of arguments
    """
    parser = argparse.ArgumentParser(
        description="Analyze tumor growth models using a CSV dataset"
    )

    parser.add_argument("--file", required=True, help="Path to the CSV file")
    parser.add_argument("--id-column", required=True, help="Column containing the tumor IDs")
    parser.add_argument("--time", required=True, help="Column containing the time points")
    parser.add_argument("--volume", required=True, help="Column containing the tumor volume")
    parser.add_argument("--tumor-id", required=False, help="Optional entry to analyze a specified tumor ID")

    return parser.parse_args()


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

# Creating dictionary for the optimizers
optimizers = {
    "Hooke-jeeves": hooke_jeeves,
    "Monte-Carlo": monte_carlo,
}


def run_comparison(data, id_column, time_column, volume_column, tumor_id=None):
    """
    Fits and compares tumor growth models using different solvers and optimizers.

    For each selected tumor, the function optimizes the parameters of each model and calculates the
    MSE, AICc and BIC.

    :param data: Pandas DataFrame
    :param id_column: Column containing the tumor IDs
    :param time_column: Column containing the time points
    :param volume_column: Column containing the tumor volumes
    :param tumor_id: Optional entry to analyze a specified tumor ID

    :return: list of dictionaries containing the model, solver, optimizer, optimized parameters,
             MSE, AICc and BIC for each tumor

    :raises: ValueError, If the specified tumor ID is not found in the dataset
    """
    results = []

    if tumor_id is not None:
        if tumor_id not in data[id_column].values:
            raise ValueError(f"Tumor ID '{tumor_id}' not found in data")

        tumor_ids = [tumor_id]
    else:
        tumor_ids = data[id_column].unique()

    for tumor_id in tumor_ids:
        times, volumes = select_tumor_data(
            data,
            id_column,
            time_column,
            volume_column,
            tumor_id
        )

        for model_name, model in models.items():
            for solver_name, solver in solvers.items():
                for optimizer_name, optimizer in optimizers.items():
                    best_parameters, best_mse = optimizer(
                        model,
                        solver,
                        times,
                        volumes
                    )

                    n = len(times)
                    k = len(best_parameters)

                    aicc_value = aicc(best_mse, n, k)
                    bic_value = bic(best_mse, n, k)

                    results.append({
                        "Tumor ID": tumor_id,
                        "Model": model_name,
                        "Solver": solver_name,
                        "Optimizer": optimizer_name,
                        "Parameters": best_parameters,
                        "MSE": best_mse,
                        "AICc": aicc_value,
                        "BIC": bic_value
                    })
    return results


def print_results(results):
    """
    Displays the model comparison results as a table in the terminal.

    Parameter values are rounded to 6 decimal places for readability.

    :param results: list of dictionaries containing the model, solver, optimizer, optimized parameters,
                    MSE, AICc and BIC for each tumor
    """
    for result in results:
        parameters = result["Parameters"]

        for name in parameters:
            parameters[name] = round(parameters[name], 6)

    results_df = pd.DataFrame(results)
    print(results_df.to_string(
        index=False,
        float_format="%.2f",
    ))

def main():
    """
    Runs the model comparison from the command line.

    Loads the dataset, executes the model comparison and displays the results in the terminal.
    """
    args = parse_arguments()

    data = load_data(args.file)

    results = run_comparison(
        data,
        args.id_column,
        args.time,
        args.volume,
        args.tumor_id
    )

    print_results(results)

if __name__ == "__main__":
    main()