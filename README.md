****Investment Portfolio Analyzer****

**Overview**
This repository contains Python scripts designed to help you analyze and visualize your investment portfolio over time.

**Scripts**
generate_daily_portfolio.py

This script calculates the current value of your portfolio using Yahoo Finance's library to fetch real-time stock prices.
Prerequisites: You need to fill out the data_.csv file with your investment details. Based on this data, a portfolio_statistics.json file is generated with various statistics about your investments.
generate_all_time_portfolio.py

Utilizes the portfolio_statistics.json files generated by generate_daily_portfolio.py stored in the "historico" folder.
Provides visualizations to users, illustrating the evolution of their portfolio over time.
Setup: Ensure the "historico" folder contains all relevant JSON files. Modify the script to specify the path to this folder in the initial lines for proper functionality.

**Usage**
For generate_daily_portfolio.py:

**Setup:**

Install necessary Python libraries (e.g., Yahoo Finance API).
Ensure investments.csv is filled with accurate investment data (amount invested, stock symbols, etc.). 
**In order to get the correct Ticker for each stock, search in google for this: "*stock_you_want_to_search* ticker yahoo finance *currency*/*market*"**

**Execution**:

Run generate_daily_portfolio.py to calculate the current portfolio value and generate portfolio_statistics.json.
For generate_all_time_portfolio.py:
Setup:

Place all portfolio_statistics.json files generated by generate_daily_portfolio.py into the "historico" folder.
Update the script to specify the correct path to the "historico" folder.
Execution:

Run generate_all_time_portfolio.py to visualize the historical performance and composition of your portfolio.

**Future Development**

We are working towards developing an application where each user can access their data and visualizations through a personalized dashboard. This dashboard will provide comprehensive insights into the user's investment portfolio, including trends, performance metrics, and asset allocation over time.

**Feedback and Contributions**

This application is currently under active development. We welcome any suggestions, feedback, or contributions that can enhance its functionality or user experience.
