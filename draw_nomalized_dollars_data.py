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
nomalized_data_y = [0]
for i in range(1, len(dollar_data_y)):
    nomalized_data_y.append((dollar_data_y[i]-dollar_data_y[i-1])/dollar_data_y[i-1])
plt.scatter(dollar_data_x, [0 for _ in dollar_data_x])
plt.scatter(dollar_data_x, nomalized_data_y)
plt.show()
