### Project Overview
The aim of this Python package is to simulate and compare different tumor growth models using any kind of tumor growth data. Users can provide their own datasets, allowing the package to be used for different tumor growth analyses.

The package solves ordinary differential equations (ODEs) using numerical solvers, optimizes model parameters, and evaluates the performance of different models using statistical comparison criteria.

By comparing the different models, solvers and optimization methods, users can determine which combination describes their tumor growth data in the best way. 

### Installation and requirements
To use this package, clone the repository to your local computer and open the project folder in an IDE or terminal. 

The package was developed using python 3.12.6

The following Python libraries are required:
| Library | Version | Purpose |
|---|---|---|
| Numpy | 2.1.3 | Numerical calculations and arrays |
| Pandas | 2.2.3 | Reading CSV files and displaying results |
| SciPy | 1.17.1 | Solving ordinary differential equations |

The required libraries can be installed by using:
`pip install numpy pandas scipy`

The input data must be provided in CSV format and must contain the following: tumor identifiers, measurement time points and corresponding tumor volumes. The column names can be specified by the user. The time points and volumes must me numerical.

Each tumor should have multiple measurements at different time points to allow model fitting and comparison.

### Project Structure

```text
Casus_Dynamic-Modelling/
├── Comparison/
│   ├── AICc.py
│   └── BIC.py
├── data/
│   └── synthetic_tumor_data.csv
├── metrics/
│   ├── calculate_error.py
│   └── mse.py
├── models/
│   ├── base_model.py
│   ├── bertalanffy_model.py
│   ├── Exponential.py
│   ├── gompertz.py
│   └── logistic_model.py
├── optimization/
│   ├── hooke_jeeves.py
│   └── monte_carlo.py
├── solvers/
│   ├── euler.py
│   └── ODE_scipy.py
├── model_comparison.py
└── README.md
```
The project is organized into separate modules for tumor growth models, numerical solvers, parameter optimization, error calculation and model comparison.

The models directory contains the mathematical tumor growth models, while solvers contains the numerical methods used to solve them. The optimization directory contains the methods used to improve model parameters.

The metrics and Comparison directories contain functions for calculating model errors and evaluating model performance.

The main script, model_comparison.py, combines these components to compare the models using a selected dataset.

### Usage
Users can provide their own tumor growth data in CSV format. The user specifies the path to the CSV file using the --file argument. 

The column names for tumor IDs, time points, and tumor volumes can be specified separately by using --id-column, --time, and --volume.

the --tumor-id argument is optional and allows users to analyze a specific tumor. If no tumor ID is specified, all tumors in the dataset will be analyzed.

#### Command-line arguments
| Argument | Description | Required |
|---|---|---|
|`--file` | Path to the CSV file | Yes |
| `--id-column` | Column containing tumor IDs | Yes |
| `--time` | Column containing time points | Yes |
| `--volume` | Column containing tumor volumes | Yes |
| `--tumor-id` | Specific tumor ID to analyze | No |

##### Example
`python .\model_comparison.py --file .\data\synthetic_tumor_data.csv --id-column ID --time Times --volume Volume --tumor-id Model1_101`

Users can replace the file path and column names with those corresponding to their own CSV dataset. The --tumor-id argument can be omitted to analyze all tumors.

The available command-line arguments can also be displayed using: 
`python model_comparison.py --help`

### Implemented Methods

##### Tumor Growth Models
Four mathematical models are implemented to simulate tumor growth overtime.

- **Exponential Growth:** Assumes that tumor growth is proportional to the current tumor volume. The model uses one parameter, c, which determines the growth rate.
- **Logistic Growth:** Describes that the tumor growth gradually slows down as the volume approaches a carrying capacity. The model uses the growth rate r and the carrying capacity K.
- **Gompertz Growth:** Describes the tumor growth that slows down as the volume approaches a limiting value. The parameters c and V_max determine the growth behavior.
- **Von Bertalanffy Growth:** Describes the tumor growth through a balance between growth and loss processes. The parameters a and b determine the contribution of these processes.

The models use ordinary differential equations to describe how tumor volume changes overtime.

##### Numerical Solvers
The package includes two numerical solvers for solving the differential equations.

###### Euler Method
The Euler method estimates the next tumor volume based on the current volume and its rate of change. It uses a fixed time step and was implemented manually in Python.

###### SciPy Solver
The SciPy solver uses the solve_ivp() function with the RK45 method. This solver uses adaptive internal time steps to calculate the tumor volumes while controlling numerical error.

Using both solvers allows the results of a manually implemented numerical method to be compared with those of a solver from SciPy.

##### Parameter Optimization
Two optimization methods are implemented to find parameter values that minimize the difference between measured and predicted tumor volumes. 

###### Hooke-Jeeves
Hooke-Jeeves is a local optimization method that adjusts model parameters step by step. When an adjustment improves the model fit, the new parameter values are retained. If no improvement is found, the step size is reduced.

###### Monte Carlo
Monte Carlo uses randomly generated parameter combinations within predefined search ranges. Each combination is evaluated, and a new parameter set is retained when it produces a lower error.

Because Monte Carlo uses random values, its results may differ between executions. 

Both optimization methods use the mean squared error (MSE) to evaluate paraneter combinations.

##### Model Evaluation
The package uses three criteria to evaluate model performance:

- **Mean Squared Error (MSE):** Measures the average squared difference between measured and predicted tumor volumes. Lower values indicate a closer fit to the measurements.
- **Corrected Akaike Information Criterion (AICc):** Evaluates model fit while accounting for the number of parameters, including a correction for small datasets.
- **Bayesian Information Criterion (BIC):** Evaluates model fit while applying a penalty for model complexity.

For models fitted to the same dataset, lower AICc and BIC values indicate a more favorable balance between model fit and complexity.

### Output and Interpretation
The results are displayed as a table in the terminal. Each row represents a combination of a tumor growth model, numerical solver, and optimization method.

The output contains the following information:
| Column | Description |
|---|---|
| Tumor ID | Identifier of the analyzed tumor |
| Model | Tumor growth model used for the simulation |
| Solver | Numerical solver used to solve the ODE |
| Optimizer | Optimization method used to estimate the parameters |
| Parameters | Optimized parameter values for the model |
| MSE       | Mean squared error between measured and predicted values |
| AICc| Corrected Akaike Information Criterion |
| BIC | Bayesian Information Criterion |

For every tumor, the package evaluates four models using two solvers and two optimization methods. This results in 16 combinations per tumor.

The results can be compared to determine which combinations describe the measured tumor volumes most closely.

A lower MSE indicates a better fit to the measurements, while AICc and BIC also take the number of model parameters into account. These criteria can help identify suitable models for the selected dataset.

However, the model with the lowest error is not necessarily the most biologically realistic model.

### Example User Case
A Jupyter Notebook is included to demonstrate how the package can be used to analyze tumor growth data.

The notebook applies the implemented method to a selected dataset and visualizes the measured tumor volumes alongside the simulated growth curves. It also demonstrates how the results can be compared and interpreted.

### Limitations
The tumor growth models are simplified mathematical representations of tumor growth and do not account for biological processes like the immune system or treatment.

The accuracy of the results depends on the quality of the dataset, the selected model, and the optimization method. Different parameter values and optimization methods may lead to different results.

A model that fits one dataset well might not necessarily perform well on other datasets.

### References
Murphy, H., Jaafari, H., & Dobrovolny, H. M. (2016). Differences in predictions of ODE models of tumor growth: A cautionary example. BMC Cancer, 16, 163. https://doi.org/10.1186/s12885-016-2164-x

SciPy Developers. scipy.integrate.solve_ivp — SciPy documentation. 
https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html

Odziemczyk, W. (2021). Application of Optimization Algorithms for Identification of Reference Points in a Monitoring Network. Sensors, 21(5), 1739. https://doi.org/10.3390/s21051739

MathWorks. Information Criteria for Model Selection. 
https://www.mathworks.com/help/econ/information-criteria.html