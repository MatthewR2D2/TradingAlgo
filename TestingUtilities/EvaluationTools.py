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

import numpy as np
import matplotlib.pyplot as plt

'''
sharpe ratio to get to know whether your portfolio’s returns are the result 
of the fact that you decided to make smart investments or to take a lot of risks
'''
def sharpeRatio(portfolio):

    # Isolate the returns of your strategy
    returns = portfolio['returns']

    # annualized Sharpe ratio
    sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())

    # Print the Sharpe ratio
    print("Sharpe Ratio:", sharpe_ratio)


'''
Compound Annual Growth Rate (CAGR), which provides you with a 
constant rate of return over the time period. In other words,
 the rate tells you what you really have at the end of your investment period. 
'''

def cagrCalculation(symbol):
    # Get the number of days in `aapl`
    days = (symbol.index[-1] - symbol.index[0]).days
    # Calculate the CAGR
    cagr = ((((symbol['Adj. Close'][-1]) / symbol['Adj. Close'][1])) ** (365.0 / days)) - 1
    # Print the CAGR
    print("Compund Annual Growth Rate: ", cagr)


'''
Maximum Drawdown, which is used to measure the largest single drop from peak to 
bottom in the value of a portfolio, 
so before a new peak is achieved. In other words, the score indicates the risk
 of a portfolio chosen based on a certain strategy.
'''
def maxDailyDrawdown(symbol, window):


    # Calculate the max drawdown in the past window days for each day
    rolling_max = symbol['Adj. Close'].rolling(window, min_periods=1).max()
    daily_drawdown = symbol['Adj. Close'] / rolling_max - 1.0

    # Calculate the minimum (negative) daily drawdown
    max_daily_drawdown = daily_drawdown.rolling(window, min_periods=1).min()

    # Plot the results
    daily_drawdown.plot()
    max_daily_drawdown.plot()

    # Show the plot
    plt.title("Drawdown")
    plt.show()