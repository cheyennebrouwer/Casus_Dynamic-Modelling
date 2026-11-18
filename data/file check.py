import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("synthetic_tumor_data.csv")

selected_ids = ["Model1_101", "Model2_255", "Model4_356"]

for tumor_id in df["ID"].unique():
    tumor = df[df["ID"] == tumor_id].sort_values("Times")

    plt.plot(
        tumor["Times"],
        tumor["Volume"],
        marker="o",
        label=tumor_id,
    )

plt.xlabel("Time (days)")
plt.ylabel("Tumor volume)")
plt.title("Tumor growth rate")
plt.legend()
plt.show()