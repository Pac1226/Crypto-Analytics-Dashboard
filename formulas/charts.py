"""Functions for Building Interactive Charts"""

import pandas as pd
import datetime as dt
import os
import hvplot.pandas
import holoviews as hv
import panel as pn
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def crypto_widget():
    crypto_widget = pn.widgets.Select( 
    options= ['Bitcoin (BTC)', 'Ethereum (ETH)',
              'BNB Chain (BNB)','Cardano (ADA)',
              'Solana (SOL)', 'Terra (LUNA)', 
              'Avalanche (AVAX)', 'Polkadot (DOT)', 
              'Polygon (MATIC)', 'Cosmos (ATOM)', 
              'Algorand (ALGO)', 'NEAR (NEAR)'])

    return crypto_widget


def statistics_widget():
    statistics_widget = pn.widgets.Select( 
    options= ['Price Change', 'Annual Volatity', 
              'Max Drawdown', 'Peak', 
              'Sharpe Ratio', 'Sortino Ratio', 
              'Calmar Ratio'])

    return statistics_widget

def ratios_widget():
    ratios_widget = pn.widgets.Select( 
    options= ['Sharpe Ratio', 'Sortino Ratio', 
              'Calmar Ratio'])

    return ratios_widget

def rankings_widget():
    rankings_widget = pn.widgets.Select( 
    options= ['Last 12 Months', 'Since October 2020', 
            'Year-to-Date (2022)', 'Last Year (2021)', 
            'Last 180 Days', 'Last 90 Days', 
            'Last 30 Days'])

    return rankings_widget


def mvrv_price_chart(asset, mvrv_data):
    chart = make_subplots(specs=[[{"secondary_y" : True}]])
    chart.add_trace(go.Scatter(x=mvrv_data.index, y=mvrv_data[f"{asset} Market Cap"], name=f"{asset} Market Cap"), secondary_y=True,)
    chart.add_trace(go.Scatter(x=mvrv_data.index, y=mvrv_data[f"{asset} Z-Score"], name=f"{asset} MVRV Z-Score"), secondary_y=False,)
    chart.update_layout(title_text = f"{asset} Market Cap vs. MVRV Z-Score")
    chart.update_xaxes(title_text = "Date")
    chart.update_yaxes(title_text="Market Cap", secondary_y=True)
    chart.update_yaxes(title_text="MVRV Z-Score", secondary_y=False)
    chart.update_yaxes(ticklen=5, secondary_y=True)
    chart.update_layout(template="simple_white")
    chart

    return chart


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