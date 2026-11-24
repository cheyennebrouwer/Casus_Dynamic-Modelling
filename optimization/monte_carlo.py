from random import gauss
from optimization.hooke_jeeves import mse


def monte_carlo():
    # Initialisatie van onbekende waarden
    params = {
        'a': 0.0,
        'b': 0.0,
        'y0': 0.0,
    }

    # Herhaaldelijke aanpassing
    current_mse = mse(**params)
    tries = 0
    while tries < 1000:
        tries += 1
        new_params = {key: val + gauss(sigma=0.01) for key, val in params.items()}
        new_mse = current_mse(**new_params)
        if new_mse < current_mse:
            params = new_params
            current_mse = new_mse
            tries = 0


# a, b, N = 0, np.pi, 1000
#
#
# def f(x):
#     return np.sin(x)
#
#
# x_random = np.random.uniform(a, b, N)
# estimate = (b - a) * np.mean(f(x_random))
#
# print(f"Monte Carlo Estimate: {estimate:.4f}")
#
# repeats = 1000
# estimates = []
#
# for _ in range(repeats):
#     x_samples = np.random.uniform(a, b, N)
#     estimates.append((b - a) * np.mean(f(x_samples)))
#
# plt.hist(estimates, bins=30, edgecolor='black')
# plt.title("Monte Carlo Estimate Distribution")
# plt.xlabel("Estimate")
# plt.ylabel("Frequency")
# plt.show()
