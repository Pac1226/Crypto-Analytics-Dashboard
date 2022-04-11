"""Functions to Aggregate Crypto Data from the Messari API"""

# Required Libraries for Functions to execute in development environment
import pandas as pd
import datetime as dt
import os
import json
import requests
import sys
from dotenv import load_dotenv
from sqlalchemy import column
from formulas.api import (get_timeseries_data, get_token_statistics, get_daily_returns, get_mvrv)
import alpaca_trade_api as tradeapi

load_dotenv()

alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
a_api = tradeapi.REST(alpaca_api_key, alpaca_secret_key, api_version="v2")

start_date = '2020-10-14' 
end_date = pd.to_datetime("today")
tickers = ["SPY", "QQQ", "ARKK"]
timeframe = "1D"

# Function to save DataFrames as a CSV file
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

    column_names = ["Bitcoin (BTC)", "Ethereum (ETH)", 
                    "BNB Chain (BNB)", "Cardano (ADA)",
                    "Solana (SOL)", "Terra (LUNA)",
                    "Avalanche (AVAX)", "Polkadot (DOT)",
                    "Polygon (MATIC)", "Cosmos (ATOM)",
                    "Algorand (ALGO)", "NEAR (NEAR)"]

    crypto_returns.columns = column_names
    crypto_prices.columns = column_names
    crypto_returns = crypto_returns.round(2)
    crypto_prices = crypto_prices.round(2)

    return crypto_returns, crypto_prices

def load_crypto_statistics(start_date, end_date):

    bitcoin_statistics = get_token_statistics('Bitcoin', start_date, end_date)
    ethereum_statistics = get_token_statistics('Ethereum', start_date, end_date)
    bnb_statistics = get_token_statistics('BNB', start_date, end_date)
    cardano_statistics = get_token_statistics('Cardano', start_date, end_date)
    solana_statistics = get_token_statistics("Solana", start_date, end_date)
    terra_statistics = get_token_statistics('Terra', start_date, end_date)
    avalanche_statistics = get_token_statistics('Avalanche', start_date, end_date)
    polkadot_statistics = get_token_statistics('Polkadot', start_date, end_date)
    polygon_statistics = get_token_statistics('Polygon', start_date, end_date)
    cosmos_statistics = get_token_statistics('Cosmos', start_date, end_date)
    algorand_statistics = get_token_statistics('Algorand', start_date, end_date)
    near_statistics = get_token_statistics('NEAR', start_date, end_date)

    crypto_statistics = pd.concat(
        [bitcoin_statistics, ethereum_statistics, bnb_statistics,
        cardano_statistics, solana_statistics, terra_statistics, 
        avalanche_statistics, polkadot_statistics, polygon_statistics,
        cosmos_statistics, algorand_statistics, near_statistics], 
        axis= "rows", join="inner")

    column_names = ["Bitcoin (BTC)", "Ethereum (ETH)", 
                    "BNB Chain (BNB)", "Cardano (ADA)", 
                    "Solana (SOL)", "Terra (LUNA)", 
                    "Avalanche (AVAX)", "Polkadot (DOT)", 
                    "Polygon (MATIC)", "Cosmos (ATOM)", 
                    "Algorand (ALGO)", "NEAR (NEAR)"]

    crypto_statistics = pd.DataFrame(crypto_statistics.T)
    crypto_statistics.columns = column_names
    crypto_statistics = crypto_statistics.round(2) 
    crypto_statistics = crypto_statistics.rename_axis("Metric")

    return crypto_statistics


def load_stock_prices(start_date, end_date):

    #Pulls and cleans the data
    stock_prices = a_api.get_barset(tickers, timeframe, start=start_date, end=end_date, limit=1000).df
    stock_prices.reset_index(inplace=True)
    stock_prices = stock_prices.rename(columns={"time": "Date"})
    stock_prices["Date"] = stock_prices["Date"].dt.strftime('%Y-%m-%d')
    stock_prices["Date"] = pd.to_datetime(stock_prices["Date"], infer_datetime_format=True)
    stock_prices = stock_prices.set_index("Date")
    stock_prices = stock_prices.loc[f"{start_date}" : f"{end_date}"]

    # Creates new DataFrame for SPY, QQQ, ARKK
    sp500_df = pd.DataFrame(stock_prices["SPY"]["close"])
    sp500_df = sp500_df.rename(columns={"close": "S&P 500 (SPY)"})

    nasdaq_df = pd.DataFrame(stock_prices["QQQ"]["close"])
    nasdaq_df = nasdaq_df.rename(columns={"close": "NASDAQ (QQQ)"})

    arkk_df = pd.DataFrame(stock_prices["ARKK"]["close"])
    arkk_df = arkk_df.rename(columns={"close": "Ark Innovation Fund (ARKK)"})

    daily_returns = pd.concat([sp500_df,nasdaq_df, arkk_df],axis="columns", join="inner")
    daily_returns = daily_returns.pct_change().dropna()

    cumulative_returns = (1 + daily_returns).cumprod()
    cumulative_returns = cumulative_returns.round(2)
    
    return cumulative_returns


def load_power_rankings(start_date, end_date):

    bitcoin_df = get_daily_returns('Bitcoin', start_date, end_date)
    ethereum_df = get_daily_returns('Ethereum', start_date, end_date)
    bnb_df = get_daily_returns('BNB', start_date, end_date)
    cardano_df = get_daily_returns('Cardano', start_date, end_date)
    solana_df = get_daily_returns("Solana", start_date, end_date)
    terra_df = get_daily_returns('Terra', start_date, end_date)
    avalanche_df = get_daily_returns('Avalanche', start_date, end_date)
    polkadot_df = get_daily_returns('Polkadot', start_date, end_date)
    polygon_df = get_daily_returns('Polygon', start_date, end_date)
    cosmos_df = get_daily_returns('Cosmos', start_date, end_date)
    algorand_df = get_daily_returns('Algorand', start_date, end_date)
    near_df = get_daily_returns('NEAR', start_date, end_date)

    daily_returns = pd.concat([bitcoin_df["Bitcoin"], ethereum_df["Ethereum"], bnb_df['BNB'],
        cardano_df["Cardano"], solana_df["Solana"], terra_df["Terra"], 
        avalanche_df["Avalanche"], polkadot_df["Polkadot"], polygon_df["Polygon"], 
        cosmos_df["Cosmos"], algorand_df["Algorand"], near_df["NEAR"]], 
        axis= "columns", join="inner")
    

    crypto_rolling1year = daily_returns.tail(365)
    crypto_rolling1year = (1 + crypto_rolling1year).cumprod().dropna()
    crypto_rolling1year = crypto_rolling1year.tail(1)
    crypto_rolling1year.index = ["Last 12 Months"]

    crypto_crown = daily_returns
    crypto_crown = (1 + crypto_crown).cumprod().dropna()
    crypto_crown = crypto_crown.tail(1)
    crypto_crown.index = ["Since October 2020"]

    crypto_2022 = daily_returns.loc["2022-01-01":]
    crypto_2022 = (1 + crypto_2022).cumprod().dropna()
    crypto_2022 = crypto_2022.tail(1)
    crypto_2022.index = ["Year-to-Date (2022)"]

    crypto_2021 = daily_returns.loc["2021-01-01": "2021-12-31"]
    crypto_2021 = (1 + crypto_2021).cumprod().dropna()
    crypto_2021 = crypto_2021.tail(1)
    crypto_2021.index = ["Last Year (2021)"]

    crypto_rolling6month = daily_returns.tail(180)
    crypto_rolling6month = (1 + crypto_rolling6month).cumprod().dropna()
    crypto_rolling6month = crypto_rolling6month.tail(1)
    crypto_rolling6month.index = ["Last 180 Days"]

    crypto_rolling3month = daily_returns.tail(90)
    crypto_rolling3month = (1 + crypto_rolling3month).cumprod().dropna()
    crypto_rolling3month = crypto_rolling3month.tail(1)
    crypto_rolling3month.index = ["Last 90 Days"]

    crypto_monthly = daily_returns.tail(30)
    crypto_monthly = (1 + crypto_monthly).cumprod().dropna()
    crypto_monthly = crypto_monthly.tail(1)
    crypto_monthly.index = ["Last 30 Days"]

    power_rankings = pd.concat([crypto_rolling1year, crypto_crown, crypto_2022, crypto_2021, crypto_rolling6month, crypto_rolling3month, crypto_monthly], axis="rows", join="inner")
    column_names = ["Bitcoin (BTC)", "Ethereum (ETH)", 
                    "BNB Chain (BNB)", "Cardano (ADA)",
                    "Solana (SOL)", "Terra (LUNA)",
                    "Avalanche (AVAX)", "Polkadot (DOT)",
                    "Polygon (MATIC)", "Cosmos (ATOM)",
                    "Algorand (ALGO)", "NEAR (NEAR)"]
    power_rankings.columns = column_names
    power_rankings = power_rankings.T
    power_rankings = power_rankings.sort_values("Last 12 Months", ascending=False)
    power_rankings = power_rankings.round(2)
    power_rankings = power_rankings.rename_axis("Token")

    return power_rankings


def load_mvrv_data(start_date, end_date):

    bitcoin_mvrv = get_mvrv("Bitcoin", start_date, end_date)
    ethereum_mvrv = get_mvrv("Ethereum", start_date, end_date)
    cardano_mvrv = get_mvrv("Cardano", start_date, end_date)
    polkdot_mvrv = get_mvrv("Polkadot", start_date, end_date)

    mvrv_data = pd.concat([bitcoin_mvrv, ethereum_mvrv,
                            cardano_mvrv, polkdot_mvrv], 
                            axis="columns", join="outer")

    mvrv_data = mvrv_data.round(2)

    return mvrv_data