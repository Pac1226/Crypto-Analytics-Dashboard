"""A Collection of Functions to Collect/Synthesis Crypto Data from the Messari API"""

# Required libraries and dependencies
import pandas as pd
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

messari_api_key = os.getenv("MESSARI_API_KEY")
messari = Messari(messari_api_key)

# Update the Risk-Free Rate using the 10-Year US Treasury Yield
risk_free_rate = .02



"""Timeseries Price Data Function to get historical price data for any crypto asset over any period"""

def get_timeseries_data(asset, start, end):

    # API pull from Messari for timeseries price data
    price_data = messari.get_metric_timeseries(asset_slugs=asset, asset_metric = "price", start=start, end=end)
    
    # Filters the data to capture the closing price only
    price_data = pd.DataFrame(price_data[asset]['close'])
    price_data = price_data.rename(columns={"close" : f"{asset} Price"})
    price_data.index.names = ['Date']
    
    # Function returns the daily returns, cumulative returns, and real price of the asset
    price_data[f"{asset} Daily Returns"] = price_data[f"{asset} Price"].pct_change()
    price_data[f"{asset} Cumulative Returns"] = (1 + price_data[f"{asset} Daily Returns"]).cumprod()

    price_data.dropna(inplace=True)
    return price_data


"""Timeseries Rolling Averages Function to get historical rolling averages for any crypto asset over any period"""

def get_rolling_averages(asset, start, end):

    # API pull from Messari for timeseries price data
    price_data = messari.get_metric_timeseries(asset_slugs=asset, asset_metric = "price", start=start, end=end)
    
    # Filters the data to capture the closing price only
    price_data = pd.DataFrame(price_data[asset]['close'])
    price_data = price_data.rename(columns={"close" : f"{asset} Price"})
    price_data.index.names = ['Date']
    
    # Function returns the daily returns, cumulative returns, and real price of the asset
    price_data[f"{asset} 180-Day Rolling Average"] = price_data[f"{asset} Price"].rolling(window=180).mean()
    price_data[f"{asset} 60-Day Rolling Average"] = price_data[f"{asset} Price"].rolling(window=60).mean()
    price_data[f"{asset} 180-Day Standard Deviation"] = price_data[f"{asset} Price"].rolling(window=180).std()
    price_data[f"{asset} 60-Day Standard Deviation"] = price_data[f"{asset} Price"].rolling(window=60).std()
    price_data = price_data.drop(columns=([f"{asset} Price"]))

    price_data.dropna(inplace=True)
    return price_data


""" Cumulative Returns Function to get the cumulative returns for any crypto asset over any period"""

def get_cumulative_returns(asset, start, end):
    
    # API pull from Messari for timeseries price data
    price_data = messari.get_metric_timeseries(asset_slugs=asset, asset_metric = "price", start=start, end=end)
    
    # Filters the data to capture the closing price only
    price_data = pd.DataFrame(price_data[asset]['close'])
    price_data = price_data.rename(columns={"close" : asset})
    price_data.index.names = ['Date']

    # Calculates cumulative returns of the asset
    # Column title is the "Asset" instead of "Cumulative Returns" to simplify the concatation of multiple assets later
    price_data[asset] = price_data[asset].pct_change()
    price_data[asset] = (1 + price_data[asset]).cumprod()
    price_data.dropna(inplace=True)

    # Calculates cumulative returns of the asset
    return price_data


""" Daily Returns Function to get average daily returns for any crypto asset over any period"""

def get_daily_returns(asset, start, end):
    
    # API pull from Messari for timeseries price data
    daily_returns = messari.get_metric_timeseries(asset_slugs=asset, asset_metric = "price", start=start, end=end)

    # Filters the data to capture the closing price only
    daily_returns = pd.DataFrame(daily_returns[asset]['close'])
    daily_returns = daily_returns.rename(columns={"close" : asset})
    daily_returns.index.names = ['Date']

    # Calculates average daily returns of the asset
    daily_returns[asset] = daily_returns[asset].pct_change()
    daily_returns.dropna(inplace=True)
    
    return daily_returns


""" Risk/Return Function that gets three risk/return metrics for any asset over any period"""

def get_mvrv (asset, start, end):
    
    # API pull from Messari for timeseries price data
    mcap_circulating_df = messari.get_metric_timeseries(asset_slugs=asset, asset_metric = "mcap.circ", start=start, end=end)
    mcap_realized_df = messari.get_metric_timeseries(asset_slugs=asset, asset_metric = "mcap.realized", start=start, end=end)

    # Combines data and calculates MVRV Ratio
    mvrv = pd.concat([mcap_circulating_df, mcap_realized_df], axis = "columns", join ="outer")
    mvrv.columns = [f"{asset} Market Cap", f"{asset} Realized Value"]
    mvrv[f"{asset} MVRV"] = mvrv[f"{asset} Market Cap"] / mvrv[f"{asset} Realized Value"]
    mvrv [f"{asset} Z-Score"] = (mvrv[f"{asset} MVRV"] - mvrv[f"{asset} MVRV"].mean()) / mvrv[f"{asset} MVRV"].std()
    mvrv = mvrv.drop(columns={f"{asset} Realized Value", f"{asset} MVRV"})

    return mvrv

def get_market_cap (asset, start, end):
    
    # API pull from Messari for timeseries price data
    mcap_circulating_df = messari.get_metric_timeseries(asset_slugs=asset, asset_metric = "mcap.circ", start=start, end=end)
    mcap_circulating_df.columns = [f"{asset} Market Cap"]

    return mcap_circulating_df    

def get_token_statistics(asset, start, end):
    
    # API pull from Messari for timeseries price data
    price_data = messari.get_metric_timeseries(asset_slugs=asset, asset_metric = "price", start=start, end=end)

    # Filters the data to capture the closing price only
    price_data = pd.DataFrame(price_data[asset]['close'])
    price_data = price_data.rename(columns={"close" : asset})
    price_data.index.names = ['Date']
    price_data = price_data.tail(365)
    
    # Calculates average daily returns and cumulative returns of the asset
    daily_returns = pd.DataFrame(price_data.pct_change().dropna())
    cumulative_returns = pd.DataFrame((1 + daily_returns).cumprod())
    total_return = cumulative_returns.iloc[-1]
    peak = cumulative_returns.expanding(min_periods=1).max()
    ath = peak.max()

    # Calculates annualized returns / standard deviation, the variance, and max drawdown
    standard_deviation = daily_returns.std() * np.sqrt(365)
    max_drawdown = (cumulative_returns/peak-1).min()
    negative_standard_deviation = daily_returns[daily_returns<0].std() * np.sqrt(365)

    # Calculates the Sharpe, Sortino, & Calmar Ratios. Negative Annualized Standard Deviation is used for Sortino Ratio
    sharpe_ratio = (total_return - risk_free_rate) / standard_deviation
    sortino_ratio = (total_return - risk_free_rate) / negative_standard_deviation
    calmar_ratio = (total_return - risk_free_rate) / (abs(max_drawdown))

    # Combines three metrics into a single DataFrame
    alist = []
    alist.append(total_return)
    alist.append(standard_deviation)
    alist.append(max_drawdown)
    alist.append(ath)
    alist.append(sharpe_ratio)
    alist.append(sortino_ratio)
    alist.append(calmar_ratio)
    token_statistics = pd.DataFrame(alist).T
    token_statistics.columns = ["Price Change", "Annual Volatility", "Max Drawdown", "Peak", "Sharpe Ratio", "Sortino Ratio", "Calmar Ratio"]
    token_statistics = token_statistics.round(2)

    return token_statistics



def get_cumulative_returns(asset, start, end):
    
    # API pull from Messari for timeseries price data
    price_data = messari.get_metric_timeseries(asset_slugs=asset, asset_metric = "price", start=start, end=end)
    
    # Filters the data to capture the closing price only
    price_data = pd.DataFrame(price_data[asset]['close'])
    price_data = price_data.rename(columns={"close" : asset})
    price_data.index.names = ['Date']

    # Calculates cumulative returns of the asset
    # Column title is the "Asset" instead of "Cumulative Returns" to simplify the concatation of multiple assets later
    price_data[asset] = price_data[asset].pct_change()
    price_data[asset] = (1 + price_data[asset]).cumprod()
    price_data.dropna(inplace=True)

    # Calculates cumulative returns of the asset
    return price_data


def timeseries_linear_regression(asset, start, end):
    
    # API pull from Messari for timeseries price data
    price_data = messari.get_metric_timeseries(asset_slugs=asset, asset_metric = "price", start=start, end=end)
    
    # Filters the data to capture the closing price only
    price_data = pd.DataFrame(price_data[asset]['close'])
    price_data = price_data.rename(columns={"close" : asset})
    price_data.index.names = ['Date']

    # Calculates cumulative returns of the asset
    # Column title is the "Asset" instead of "Cumulative Returns" to simplify the concatation of multiple assets later
    price_data[asset] = price_data[asset].pct_change()
    price_data[asset] = (1 + price_data[asset]).cumprod()
    price_data.dropna(inplace=True)
    
    sma200 = price_data.rolling(window=200).mean()
    sma50 = price_data.rolling(window=50).mean()
    
    std = price_data[asset].std()
    
    linear_regression_df = price_data
    linear_regression_df.reset_index(inplace=True)
    
    X = linear_regression_df["Date"].to_list() # convert Series to list
    X = fa.datetimeToFloatyear(X) # for example, 2020-07-01 becomes 2020.49589041
    X = np.array(X) # convert list to a numpy array
    X = X[::,None] # convert row vector to column vector (just column vector is acceptable)
    y = linear_regression_df[asset] # get y data (relative price)
    y = y.values # convert Series to numpy
    y = y[::,None] # row vector to column vector (just column vector is acceptable)
    
    slope, intercept, x, fittedline = fa.timeseriesLinearRegression(linear_regression_df["Date"], linear_regression_df[asset])

    
    fittedline_upper_1 = fittedline + std
    fittedline_lower_1 = fittedline - std
    fittedline_upper_2 = fittedline + (std*2)
    fittedline_lower_2 = fittedline - (std*2)
    
    fig = plt.figure(figsize=(16, 9)) # make canvas of picture. figsize is optional
    plt.plot(linear_regression_df["Date"], linear_regression_df[asset], label="original", color="black") 
    plt.plot(linear_regression_df["Date"], fittedline, label="prediction", color="red")
    plt.plot(linear_regression_df["Date"], fittedline_upper_1, label="1 Standard Deviation", color="green")
    plt.plot(linear_regression_df["Date"], fittedline_lower_1, label="1 Standard Deviation", color="green")
    plt.plot(linear_regression_df["Date"], fittedline_upper_2, label="2 Standard Deviations", color="blue")
    plt.plot(linear_regression_df["Date"], fittedline_lower_2, label="2 Standard Deviations", color="blue")
    plt.plot(linear_regression_df["Date"], sma200, label="SMA 200", color="grey") # draw line (label is optional)
    plt.plot(linear_regression_df["Date"], sma50, label="SMA 50", color="lightgrey")

    plt.xlabel("Date") # optional
    plt.ylabel("Price Change") # optional
    plt.suptitle(f"Linear Regression of {asset} Timeseries Data") # optional
    plt.legend(loc="best") # optional
    
    return