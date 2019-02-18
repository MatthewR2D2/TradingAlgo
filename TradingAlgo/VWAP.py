import matplotlib.pyplot as plt
import numpy as np


class VWAP():
    def __init__(self):
        print("Created VWAP object")
    '''
    Available Columns
    ['Open' 'High' 'Low' 'Close' 'Volume' 'Ex-Dividend' 'Split Ratio'
     'Adj. Open' 'Adj. High' 'Adj. Low' 'Adj. Close' 'Adj. Volume'
     'Open-Close']
    '''

    '''
    This sets up the columns that are needed for VWAP
    Call this before the VWAP function
    '''
    def setUpData(self, symbol):
        # add vwap to the dataframe and other colums
        symbol["TP"] = ""  # Typical Price
        symbol["TPV"] = ""
        symbol["SumTPV"] = ""
        symbol["SumVol"] = ""
        symbol["VWAP"] = ""
        # Get rid of everything but VWAP
        newColumns = ["TPV", "SumTPV", "SumVol"]
        return symbol, newColumns

    '''
    This is the VWAP function 
    '''

    def vwap(self, symbol, columns, side):
        symbol['TP'] = (symbol['High'] + symbol['Low'] + symbol['Close'] + symbol['Open']) / 4
        symbol['TPV'] = symbol.TP * symbol['Volume']
        symbol['SumTPV'] = symbol.TPV.cumsum()
        symbol['SumVol'] = symbol['Volume'].cumsum()
        symbol["VWAP"] = symbol.SumTPV.div(symbol.SumVol)

        # Remove added columns from the dataframe
        symbol.drop(columns, inplace=True, axis=1)

        # Buy is 1 Sell is 0
        symbol['VWAP-Signal'] = np.where(symbol["VWAP"] > symbol['TP'], 1.0, 0.0)
        print(symbol[["VWAP", 'TP', 'VWAP-Signal']])
        return symbol

    def plotVWAP(self, symbol):

        symbol[['VWAP', 'TP', 'VWAP-Signal']].plot()
        plt.title("VWAP [High, Low, Close, Open]")

        plt.show()






