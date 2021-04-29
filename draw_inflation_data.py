import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('mid_inflation_data.csv')
inflation_data_x = []
inflation_data_y = []
for row in df.iterrows():
    inflation_data_x.append(row[1][0])
    inflation_data_y.append(row[1][1])
plt.scatter(inflation_data_x, inflation_data_y)
plt.grid()
plt.show()

