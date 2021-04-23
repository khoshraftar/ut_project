import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('dollar.csv')
dollar_data_x = []
dollar_data_y = []
for row in df.iterrows():
    dollar_data_x.append(row[1][0])
    dollar_data_y.append(row[1][1])
dollar_data_x = list(reversed(dollar_data_x))
dollar_data_y = list(reversed(dollar_data_y))
plt.scatter(dollar_data_x, [0 for _ in dollar_data_x])
plt.scatter(dollar_data_x, dollar_data_y)
plt.show()
