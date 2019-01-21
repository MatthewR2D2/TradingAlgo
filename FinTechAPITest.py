#Simple example of using the Alpha vantage API test
#AFPRIOB9PFYDM3L6   key https://www.alphavantage.co/support/#api-key

from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import matplotlib.pyplot as plt
from config import FinTechConfig as ftc #Store the alpha api key here

alpha_key = "AFPRIOB9PFYDM3L6"

ts = TimeSeries(key=alpha_key)
# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_intraday('GOOGL')
print(data)


#Get a symbol with special time

symbol = 'MSFT'
interval = '1min'
outputsize = 'full'


ts = TimeSeries(key=ftc.alpha_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol=symbol, interval= interval, outputsize=outputsize)
pprint(data.head(2))

#Simple Plotting of Data from Alpha vantage
ts = TimeSeries(key=ftc.alpha_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol=symbol,interval=interval, outputsize=outputsize)
data['2. high'].plot()
data['3. low'].plot()
plt.title('Intraday Times Series for the MSFT stock (1 min)')
plt.show()