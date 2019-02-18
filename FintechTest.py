#!/usr/bin/env python

'''
# Short Description@
# 
# Full Description@
# 
__author__ = "Matthew Millar"
__copyright__ = ""
__credits__ =
__license__ = ""
__version__ = "0.0.0"
__maintainer__ = "Matthew Millar"
__email__ = "matthew.millar@igniterlabs.com"
__status__ = "Dev"

'''

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from TradingAlgoUtilities import DataExplorationUtils as DEU


instrument = "WIKI/AAPL" # Quandl Code for each stock
start = "2006-10-01"
end = "2018-01-01"

storedDataPath = "data/data.csv"


# Check to see if the file exsist or not
# If it does not then write it to the path for saving
if os.path.isfile(storedDataPath):
    # Read in from the stored data place
    aapl = DEU.readSymbolDataFromCSV(storedDataPath)
else:
    # Get the data from the internet
    aapl = DEU.getStockData(instrument, start, end)
    DEU.writeSymbolDatatoCSV(aapl, storedDataPath)

# Resample the data to monthly view
monthlyAAPL = DEU.resampleDataTime(aapl, 'M')


# Define absolut gains
print("Absolut Gains")
DEU.defineAbsolutGain(aapl)

'''
Visualization of Data
'''
DEU.plotCloseValues(aapl)

'''
Calculate Returns
'''
dailyPCTChange, dailyLogReturns, bmPctChange, qPctChange = DEU.calculateReturns(aapl)

'''
Moving Windows
'''
DEU.movingWindows(aapl)

'''
Calculate Volatility
'''
# Moving historical standard deviation of the log returns
minPeriod = 75
DEU.calculateVolatility(minPeriod, dailyPCTChange)

'''
Trading Strategies 
Momentum Strategy: stocks have momentum or upward or downward trends, 
that you can detect and exploit.
Moving average crossover, dual moving average crossover , turtle trading are examples
'''

'''
The moving average crossover is when the price of an asset moves from one side 
of a moving average to the other. This crossover represents a change in momentum
 and can be used as a point of making the decision to enter or exit the market.

The dual moving average crossover occurs when a short-term average crosses a 
long-term average. This signal is used to identify that momentum is shifting in
the direction of the short-term average. 
A buy signal is generated when the short-term average crosses the long-term 
average and rises above it, while a sell signal is triggered by a 
short-term average crossing long-term average and falling below it.

Turtle trading is a popular trend following strategy that was initially 
taught by Richard Dennis. The basic strategy is to buy futures on a 
20-day high and sell on a 20-day low.
'''

'''
Reversion Strategy
The movement of a quantity will eventrually reverse. 

mean reversion strategy
Where stocks will return to their mean and you can take advantage of them
once they are there

Pairs Trading mean reversion
If two stocks have a high correlation that change in the differnce in price between
the two stocks can show a trading event
'''


'''
Simple Trading algo
Moving avergage crossover
create two separate Simple Moving Averages (SMA) of a time series with 
differing lookback periods, let’s say, 40 days and 100 days. 
If the short moving average exceeds the long moving average then you go long,
 if the long moving average exceeds the short moving average then you exit.
 Long = buy
 short = sell
'''

shortWndow = 40
longWindow = 100

# Create the signals
signals = pd.DataFrame(index=aapl.index)
signals['signal'] = 0.0

# Create short simple moving avg over short window
signals['short_mavg'] = aapl['Close'].rolling(window=shortWndow,
                                              min_periods=1,
                                              center=False).mean()

# Create a long simple moving avg over the long window
signals['long_mavg'] = aapl['Close'].rolling(window=longWindow,
                                             min_periods=1,
                                             center=False).mean()

# Create the signals
signals['signal'][shortWndow:] =\
    np.where(signals['short_mavg'][shortWndow:] >
             signals['long_mavg'][shortWndow:], 1.0, 0.0)


# Create tradding orders
signals['positions'] = signals['signal'].diff()

# print the signals
print(signals)

fig = plt.figure()

# Add a subplot and label for y-axis
ax1 = fig.add_subplot(111, ylabel='Price in $')

# Plot the closing price
aapl['Close'].plot(ax=ax1, color='b', lw=2.)

# Plot the short and long moving averages
signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

# Plot the buy signals
ax1.plot(signals.loc[signals.positions == 1.0].index,
         signals.short_mavg[signals.positions == 1.0],
         '^', markersize=10, color='g')

# Plot the sell signals
ax1.plot(signals.loc[signals.positions == -1.0].index,
         signals.short_mavg[signals.positions == -1.0],
         'v', markersize=10, color='r')

# Show the plot
#plt.show()

'''
Backtesting the simple algo
'''

initialCapital = float(100000.0)

# Create a DataFrame `positions`
positions = pd.DataFrame(index=signals.index).fillna(0.0)

# Buy a 100 shares
positions['AAPL'] = 100*signals['signal']

# Initialize the portfolio with value owned
portfolio = positions.multiply(aapl['Adj. Close'], axis=0)

# Store the difference in shares owned
pos_diff = positions.diff()

# Add `holdings` to portfolio
portfolio['holdings'] = (positions.multiply(aapl['Adj. Close'], axis=0)).sum(axis=1)

# Add `cash` to portfolio
portfolio['cash'] = initialCapital - (pos_diff.multiply(aapl['Adj. Close'], axis=0)).sum(axis=1).cumsum()

# Add `total` to portfolio
portfolio['total'] = portfolio['cash'] + portfolio['holdings']

# Add `returns` to portfolio
portfolio['returns'] = portfolio['total'].pct_change()

# Print the first lines of `portfolio`
print(portfolio.head())


# Create a figure to show the back testing
fig = plt.figure()

ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')

# Plot the equity curve in dollars
portfolio['total'].plot(ax=ax1, lw=2.)

ax1.plot(portfolio.loc[signals.positions == 1.0].index,
         portfolio.total[signals.positions == 1.0],
         '^', markersize=10, color='m')
ax1.plot(portfolio.loc[signals.positions == -1.0].index,
         portfolio.total[signals.positions == -1.0],
         'v', markersize=10, color='k')

# Show the plot
plt.show()


'''
Evaluatioins tools
'''

'''
harpe ratio to get to know whether your portfolio’s returns are the result 
of the fact that you decided to make smart investments or to take a lot of risks
'''
# Isolate the returns of your strategy
returns = portfolio['returns']

# annualized Sharpe ratio
sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())

# Print the Sharpe ratio
print(sharpe_ratio)

'''
Maximum Drawdown, which is used to measure the largest single drop from peak to 
bottom in the value of a portfolio, 
so before a new peak is achieved. In other words, the score indicates the risk
 of a portfolio chosen based on a certain strategy.
'''

# Define a trailing 252 trading day window
window = 252

# Calculate the max drawdown in the past window days for each day
rolling_max = aapl['Adj. Close'].rolling(window, min_periods=1).max()
daily_drawdown = aapl['Adj. Close']/rolling_max - 1.0

# Calculate the minimum (negative) daily drawdown
max_daily_drawdown = daily_drawdown.rolling(window, min_periods=1).min()

# Plot the results
daily_drawdown.plot()
max_daily_drawdown.plot()

# Show the plot
plt.show()

'''
Compound Annual Growth Rate (CAGR), which provides you with a 
constant rate of return over the time period. In other words,
 the rate tells you what you really have at the end of your investment period. 
'''

# Get the number of days in `aapl`
days = (aapl.index[-1] - aapl.index[0]).days

# Calculate the CAGR
cagr = ((((aapl['Adj. Close'][-1]) / aapl['Adj. Close'][1])) ** (365.0/days)) - 1

# Print the CAGR
print(cagr)