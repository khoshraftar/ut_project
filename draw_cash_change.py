import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('cash_change.csv')
cash_data_x = []
cash_data_y = []
for row in df.iterrows():
    cash_data_x.append(row[1][0])
    cash_data_y.append(row[1][1])
plt.scatter(cash_data_x, cash_data_y)
plt.grid()
plt.show()

