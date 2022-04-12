# Crypto Analytics Dashboard

The crypto analytics dashboard is a technical indicators application built by Peter Lieberman to guide crypto trading and investment strategies. It contains linear regression, asset correlation, and asset performance statistics, including Sortino Ratios and Peak to Trough data. The application collects real-time data from the Messari API, performs statstical modeling on the back-end, and displays the data in a Jupyter Notebook.


## Technologies

```python
The program uses a combination of first-party & third-party Python libraries: 
    
    - 3rd Party Libraries: Pandas, NumPy, FinancialAnalysis, Messari.Messari, Datetime, hvPlot, Matplotlib
    
    - 1st Party Modules: api.py, calculations.py, charts.py, filters.py
```
---

## Installation Guide

For most users, FinancialAnalysis, Messari.Messari will need to be installed prior to utilizing the Jupyter Notebooks. The Voila version can be asked by anyone through a web browser.

---

## Modules

The crypto_analytics.py is the main script. The "formulas" folder contains four (4) modules that I built that connect to the Messari API, clean the data, and run statistical models. The "data" folder contains several CSV files that contain data pulled from the Messari API. These data files are not used in the the application itself, but are shared for offline data analysis.


## Usage

The assets included in the dashboard are Bitcoin, Ethereum, Cardano, BNB Smart Chain, Solana, Avalanche, Terra, Polkadot, Polygon, Cosmos, NEAR, and Algorand. There are four (4) areas of anaylsis:

1) Crypto Power Rankings: displays the real-time price change of the crypto assets over the last 12 months, last 180 days, and the last 90 days

2) Financial Ratios & Performance Statistics: shows the price peak-to-trough and Sharpe, Sortino, and Calmar ratios over the last 12 months

3) Assets Correlations: shows the correlation of the crypto assets on a rolling 12 month basis, displayed as a heatmap

4) Linear Regressions: performs a timeseries linear regression that produces a parellel channel of the long-term mean and standard deviation. This is used to guide a "mean reversion" trading strategy 

---

## Charts



---

## Contributors

The application was built by Peter Lieberman.

---

## License

Anyone can utilize the application. However, the Jupyter Notebook requires a private key to access the data from the Messari API.