# Crypto Analytics Dashboard

There are two applications that assess the risk/return profile of crypto assets and provide insight into future price movements using linear regressions. The app connects to the Messari API, a crypto research firm that aggreggates data from crypto exchanges, protocols, and analytics firms. The app runs a series of statistical models on real-time data, displaying key insights as data visualizations.

The **first** application is called **"crypto_analytics dashboard.ipynb."** It is a Jupyter Notebook that can be accessed over the internet through the below link for viewing only or downloaded from GitHub for full customization.

[nbviewer.org](https://nbviewer.org/github/Pac1226/Crypto-Analytics-Dashboard/blob/main/crypto_analytics_dashboard.ipynb)

The **second** application is **"crypto_streamlit_app.py."** This is an interactive web application hosted on Streamlit that responds to user inputs and updates in real-time. The data and insights are the same. The former is more comprehensive and the latter is more interactive and user-friendly.

---

## Technologies

```python
The program uses Pandas, NumPy, FinancialAnalysis, Messari, Scikit-learn, hvPlot, Matplotlib, and sevaral custom built functions. 
```

---

## Installation Guide

FinancialAnalysis and Messari.Messari will need to be installed to run the Jupyter Notebook locally on your computer. There are four additional modules in the "formulas" folder that the application depends on.

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

There are four (4) key insights that can be displayed over any time period for which there is data on the asset. For most assets, the data only goes back to Q3/Q4 2020.

* Historical Price Performance
  - Compares the price growth across time windows, giving a sense of shifting investor interest.
  
* Risk/Return Metrics
  - Builds a risk/return profile, showing the annual volatility, price peak, max drawdown, and the Sharpe, Sortino, and Calmar ratios.
  
* Asset Correlations
  - Displays the correlation among assets over any time period, which is used to build diversified portfolios and assess macro crypto sentinent.
  
* Linear Regressions
  - Runs machine learning models to pinpoint the linear regression paralell channel over any period.
  - Shows the regression line, parallel lines for one (1) and two (2) standard devaitions above/below the mean, and the Simple Moving Averages (SMA).

---

## License

Anyone can utilize the application. Running the Jupyter Notebook locally requires a private key to access the data from the Messari API.
