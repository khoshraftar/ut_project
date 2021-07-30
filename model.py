import sys
from datetime import datetime
from math import sqrt

import pandas as pd
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot
from sklearn.metrics import mean_squared_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller


def parse_date(df):
    df['date'] = pd.to_datetime(df["date"])
    df = df.set_index("date")
    df.index = df.index.to_period("M")
    return df


def get_ticker_dataframe():
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

    normalized_flatten_prices = [[flatten_monthly_prices[0][0], 0]]
    # normalize
    for x in range(1, len(flatten_monthly_prices)):
        normalized_flatten_prices.append([
            flatten_monthly_prices[x][0],
            (flatten_monthly_prices[x][1] - flatten_monthly_prices[x - 1][1]) / flatten_monthly_prices[x - 1][1]]
        )
    df = pd.DataFrame(normalized_flatten_prices, columns=["date", "change"])
    return parse_date(df)


def get_dollar_dataframe():
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
        nomalized_data_y.append((dollar_data_y[i] - dollar_data_y[i - 1]) / dollar_data_y[i - 1])
    df = pd.DataFrame(zip(dollar_data_x, nomalized_data_y), columns=["date", "change"])
    return parse_date(df)


def get_inflation_dataframe():
    df = pd.read_csv('mid_inflation_data.csv', names=["date", "change"])
    return parse_date(df)


def get_cash_dataframe():
    df = pd.read_csv('cash_change.csv')
    return parse_date(df)


def draw_series(values):
    pyplot.plot(values)
    pyplot.show()


ticker_values = get_ticker_dataframe().values
dollar_values = get_dollar_dataframe().values
inflation_values = get_inflation_dataframe().values
cash_values = get_cash_dataframe().values
index = get_ticker_dataframe().index
combined_values = []
for i in range(len(ticker_values)):
    a = float(0.5 * dollar_values[i] + 0.5 * inflation_values[i] - 0 * cash_values[i])
    combined_values.append(a)

x = []
dt = datetime(2015, 1, 1)
while dt < datetime(2021, 1, 1):
    x.append(dt)
    dt += relativedelta(months=1)

size = int(len(ticker_values) * 0.66)
train, test = ticker_values[0:size], ticker_values[size:len(ticker_values)]
x_train, x_test = x[0:size], x[size:len(ticker_values)]
# stationary test
draw_series(values=ticker_values)
result = adfuller(ticker_values)
print('p-value: %f' % result[1])
# 1st order differencing
draw_series(get_ticker_dataframe().diff().values)
result = adfuller(get_ticker_dataframe().diff().dropna().values)
print('p-value: %f' % result[1])

# ACF and PACF
plot_acf(pd.DataFrame(train), lags=22)
pyplot.show()
#
plot_pacf(pd.DataFrame(train), lags=22)
pyplot.show()

# def get_pdq(time_series):
#     plot_acf(time_series)
#     plot_pacf(time_series)
#     pyplot.show()
#
#     r,rac,Q = acf(time_series, qstat=True , nlags=34)
#     prac = pacf(time_series,method='ywmle', nlags= 34)
#     table_data = numpy.c_[range(1,len(r)), r[1:],rac,prac[1:len(rac)+1],Q]
#     table = pd.DataFrame(table_data, columns=['lag', "AC","Q", "PAC", "Prob(>Q)"])
#     print(table)
#
# get_pdq(pd.DataFrame(combined_values))

history = [x for x in train]
predictions = list()
# walk-forward validation
for t in range(len(test)):
    model = ARIMA(history, order=(3, 1, 3), exog=combined_values[:len(history)])
    model_fit = model.fit()
    output = model_fit.forecast(exog=combined_values[len(history)])
    yhat = output[0]
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)
    print('predicted=%f, expected=%f' % (yhat, obs))
# evaluate forecasts
rmse = sqrt(mean_squared_error(test, predictions) * 0.66)
print('Test RMSE: %.3f' % rmse)
# plot forecasts against actual outcomes
pyplot.plot(x_test, test, label="test")
pyplot.plot(x_test, predictions, color='red', label="prediction")
pyplot.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
pyplot.show()
