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
