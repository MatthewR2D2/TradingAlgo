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
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class MovingWindowStrategy():

    def __init__(self, symbol, shortWindow, longWindow):
        self.symbol = symbol
        self.shortWindow = shortWindow
        self.longWindow = longWindow

    def movingwindow(self):
        # Create the signals
        signals = pd.DataFrame(index=self.symbol.index)
        signals['signal'] = 0.0

        # Create short simple moving avg over short window
        signals['short_mavg'] = self.symbol['Close'].rolling(window= self.shortWindow,
                                                      min_periods=1,
                                                      center=False).mean()

        # Create a long simple moving avg over the long window
        signals['long_mavg'] = self.symbol['Close'].rolling(window=self.longWindow,
                                                     min_periods=1,
                                                     center=False).mean()

        # Create the signals
        signals['signal'][ self.shortWindow:] = \
            np.where(signals['short_mavg'][ self.shortWindow:] >
                     signals['long_mavg'][ self.shortWindow:], 1.0, 0.0)

        # Create tradding orders
        signals['positions'] = signals['signal'].diff()

        # print the signals
        print(signals)

        fig = plt.figure()

        # Add a subplot and label for y-axis
        ax1 = fig.add_subplot(111, ylabel='Price in $')

        # Plot the closing price
        self.symbol['Close'].plot(ax=ax1, color='b', lw=2.)

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
        plt.title("Moving Window Strategy")
        plt.show()

        return signals