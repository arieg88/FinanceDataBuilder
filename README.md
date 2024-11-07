# FinanceDataBuilder

## 🌟 News Scraper and Dataset Builder for Financial Data 📊

Welcome to the **News Scraper and Dataset Builder** repository! This project is designed to scrape financial news articles and build a comprehensive dataset that combines sentiment, emotions, and stock market performance. You can use this dataset for further analysis or to build machine learning models.

## 🔥 Features

- 📰 **Scrape News Articles**: Retrieve financial news articles from Yahoo Finance for top S&P 500 companies.
- 🌐 **Google URLs Scraper**: Extract relevant URLs from Google search results.
- 📈 **Stock Market Data**: Combine articles with hourly stock market data from Yahoo Finance.
- 💬 **Sentiment & Emotion Analysis**: Perform sentiment analysis (using FinBERT and Vader) and emotion analysis on the scraped articles.
- 📊 **Interactive Dashboards**: Visualize the data with interactive plots and insights using Dash.

### 📦 Required Libraries

- `requests` 📡
- `selenium` 🌐
- `beautifulsoup4` 🍲
- pandas 🐼
- `yfinance` 📉
- `finbert` 🤖
- `nltk` 🧠
- `vaderSentiment` 💭

### 1. 📰 **Yahoo Article Scraper**

This scraper fetches news articles from Yahoo Finance based on a search query and stores the article metadata (title, author, date, text).

### 2. 🌍 **Google URLs Scraper**

Fetches URLs from Google search results based on a query. This is useful for gathering links to news articles.

### 3. 📅 **Dataset Builder**

This script combines the scraped articles with stock market data, performs sentiment and emotion analysis, and outputs a comprehensive dataset.

The dataset contains:

- `Date`: The date of the article.
- `Title`: The title of the article.
- `Author`: The author of the article.
- `Text`: The full article text.
- `Company`: The company mentioned in the article.
- `Sentiment Scores`: Results from FinBERT and Vader.
- `Emotion Scores`: Emotional metrics (e.g., joy, fear, sadness).
- `Stock Data`: Hourly stock prices for the company.

### 4. 📊 **Dashboard for Data Visualization**

For visualizing the data, trends, sentiment, and emotions, you can use the interactive Dash dashboard. This is available in a separate repository. 

Check out the dashboard [here]([https://github.com/yourusername/dashboard-repository](https://github.com/arieg88/NewsAnalysisDashboard)).

The dashboard includes visualizations like:

- 🧮 Sentiment distribution by company.
- 📅 Article counts by month and week.
- 📈 Stock data and candlestick charts.
