# Crypto Analytics Dashboard

This is an application that generates insights about the price action of crypto assets. It connects to the Messari API, which aggreggates data from crypto exchanges, protocols, and analytics firms. The app runs a series of statistical models on real-time price data and displays key insights as data visualizations.

There are two versions of the application:

The **first** application is **"crypto_analytics dashboard.ipynb."** It is a Jupyter Notebook that can be viewed at [nbviewer.org](https://nbviewer.org/github/Pac1226/Crypto-Analytics-Dashboard/blob/main/crypto_analytics_dashboard.ipynb).

The **second** application is **"crypto_streamlit_app.py."** This is an interactive web application hosted on Streamlit.

---

## Technologies

```python
The program uses Pandas, NumPy, FinancialAnalysis, Messari, Scikit-learn, hvPlot, Matplotlib, and sevaral custom built functions. 
```

---

## Installation Guide

FinancialAnalysis and Messari.Messari are required to run the Jupyter Notebook locally on your computer. There are four additional modules in the "formulas" folder that the application also depends on.

Accessing the web-applications requires no programming or downloading. These are accessible to anyone through a web browser.

--

## Crypto Assets

The applications aggregate, clean, and run models on timeseries price data collected on twelve (12) Layer One blockchain protocols.

* Bitcoin (BTC)
* Ethereum (ETH)
* BNB Chain (BNB)
* Solana (SOL)
* Cardano (ADA)
* Terra (LUNA)
* Avalanche (AVAX)
* Polygon (MATIC)
* Polkadot (DOT)
* NEAR Protocol (NEAR)
* Cosmos (ATOM)
* Algorand (ALGO)

--

## Analytics & Insights

There are four (4) key insights that can be displayed over any time period. For most assets, the data only goes back to Q3/Q4 2020.

* Historical Price Performance
  - Compares the price growth across time windows, giving a sense of shifting investor interest.
  
* Risk/Return Metrics
  - Builds a risk/return profile, showing the annual volatility, price peak, max drawdown, and the Sharpe, Sortino, and Calmar ratios.
  
* Asset Correlations
  - Displays the correlation among assets over any time period, proiding insights into portfolio construction and macro crypto sentinent.
  
* Linear Regressions
  - Runs machine learning models to pinpoint the linear regression paralell channel over any period.
  - Shows the regression line, standard deviation parellel lines, and the 50-Day / 200-Day Simple Moving Average (SMA).

---

## License

Running the Jupyter Notebook locally requires a private key to access the data from the Messari API.
