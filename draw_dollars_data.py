import datetime

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('dollar.csv')
dollar_data_x = []
dollar_data_y = []
i = 0
for row in df.iterrows():
    dollar_data_y.append(row[1][1])
    if not i % 20:
        dollar_data_x.append(datetime.datetime.strptime(row[1][0], "%Y-%m-%d"))
    else:
        dollar_data_x.append("")
dollar_data_x = list(reversed(dollar_data_x))
dollar_data_y = list(reversed(dollar_data_y))
plt.plot(dollar_data_x, dollar_data_y)
plt.grid()
plt.title("dollar price")
plt.show()
