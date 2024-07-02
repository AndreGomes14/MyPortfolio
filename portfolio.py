import csv
import yfinance as yf
import json
from datetime import datetime

# Function to read the CSV file and return data as a list of dictionaries
def read_csv(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        data = [row for row in reader]
    return data

# Function to get the current price of a stock based on its ticker using yfinance
def get_price(ticker):
    try:
        ticker_data = yf.Ticker(ticker)
        current_price = ticker_data.history(period='1d')['Close'].iloc[-1]  # Last closing price
        return current_price
    except Exception as e:
        print(f'Error fetching price for {ticker}: {e}')
        return None

# Function to calculate profit/loss per stock and total portfolio value
def calculate_statistics(data, current_prices):
    total_portfolio_value = 0
    total_loss = 0
    total_profit = 0
    portfolio_by_broker = {}

    for stock in data:
        ticker = stock['ticker']
        avg_buy_value = float(stock['Average Buy Value'].replace(',', '.'))  # Convert to float
        number_of_shares = float(stock['Number of shares'].replace(',', '.'))  # Convert to float
        total_value = float(stock['Total value'].replace(',', '.'))  # Convert to float
        current_price = current_prices.get(ticker)

        if current_price:
            # Calculate profit/loss per share and percentage change
            profit_loss_per_share = (current_price - avg_buy_value) * number_of_shares
            percentage_change = ((current_price - avg_buy_value) / avg_buy_value) * 100 if avg_buy_value != 0 else 0

            # Calculate total value of the stock
            total_stock_value = current_price * number_of_shares

            # Calculate total portfolio value
            total_portfolio_value += total_stock_value

            # Accumulate total loss and profit
            if profit_loss_per_share < 0:
                total_loss += abs(profit_loss_per_share)
            else:
                total_profit += profit_loss_per_share

            # Calculate total investment value
            total_investment_value = avg_buy_value * number_of_shares

            # Determine broker and add statistics by broker
            broker = stock['Broker']
            if broker not in portfolio_by_broker:
                portfolio_by_broker[broker] = {
                    'Total Portfolio Value': 0,
                    'Total Investment (€)': 0,
                    'Total Loss (€)': 0,
                    'Total Profit (€)': 0,
                    'Stocks': []
                }

            # Add stock statistics to broker's portfolio
            portfolio_by_broker[broker]['Stocks'].append({
                'Name': stock['Name'],
                'Ticker': ticker,
                'Total Investment (€)': total_investment_value,
                'Average Buy Value (€)': avg_buy_value,
                'Number of shares': number_of_shares,
                'Total value (€)': total_value,
                'Profit/Loss (€)': profit_loss_per_share,
                'Percentage Change (%)': percentage_change,
                'Total Stock Value (€)': total_stock_value
            })

            # Update broker's total portfolio value, total loss, total profit, and total investment
            portfolio_by_broker[broker]['Total Portfolio Value'] += total_stock_value
            portfolio_by_broker[broker]['Total Profit (€)'] += profit_loss_per_share if profit_loss_per_share > 0 else 0
            portfolio_by_broker[broker]['Total Loss (€)'] += abs(profit_loss_per_share) if profit_loss_per_share < 0 else 0
            portfolio_by_broker[broker]['Total Investment (€)'] += total_investment_value

    # Calculate top 3 winners and losers based on profit/loss per share for each broker
    for broker, broker_data in portfolio_by_broker.items():
        sorted_stocks = sorted(broker_data['Stocks'], key=lambda x: x['Profit/Loss (€)'], reverse=True)
        broker_data['Top 3 Winners by Profit (€)'] = sorted_stocks[:3]
        broker_data['Top 3 Losers by Profit (€)'] = sorted_stocks[-3:]

    # Prepare JSON object
    statistics = {
        'Name': f'Statistics_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}',
        'Total Portfolio Value (€)': total_portfolio_value,
        'Total Profit (€)': total_profit,
        'Total Loss (€)': total_loss,
        'Portfolio by Broker': portfolio_by_broker
    }

    return statistics

# Function to generate JSON file with statistics
def generate_statistics_json(statistics):
    # Generate filename with current date and time
    filename = f'{statistics["Name"]}.json'

    # Write statistics to JSON file
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(statistics, jsonfile, indent=4, ensure_ascii=False)

    print(f'Statistics saved to {filename}')

def main():
    csv_file = 'data_.csv'  # Change to your .csv name
    data = read_csv(csv_file)

    current_prices = {row['ticker']: get_price(row['ticker']) for row in data}

    statistics = calculate_statistics(data, current_prices)
    generate_statistics_json(statistics)

if __name__ == '__main__':
    main()
