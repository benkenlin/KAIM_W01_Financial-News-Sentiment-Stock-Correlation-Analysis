# Financial News Sentiment Analysis Project

## Overview
This project analyzes financial news sentiment and its correlation with stock market movements for Nova Financial Solutions. It processes a large dataset of financial news headlines to extract insights about market sentiment and trading patterns.

## Business Objective
The project aims to:
- Analyze sentiment in financial news headlines using NLP techniques
- Establish statistical correlations between news sentiment and stock price movements
- Develop actionable trading strategies based on news sentiment analysis

## Dataset Description
The Financial News and Stock Price Integration Dataset (FNSPID) contains:
- **headline**: News article titles
- **url**: Direct link to full articles
- **publisher**: Article source/author
- **date**: Publication timestamp (UTC-4)
- **stock**: Stock ticker symbol




## Key Features
- Sentiment analysis of financial headlines
- Statistical correlation analysis
- Publication pattern analysis
- Publisher analysis
- Temporal trend analysis



## Initial Findings
- Dataset contains 1.4M records with 845K unique headlines
- Most common content type is analyst ratings
- Clear weekday vs weekend publication patterns
- Strong correlation between news sentiment and market movements

## Task 2: Stock Price Analysis


### Analysis Components
1. Technical Analysis
   - Moving averages (SMA, EMA) for trend identification
   - Momentum indicators (RSI, MACD)
   - Volatility measures (Bollinger Bands)
   - Volume analysis

2. Statistical Analysis
   - Return distributions
   - Volatility patterns
   - Correlation studies
   - Anomaly detection



### Key Findings
- Significant price movements often preceded by news sentiment shifts
- Trading volume shows strong correlation with news frequency
- Technical indicators provide confirmation of news-based signals
- Certain news categories have stronger price impact

### Task 3: Correlation Analysis

### Overview
The correlation analysis focuses on understanding the relationship between news sentiment and stock price movements. By analyzing how sentiment scores derived from news headlines correlate with daily stock returns, we can gain insights into market behavior.

### Analysis Components
1. Data Alignment
   - Align news and stock data by date to ensure accurate correlation analysis.
   - Filter datasets to include only overlapping dates for reliable results.

2. Sentiment Analysis
   - Calculate sentiment scores for news headlines using TextBlob.
   - Aggregate sentiment scores by date to analyze trends over time.

3. Stock Return Calculation
   - Compute daily stock returns based on adjusted closing prices.
   - Analyze the percentage change in stock prices to assess performance.

4. Correlation Calculation
   - Calculate Pearson correlation coefficients to quantify the relationship between sentiment and stock returns.
   - Identify stocks with the strongest and weakest correlations.

5. Visualization
   - Create scatter plots to visualize the relationship between sentiment scores and daily stock returns.
   - Generate bar plots to display correlation coefficients for each stock symbol.

### Key Findings
- The analysis reveals varying degrees of correlation between sentiment and stock performance across different stocks.
- Stocks like NVDA and AAPL show a strong positive correlation, indicating that higher sentiment is associated with increased stock returns.
- Conversely, some stocks exhibit negligible or negative correlations, suggesting that sentiment alone may not be a reliable predictor of stock performance.
- The scatter plots illustrate the complexity of the relationship, emphasizing the need for a multifaceted approach to understanding market behavior.

## Getting Started
1. Clone the repository
`https://github.com/benkenlin/KAIM_W01_Financial-News-Sentiment-Stock-Correlation-Analysis.git`
2. Install required dependencies:

`pip install -r requirements.txt`

3. Run the Jupyter notebooks in the `notebooks/` directory


## Requirements
- Python 3.x
- Required packages listed in requirements.txt
- Financial news and stock price datasets



## Acknowledgments
- 10 Academy for the project guidance






