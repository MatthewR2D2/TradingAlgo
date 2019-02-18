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
from TradingAlgo.MovingWindowAlgo import MovingWindowStrategy as MWS
from TradingAlgoUtilities import DataExplorationUtils as DEU
from TestingUtilities import EvaluationTools as EveT
from TestingUtilities import BacktestingAlgo as BTA
from TradingAlgo.VWAP import VWAP
from TradingAlgo.TWAP import TWAP

'''
Available Columns
['Open' 'High' 'Low' 'Close' 'Volume' 'Ex-Dividend' 'Split Ratio'
 'Adj. Open' 'Adj. High' 'Adj. Low' 'Adj. Close' 'Adj. Volume'
 'Open-Close']
'''


if __name__ == "__main__":
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
    shortWindow = 40
    longWindow = 100
    # Create a new object trading algo
    movingWindowAlgo = MWS(aapl, shortWindow, longWindow)
    signals = movingWindowAlgo.movingwindow()

    '''
    Backtesting the simple algo
    '''
    initialCapital = float(100000.0)
    symbolText = 'AAPL'
    portfolio = BTA.backTest(initialCapital,signals,aapl,symbolText)

    '''
    Evaluatioins tools
    '''
    EveT.sharpeRatio(portfolio)

    '''
    Maximum Drawdown, which is used to measure the largest single drop from peak to 
    bottom in the value of a portfolio, 
    so before a new peak is achieved. In other words, the score indicates the risk
     of a portfolio chosen based on a certain strategy.
    '''

    # Define a trailing 252 trading day window
    window = 252
    EveT.maxDailyDrawdown(aapl, window)

    '''
    Compound Annual Growth Rate (CAGR), which provides you with a 
    constant rate of return over the time period. In other words,
     the rate tells you what you really have at the end of your investment period. 
    '''
    EveT.cagrCalculation(aapl)


    '''
    VWAP Example
    '''
    vwap = VWAP()
    aapl, vwapAddedColumn = vwap.setUpData(aapl)
    aapl = vwap.vwap(aapl, vwapAddedColumn, "BUY")
    vwap.plotVWAP(aapl)


    '''
    TWAP example
    Always use after VWAP as you need to setup the dataset to have TP typical price
    '''

    twap = TWAP()
    aapl = twap.twap(aapl)
    twap.plotTWAP(aapl)
