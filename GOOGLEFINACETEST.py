# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:44:56 2018

@author: Matt
"""
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd


def vwap(df):
    df['TP'] = (df['HIGH'] + df['LOW'] + df['CLOSE'] + df['OPEN']) / 4
    df['TPV'] = df.TP * df['VOLUME']
    df['SumTPV'] = df.TPV.cumsum()
    df['SumVol'] = df.VOLUME.cumsum()
    df["VWAP"] = df.SumTPV.div(df.SumVol)
    return df

#TWAP
def twap(df):
    
    df['TWAP'] = df.TP.expanding().mean()
    return df
    
#This returns the trade data that is requested
def get_trade_data(symbol, period, window, exch):
    url_root = ('http://www.google.com/finance/getprices?i='
                + str(period) + '&p=' + str(window)
                + 'd&f=d,o,h,l,c,v&df=cpct&x=' + exch.upper()
                + '&q=' + symbol.upper())
    response = urllib.request.urlopen(url_root)
    data=response.read().decode().split('\n')       #decode() required for Python 3
    data = [data[i].split(',') for i in range(len(data)-1)]
    header = data[0:7]
    data = data[7:]
    header[4][0] = header[4][0][8:]                 #get rid of 'Columns:' for label row
    df=pd.DataFrame(data, columns=header[4])
    df = df.dropna()                                #to fix the inclusion of more timezone shifts in the .csv returned from the goog api
    df.index = range(len(df))                       #fix the index from the previous dropna()

    ind=pd.Series(len(df))
    for i in range(len(df)):
        if df['DATE'].ix[i][0] == 'a':
            anchor_time = dt.datetime.fromtimestamp(int(df['DATE'].ix[i][1:]))  #make datetime object out of 'a' prefixed unix timecode
            ind[i]=anchor_time
        else:
            ind[i] = anchor_time +dt.timedelta(seconds = (period * int(df['DATE'].ix[i])))
    df.index = ind

    df=df.drop('DATE', 1)

    for column in df.columns:                #shitty implementation because to_numeric is pd but does not accept df
        df[column]=pd.to_numeric(df[column])

    return df


# input data
#symbol: ticker
#period: sample frequency in seconds
#window: number of days in days
#exch: exchange to get data

ticker = 'MSFT'
period = 60
days = 1
exchange = 'NASD'

df = get_trade_data(ticker, period, days, exchange)

#print('Head of data')
#print(df.head(10))

#add vwap to the dataframe and other colums
df["TP"] = ""
df["TPV"] = ""
df["SumTPV"] = ""
df["SumVol"] = ""
df["VWAP"] = ""
df["TWAP"]= ""

colums = ["TP", "TPV", "SumTPV", "SumVol", "VOLUME"]




#do vwap and twap calculation
df = vwap(df)
df = twap(df)
print(df.head(6))

df.drop(colums, inplace = True, axis = 1)

#print (df.describe())
df.plot(figsize=(30,20), style='.-')







