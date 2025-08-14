import matplotlib
matplotlib.use('MacOSX')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# variables
input_red_wine = "winequality-red.csv"
input_white_wine = "winequality-white.csv"

# load data
wine_data = pd.read_csv(input_red_wine, delimiter=";")

# bar chart with quality of wines
sns.countplot(x="quality", data=wine_data)
plt.show()

# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(wine_data.corr(), annot=True, cmap="coolwarm")
plt.show()