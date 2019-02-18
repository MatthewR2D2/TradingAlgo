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
import matplotlib.pyplot as plt

def backTest(initialCapital, signals, symbol, symbolText):
    # Create a DataFrame `positions`
    positions = pd.DataFrame(index=signals.index).fillna(0.0)

    # Buy a 100 shares 'AAPL'
    positions[symbolText] = 100 * signals['signal']

    # Initialize the portfolio with value owned
    portfolio = positions.multiply(symbol['Adj. Close'], axis=0)

    # Store the difference in shares owned
    pos_diff = positions.diff()

    # Add `holdings` to portfolio
    portfolio['holdings'] = (positions.multiply(symbol['Adj. Close'], axis=0)).sum(axis=1)

    # Add `cash` to portfolio
    portfolio['cash'] = initialCapital - (pos_diff.multiply(symbol['Adj. Close'], axis=0)).sum(axis=1).cumsum()

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
    plt.title("Back Testing")
    plt.show()

    return portfolio
