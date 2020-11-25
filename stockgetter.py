#!/usr/bin/env python3 

import csv
from datetime import date
import datetime
from datetime import timedelta
import pandas as pd
from yahoofinancials import YahooFinancials

"""
Obtain yahoo stock prices and email to nominated email addresses

Program takes stocks as an input and returns prices. Some light analysis 
done then results sent to an SQLITE3 database. Selected elements taken and 
inserted into email and sent to selected email accounts.   

Paramaters:
    Nil. 
"""

currencies = ['EURUSD=X', 'JPY=X', 'GBPUSD=X', 'AUDUSD=X', 'INRUSD=X']  # The difference is AUDUSD=X or AUD=X

# Setup dates so they can be used later, has to be a weekday or when market is open
def price_range_setup():
    today = date.today()
    is_weekday = today.weekday()
    if is_weekday >= 0 and is_weekday <= 4:
        yesterday = today - timedelta(days=1)
        yesterday, today = str(yesterday), str(today)
        return yesterday, today
    else:
        print("Today is a weekend, no data is available")
        quit()
    
def write_to_csv(filename, func):
    with open(filename, "a") as archive:
        wr = csv.writer(archive)
        for value in func:
            wr.writerow(value)

def get_stock_prices():
    #yesterday, today = price_range_setup()
    for currency in currencies:     
        raw_data = YahooFinancials(currency)
        # raw_data = raw_data.get_historical_price_data(today, today, "daily") // remember has to be a weekday! 
        raw_data = raw_data.get_historical_price_data("2020-04-15", "2020-04-15", "daily")
        df = pd.DataFrame(raw_data[currency]['prices'])
        adjclose, close, date, high, low, opening, volume = df['adjclose'], df['close'], df['date'], \
                                                    df['high'], df['low'], df['open'], df['volume']
        yield currency, adjclose, close, date, high, low, opening, volume

# Iterate through elements and calculate whatever metrics you require
def calculate_metrics():
    for value in get_stock_prices():  
        currency, adjclose, close, unix_date, high, low, opening, volume = (value[0]), (value[1][0]), (value[2][0]), (value[3][0]), \
                                                                    (value[4][0]), (value[5][0]), (value[6][0]), (value[7][0])
        
        unix_timestamp = datetime.datetime.fromtimestamp(unix_date)
        adj_timestamp = unix_timestamp.strftime('%H:%M:%S %d-%m-%Y')
        intra_day_movement = low - high
        daily_difference = opening - close
        line = currency, adj_timestamp, opening, close, high, low, intra_day_movement, daily_difference
        yield line

write_to_csv("output.csv", calculate_metrics())



    
