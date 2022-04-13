"""Crypto Linear Regression App by Peter Lieberman"""

# Loads basic libraries and dependencies
import pandas as pd
import numpy as np
import os
import financialanalysis as fa
import streamlit as st
#from dotenv import load_dotenv
from messari.messari import Messari
import matplotlib.pyplot as plt
import hvplot.pandas
import holoviews as hv
hv.extension('bokeh')

#load_dotenv()

# Insert your private key into a .env file. 
# A paid subscription is required.

#st.write("messari_api_key", os.environ["MESSARI_API_KEY"] == st.secrets["MESSARI_API_KEY"],)
messari_api_key = "b1eb4eab-94cd-4e5f-83be-24220395dd4e"
messari = Messari(messari_api_key)

# Header of application
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Crypto Analytics Application')

st.markdown("""
This app connects to crypto APIs and performs statistical analyses 
to predict future price trends!
* **Python libraries:** pandas, numpy, os, streamlit, messari.messari, financialanalysis, scikit-learn
* **Data source:** [Messari.io](https://messari.io/api).
* **Models:** linear regression, risk/return, and asset correlations
""")

# Code for the sidebar widgets
st.sidebar.header('User Input Features')

st.sidebar.caption('Select a crypto asset and the number of months to include in your analysis.')

# Twelve cryptocurrencies are included in analysis
cryptocurrencies = ['Bitcoin', 'Ethereum', 'Cardano', 
                    'BNB', 'Solana', 'Terra', 
                    'Avalanche', 'Polkadot', 'Polygon',
                    'NEAR', 'Algorand', 'Cosmos']

# Widget to select cryptocurrency
selected_asset = st.sidebar.selectbox('Cryptocurrency', cryptocurrencies)

# Widget to select timperiod (number of months) for analysis
number_of_months = st.sidebar.slider('Number of Months', min_value=1, max_value=60)
start_date = pd.to_datetime("today") - pd.DateOffset(months=number_of_months)
end_date = pd.to_datetime("today")


# Section 1: Function for Linear Regression
st.markdown("""**Linear Regression Channel**""")
st.markdown("""Chart shows the linear regression of time and price with standard deviation channels and the SMAs.""")

# Pulls and cleans price data from Messari API
# Utilizes financialanalysis (fa) module to build linear regression channels
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

    X = linear_regression_df["Date"].to_list() # converts Series to list
    X = fa.datetimeToFloatyear(X) # for example, 2020-07-01 becomes 2020.49589041
    X = np.array(X) # converts list to a numpy array
    X = X[::,None] # converts row vector to column vector (just column vector is acceptable)
    y = linear_regression_df[asset] # get y data (relative price)
    y = y.values # converts Series to numpy
    y = y[::,None] # row vector to column vector (just column vector is acceptable)
    
    slope, intercept, x, fittedline = fa.timeseriesLinearRegression(linear_regression_df["Date"], linear_regression_df[asset])

    
    fittedline_upper_1 = fittedline + std
    fittedline_lower_1 = fittedline - std
    fittedline_upper_2 = fittedline + (std*2)
    fittedline_lower_2 = fittedline - (std*2)
    
    fig = plt.figure(figsize=(16, 10)) # make canvas of picture. figsize is optional
    plt.plot(linear_regression_df["Date"], linear_regression_df[asset], label="Original", color="black") 
    plt.plot(linear_regression_df["Date"], fittedline, label="Prediction", color="red")
    plt.plot(linear_regression_df["Date"], fittedline_upper_1, label="1 Standard Deviation", color="green")
    plt.plot(linear_regression_df["Date"], fittedline_lower_1, color="green")
    plt.plot(linear_regression_df["Date"], fittedline_upper_2, color="blue")
    plt.plot(linear_regression_df["Date"], fittedline_lower_2, label="2 Standard Deviations", color="blue")
    plt.plot(linear_regression_df["Date"], sma200, label="200-Day Simple Moving Average", color="grey") # draw line (label is optional)
    plt.plot(linear_regression_df["Date"], sma50, label="50-Day Simple Moving Average", color="lightgrey")

    plt.xlabel("Date") # optional
    plt.ylabel("Price Change") # optional
    plt.title(f"{asset} Timeseries Data") # optional
    plt.legend(loc="best") # optional

    return st.pyplot()
    
chart = timeseries_linear_regression(selected_asset, start_date, end_date)


risk_free_rate = .025 # necessary for Sortino/Sharpe Ratio calculations

# Function to display summary statistics
# Pulls price data from Messari API and performs calculations
# Displays results as a bar chart
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

bar_chart = get_token_statistics(selected_asset, start_date, end_date).hvplot.bar(color="blue", hover_color="black", rot=45)

st.markdown("""**Financial Ratios & Statistics**""")
st.markdown("""Chart displays key risk/return metrics and financial ratios.""")
st.bokeh_chart(hv.render(bar_chart, backend="bokeh"))


# Function to pull timeseries price data for assets
# Feeds into functions that follow afterwards
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


# Builds two DataFrames that combine data for all the assets
# First DataFrame shows the close price data
# Second DataFrame shows the cumulative returns data
def load_crypto_prices(start_date, end_date):
    
    bitcoin_df = get_timeseries_data('Bitcoin', start_date, end_date)
    ethereum_df = get_timeseries_data('Ethereum', start_date, end_date)
    bnb_df = get_timeseries_data('BNB', start_date, end_date)
    cardano_df = get_timeseries_data('Cardano', start_date, end_date)
    solana_df = get_timeseries_data("Solana", start_date, end_date)
    terra_df = get_timeseries_data('Terra', start_date, end_date)
    avalanche_df = get_timeseries_data('Avalanche', start_date, end_date)
    polkadot_df = get_timeseries_data('Polkadot', start_date, end_date)
    polygon_df = get_timeseries_data('Polygon', start_date, end_date)
    cosmos_df = get_timeseries_data('Cosmos', start_date, end_date)
    algorand_df = get_timeseries_data('Algorand', start_date, end_date)
    near_df = get_timeseries_data('NEAR', start_date, end_date)

    crypto_returns = pd.concat([bitcoin_df["Bitcoin Cumulative Returns"], 
        ethereum_df["Ethereum Cumulative Returns"], bnb_df["BNB Cumulative Returns"],
        cardano_df["Cardano Cumulative Returns"], solana_df["Solana Cumulative Returns"], terra_df["Terra Cumulative Returns"], 
        avalanche_df["Avalanche Cumulative Returns"], polkadot_df["Polkadot Cumulative Returns"], polygon_df["Polygon Cumulative Returns"], 
        cosmos_df["Cosmos Cumulative Returns"], algorand_df["Algorand Cumulative Returns"], near_df["NEAR Cumulative Returns"]], axis= "columns", join="inner")

    crypto_prices = pd.concat([bitcoin_df["Bitcoin Price"], 
    ethereum_df["Ethereum Price"], bnb_df["BNB Price"],
    cardano_df["Cardano Price"], solana_df["Solana Price"], terra_df["Terra Price"], 
    avalanche_df["Avalanche Price"], polkadot_df["Polkadot Price"], polygon_df["Polygon Price"], 
    cosmos_df["Cosmos Price"], algorand_df["Algorand Price"], near_df["NEAR Price"]], axis= "columns", join="inner")

    column_names = ["Bitcoin", "Ethereum", 
                    "BNB Chain", "Cardano",
                    "Solana", "Terra",
                    "Avalanche", "Polkadot (DOT)",
                    "Polygon", "Cosmos",
                    "Algorand", "NEAR"]

    crypto_returns.columns = column_names
    crypto_prices.columns = column_names
    crypto_returns = crypto_returns.round(2)
    crypto_prices = crypto_prices.round(2)

    return crypto_returns, crypto_prices

crypto_returns, crypto_prices = load_crypto_prices(start_date, end_date)


# Function to calculate the asset correlations
def rolling_correlations(asset, days):
    
    rolling_correlations = pd.DataFrame(crypto_returns.rolling(window=int(days)).corr(crypto_returns[asset]).dropna())
    rolling_correlations = rolling_correlations.drop(columns={asset})
    
    rolling_correlations = rolling_correlations.round(2)
    rolling_correlations = rolling_correlations.iloc[-1]

    rolling_correlations = rolling_correlations.sort_values(ascending=True)
    
    return rolling_correlations


# Function to transform the number_of_months input into number_of_days
# "number_of_days" is used as the window to calculate the rolling correlations
def number_of_days(number_of_months):
    
    if number_of_months > 18:
        return 540
    
    else:
        return number_of_months * 30
    
number_of_days = number_of_days(number_of_months)

# Correlations heatmap
correlations = rolling_correlations(selected_asset, number_of_days)
correlations_plot = correlations.hvplot.heatmap(hover_color="black", rot=45, xaxis=None)

st.markdown("""**Asset Correlations**""")
st.markdown("""Heatmap displays the price correlation with other assets over selected time period.""")
st.caption("(A maximum of 18-months are included in calculation.)") 
st.latex("(r^2)")
st.bokeh_chart(hv.render(correlations_plot, backend="bokeh"))
