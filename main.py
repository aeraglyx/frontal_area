import statistics

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit

csv_path = "data_out.csv"
df = pd.read_csv(csv_path)

mass = df["mass"]
height = df["height"]
area = df["area"]

def power_law(x, a, b):
    return a * np.power(x, b)

def print_parameter(name, mean, perr):
    # 95% confidence interval
    print(f"{name} = {mean:.3f} ± {1.96 * perr:.3f}")

# def test_goodness_of_fit(popt, pcov, data_y):
#     perr = np.sqrt(np.diag(pcov))
#     dof = len(data_y) - len(popt)
#     t_values = popt / perr
#     p_values = [2 * (1 - stats.t.cdf(np.abs(t), dof)) for t in t_values]
#     print(", ".join([f"{m:.3f} ± {i:.3f} (95% CI)" for m, i in zip(popt, perr)]))
#     print("t-values:", ", ".join([f"{t:.3f}" for t in t_values]))
#     print("p-values:", ", ".join([f"{p:.3f}" for p in p_values]))

popt, pcov = curve_fit(power_law, mass, area)
perr = np.sqrt(np.diag(pcov))

print("\nFunction: a * mass ^ b\n")

print("Best Fit Parameters:")
print_parameter("a", popt[0], perr[0])
print_parameter("b", popt[1], perr[1])



c1 = area / np.power(mass, 0.75)
c1_avg = c1.mean()
print("\nIdealized:")
print(f"{c1_avg:.4f} * m ^ {0.75:.3f}")

print("")



x_fit = np.linspace(20, 100, 81)
y_fit = power_law(x_fit, *popt)

plt.scatter(mass, area, label="Data")
plt.plot(x_fit, y_fit, label="Fit")

plt.xlabel("Mass [kg]")
plt.ylabel("Area [m^2]")
plt.legend()
plt.show()
