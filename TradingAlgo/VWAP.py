from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import matplotlib.pyplot as plt
from config import FinTechConfig as ftc
from pprint import pprint


# 1. open  2. high  3. low  4. close  5. volume

def vwap(data):
    print("Starting VWAP")
    data['TP'] = (data['2. high'] + data['3. low'] + data['4. close'] + data['1. open']) / 4
    data['TPV'] = data.TP * data['5. volume']
    data['SumTPV'] = data.TPV.cumsum()
    data['SumVol'] = data['5. volume'].cumsum()
    data["VWAP"] = data.SumTPV.div(data.SumVol)
    print("Finished VWAP")
    return data

def setUpData(data):
    # add vwap to the dataframe and other colums
    data["TP"] = ""
    data["TPV"] = ""
    data["SumTPV"] = ""
    data["SumVol"] = ""
    data["VWAP"] = ""
    columns = ["TP", "TPV", "SumTPV", "SumVol"]

    return data, columns



symbol = 'MSFT'
interval = '1min'
outputsize = 'full'

# Get TimeSeries
ts = TimeSeries(key=ftc.alpha_key, output_format='pandas')

data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)

data, columns = setUpData(data)

# do vwap and twap calculation
newData = vwap(data)
print("Remove data columns")
newData.drop(columns, inplace=True, axis=1)



print(newData.describe())
print("Plotting data")
newData.plot.line()

pprint(newData.head(2))
