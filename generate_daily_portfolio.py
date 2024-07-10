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
    total_portfolio_value = 0.0
    total_loss = 0.0
    total_profit = 0.0
    total_invested_funds = 0.0  # Initialize total invested funds
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
            total_invested_funds += total_investment_value  # Accumulate total invested funds

            # Determine broker and add statistics by broker
            broker = stock['Broker']
            if broker not in portfolio_by_broker:
                portfolio_by_broker[broker] = {
                    'Total Portfolio Value': 0.0,
                    'Total Investment (€)': 0.0,
                    'Total Loss (€)': 0.0,
                    'Total Profit (€)': 0.0,
                    'Total Win (€)': 0.0,  # Initialize Total Win for the broker
                    'Stocks': []
                }

            # Add stock statistics to broker's portfolio
            portfolio_by_broker[broker]['Stocks'].append({
                'Name': stock['Name'],
                'Ticker': ticker,
                'Total Investment (€)': format(total_investment_value, '.2f'),
                'Average Buy Value (€)': format(avg_buy_value, '.2f'),
                'Number of shares': format(number_of_shares, '.2f'),
                'Total value (€)': format(total_value, '.2f'),
                'Profit/Loss (€)': format(profit_loss_per_share, '.2f'),
                'Percentage Change (%)': format(percentage_change, '.2f'),
                'Total Stock Value (€)': format(total_stock_value, '.2f')
            })

            # Update broker's total portfolio value, total loss, total profit, total win, and total investment
            portfolio_by_broker[broker]['Total Portfolio Value'] += total_stock_value
            portfolio_by_broker[broker]['Total Profit (€)'] += profit_loss_per_share if profit_loss_per_share > 0 else 0
            portfolio_by_broker[broker]['Total Loss (€)'] += abs(profit_loss_per_share) if profit_loss_per_share < 0 else 0
            portfolio_by_broker[broker]['Total Investment (€)'] += total_investment_value
            portfolio_by_broker[broker]['Total Win (€)'] += profit_loss_per_share if profit_loss_per_share > 0 else 0  # Accumulate Total Win

    # Calculate net profit for each broker
    for broker, broker_data in portfolio_by_broker.items():
        broker_data['Total Profit (€)'] = format(broker_data['Total Win (€)'] - broker_data['Total Loss (€)'], '.2f')  # Calculate net profit
        broker_data['Total Portfolio Value'] = format(broker_data['Total Portfolio Value'], '.2f')
        broker_data['Total Investment (€)'] = format(broker_data['Total Investment (€)'], '.2f')
        broker_data['Total Loss (€)'] = format(broker_data['Total Loss (€)'], '.2f')
        broker_data['Total Win (€)'] = format(broker_data['Total Win (€)'], '.2f')
        sorted_stocks = sorted(broker_data['Stocks'], key=lambda x: x['Profit/Loss (€)'], reverse=True)
        broker_data['Top 3 Winners by Profit (€)'] = sorted_stocks[:3]
        broker_data['Top 3 Losers by Profit (€)'] = sorted_stocks[-3:]

    # Calculate total net profit
    total_profit_net = total_profit - total_loss

    # Prepare JSON object
    statistics = {
        'Name': f'Statistics_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}',
        'Total Portfolio Value (€)': format(total_portfolio_value, '.2f'),
        'Total Invested Funds (€)': format(total_invested_funds, '.2f'),
        'Total Win (€)': format(total_profit, '.2f'),  # Add total win
        'Total Profit (€)': format(total_profit_net, '.2f'),  # Total profit as the difference between total win and total loss
        'Total Loss (€)': format(total_loss, '.2f'),
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
    csv_file = 'data.csv'  # Change to your .csv name
    data = read_csv(csv_file)

    current_prices = {row['ticker']: get_price(row['ticker']) for row in data}

    statistics = calculate_statistics(data, current_prices)
    generate_statistics_json(statistics)

if __name__ == '__main__':
    main()
