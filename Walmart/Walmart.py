import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# import data
walmart_data = pd.read_csv('walmart.csv')


# Plotting revenue by age
sns.set_theme(style="whitegrid")

# Initialize the matplotlib figure
f, ax = plt.subplots(figsize=(6, 15))

# Plot the total crashes
sns.set_color_codes("pastel")
sns.barplot(x="Purchase", y="Age", data=walmart_data,
            label="Total", color="b")

# Add a legend and informative axis label
ax.legend(ncol=2, loc="lower right", frameon=True)
ax.set(ylabel="",
       xlabel="Revenue by age")
sns.despine(left=True, bottom=True)
plt.show()