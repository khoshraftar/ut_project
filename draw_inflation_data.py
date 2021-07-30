import datetime

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('mid_inflation_data.csv')
inflation_data_x = []
inflation_data_y = []
for row in df.iterrows():
    inflation_data_x.append(datetime.datetime.strptime(row[1][0], "%Y-%m-%d"))
    inflation_data_y.append(row[1][1])
plt.plot(inflation_data_x, inflation_data_y)
plt.title("Inflation change percentage")
plt.grid()
plt.show()

