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

import pandas as pd
import numpy as np
import quandl
import matplotlib.pyplot as plt

def describeData(symbol):
    print("Available Columns")
    print(symbol.columns.values)
    print("Index", symbol.index.values)

    print(" Head")
    print(symbol.head())
    print(" Tail")
    print(symbol.tail())
    print(" Description")
    print(symbol.describe())


# Write the data to a file and then read it back in and return it
def readSymbolDataFromCSV(dataPath):
    return pd.read_csv(dataPath, header=0, index_col='Date', parse_dates=True)


def writeSymbolDatatoCSV(data, dataPath):
    data.to_csv(dataPath)
    return readSymbolDataFromCSV(dataPath)


# This method will get the data for a particular instrument
def getStockData(symbol, startTime, endTime):
    return quandl.get(symbol, start_date=startTime, end_date=endTime)


def resampleDataTime(symbol, term):
    return symbol.resample(term).mean()

def defineAbsolutGain(symbol):
    # Define absolut gains
    symbol["Open-Close"] = symbol.Open - symbol.Close
    # del aapl["Open-Close"]
    describeData(symbol)


'''
Visualization Tools
'''
def plotCloseValues(symbol):
    symbol['Close'].plot(grid=True)
    plt.title("Close Value")
    plt.show()


'''
Calculate Returns
'''

def calculateReturns(symbol):
    dailyClose = symbol[['Adj. Close']]
    dailyPCTChange = dailyClose.pct_change()  # Daily returns price change
    # Clean up the data by replacing NA with 0
    dailyPCTChange.fillna(0, inplace=True)
    # Find the daily log returns
    # a proxy for the percentage change in the price
    # Get better insight into the growth of a instrument
    dailyLogReturns = np.log(dailyClose.pct_change() + 1)

    print("Daily PCT Change:", dailyPCTChange)
    print("Daily Log Returns", dailyLogReturns)

    # Get Business monthly aggrigated data
    bm = resampleDataTime(symbol, 'BM').apply(lambda x: x[-1])
    # Get quartely data
    quarter = resampleDataTime(symbol, '4M')
    # Get the monthly % change
    bmPctChange = bm.pct_change()
    qPctChange = quarter.pct_change()

    print("Business Month % Change")
    print(bmPctChange)
    print("Quarter % Change")
    print(qPctChange)

    # Plot the PCT Change
    dailyPCTChange.hist(bins=50)
    plt.title("Pct Daily Change")
    # plt.show()

    # Cumulative daily rate of return
    # Used to determine the value of an investment at regular intervals
    cumDailyReturn = (1 + dailyPCTChange).cumprod()
    print("Cumulative daily rate of return:{}".format(cumDailyReturn))
    cumDailyReturn.plot()
    plt.title("Cumulative daily rate of return")
    # plt.show()

    cumMonthlyReturn = resampleDataTime(cumDailyReturn, "M")
    cumMonthlyReturn.plot()
    plt.title("Cumulative monthly rate of return")
    plt.show()
    # Returns the % Change
    return dailyPCTChange, dailyLogReturns, bmPctChange, qPctChange

def movingWindows(symbol):
    adjClosePx = symbol['Adj. Close']
    movingAvg = adjClosePx.rolling(window=40).mean()
    print("Moving Average:", movingAvg)

    # Short moving window rolling mean
    symbol['42'] = adjClosePx.rolling(window=40).mean()
    symbol['252'] = adjClosePx.rolling(window=252).mean()
    symbol[['Adj. Close', '42', '252']].plot()
    plt.title("Short vs Long moving window rolling mean")
    plt.show()

'''
Volatility Calculation
Measurement of change in variance in the returns of a stock over a specific period of time
The volatility is calculated by taking a 
rolling window standard deviation on the percentage change in a stock. 
Keep a close eye on the data sampling frequency 
'''

def calculateVolatility(minPeriod, dailyPCTChange):
        # Moving historical standard deviation of the log returns
        vol = dailyPCTChange.rolling(minPeriod).std() * np.sqrt(minPeriod)
        vol.plot()
        plt.title("Volatility")
        plt.show()

