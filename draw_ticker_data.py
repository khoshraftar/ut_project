import sys

import pandas as pd

ticker = sys.argv[1]
df = pd.read_csv(f'tickers_data/{ticker}.csv')
monthly_prices = [[None for _ in range(12)] for _ in [2020, 2019, 2018, 2017, 2016, 2015]]
flatten_monthly_prices = []
for row in df.iterrows():
    date_parsed = list(map(int, row[1][0].split("-")))
    if date_parsed[0] not in [2020, 2019, 2018, 2017, 2016, 2015]:
        continue
    if not monthly_prices[date_parsed[0] - 2015][date_parsed[1] - 1]:
        monthly_prices[date_parsed[0] - 2015][date_parsed[1] - 1] = row[1][8]
        flatten_monthly_prices.append([row[1][0], row[1][8]])


x = [x[0] for x in flatten_monthly_prices]
y = [y[1] for y in flatten_monthly_prices]

import matplotlib.pyplot as plt
plt.scatter(x,y)
plt.scatter(x,[0 for _ in x])
plt.grid()
plt.show()