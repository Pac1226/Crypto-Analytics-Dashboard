import pandas as pd
import datetime as dt
import numpy as np
from messari.messari import Messari
import financialanalysis as fa
import matplotlib.pyplot as plt
from pathlib import Path
from dotenv import load_dotenv
import os
import json
import requests
import sys


load_dotenv()

def rolling_correlations(prices_df, asset, window):

    rolling_correlations = pd.DataFrame(prices_df.rolling(window=int(window)).corr(prices_df[asset]).dropna())
    rolling_correlations = rolling_correlations.drop(columns={asset})
    print(f"{window}-Day Rolling Correlations")
    return rolling_correlations


def static_correlations(prices_df, asset):

    correlation_2month = prices_df.tail(60).corr() * prices_df.tail(60).corr()
    correlation_3month = prices_df.tail(90).corr() * prices_df.tail(90).corr()
    correlation_6month = prices_df.tail(180).corr() * prices_df.tail(180).corr()
    correlation_12month = prices_df.tail(365).corr() * prices_df.tail(365).corr()

    two_month = correlation_2month[asset]
    three_month = correlation_3month[asset]
    six_month = correlation_6month[asset]
    twelve_month = correlation_12month[asset]

    static_correlations = pd.DataFrame([ 
                                twelve_month, six_month,
                                three_month, two_month,],
                                index=["1-Year Correlation", 
                                "180-Day Correlation","90-Day Correlation", 
                                "60-Day Correlation"])

    static_correlations = static_correlations.drop(columns={asset})
    static_correlations = static_correlations.round(2)

    return static_correlations 


def correlations_matrix (prices_df, days):

    correlations_matrix = prices_df.tail(int(days)).corr() * prices_df.tail(int(days)).corr()

    correlations_matrix = correlations_matrix.round(2)
    
    return correlations_matrix


def technical_indicators(crypto_returns, asset):
    ta_df = pd.DataFrame(crypto_returns[asset])
    ta_df["SMA 200"] = ta_df[asset].rolling(window=200).mean()
    ta_df["SMA 50"] = ta_df[asset].rolling(window=50).mean()
    column_names = ["Returns", "SMA 200", "SMA 50"]
    ta_df.columns = column_names
    
    return ta_df

def timeseries_linear_regression(data, asset):
    
    linear_regression_df = data
    linear_regression_df.reset_index(inplace=True)
    
    X = linear_regression_df["Date"].to_list() # convert Series to list
    X = fa.datetimeToFloatyear(X) # for example, 2020-07-01 becomes 2020.49589041
    X = np.array(X) # convert list to a numpy array
    X = X[::,None] # convert row vector to column vector (just column vector is acceptable)
    y = linear_regression_df[asset] # get y data (relative price)
    y = y.values # convert Series to numpy
    y = y[::,None] # row vector to column vector (just column vector is acceptable)
    
    slope, intercept, x, fittedline = fa.timeseriesLinearRegression(linear_regression_df["Date"], linear_regression_df[asset])
    
    intercept_one_std = (intercept * 1.34) - intercept
    intercept_two_std = (intercept * 1.475) - intercept
    
    fittedline_std1_upper = fittedline + intercept_one_std
    fittedline_std1_lower = fittedline - intercept_one_std
    fittedline_std2_upper = fittedline + intercept_two_std
    fittedline_std2_lower = fittedline - intercept_two_std
    
    fig = plt.figure(figsize=(12, 7)) # make canvas of picture. figsize is optional
    plt.plot(linear_regression_df["Date"], linear_regression_df[asset], label="original", color="black") # draw line (label is optional)
    plt.plot(linear_regression_df["Date"], fittedline, label="prediction", color="red") # add one more line (label is optional)
    plt.plot(linear_regression_df["Date"], fittedline_std1_upper, label="1 Standard Deviation", color="green")
    plt.plot(linear_regression_df["Date"], fittedline_std1_lower, label="1 Standard Deviation", color="green")
    plt.plot(linear_regression_df["Date"], fittedline_std2_upper, label="2 Standard Deviations", color="blue")
    plt.plot(linear_regression_df["Date"], fittedline_std2_lower, label="2 Standard Deviations", color="blue")

    plt.xlabel("Date") # optional
    plt.ylabel("Price Change") # optional
    plt.suptitle(f"Linear Regression of {asset} Timeseries Data") # optional
    plt.legend(loc="best") # optional
    
    return