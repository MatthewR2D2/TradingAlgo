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

class TWAP():

    def __init__(self):
        print("Twap")

    def twap(self, symbol):
        symbol['TWAP'] = symbol.TP.expanding().mean()
        symbol['TWAP-Signal'] = np.where(symbol['TWAP'] > symbol['TP'], 1.0, 0.0)
        print("TWAP")
        print(symbol)
        return symbol

    def plotTWAP(self, symbol):
        symbol[['TWAP', 'TP', 'TWAP-Signal']].plot()
        plt.title("TWAP and TP")

        plt.show()